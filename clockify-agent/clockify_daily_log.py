#!/usr/bin/env python3
"""
clockify_daily_log.py

Reads today's Claude Code session JSONL files, groups work into blocks by
time gaps, generates honest descriptions via Claude API (Haiku), and creates
Clockify entries for each block.

Usage:
    python3 clockify_daily_log.py
    python3 clockify_daily_log.py --yesterday
    python3 clockify_daily_log.py --dry-run
    python3 clockify_daily_log.py --date 2026-05-23

Setup:
    1. Copy clockify_config.example.json → clockify_config.json
    2. Fill in your API keys (see SKILL.md for how to get them)
    3. Run the script
"""

import json
import sys
import argparse
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- CONFIG (loaded from clockify_config.json in same directory) -------------
def _load_config():
    config_path = Path(__file__).parent / "clockify_config.json"
    if not config_path.exists():
        raise FileNotFoundError(
            f"\nConfig file not found: {config_path}\n"
            "Copy clockify_config.example.json to clockify_config.json and fill in your keys.\n"
            "See SKILL.md for instructions.\n"
        )
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

_cfg = _load_config()

CLOCKIFY_API_KEY   = _cfg["clockify_api_key"]
CLOCKIFY_WORKSPACE = _cfg["clockify_workspace"]
CLOCKIFY_PROJECT   = _cfg["clockify_project"]
CLOCKIFY_URL       = "https://api.clockify.me/api/v1"

ANTHROPIC_API_KEY  = _cfg["anthropic_api_key"]
ANTHROPIC_MODEL    = _cfg.get("anthropic_model", "claude-haiku-4-5-20251001")

SESSIONS_DIR       = Path.home() / ".claude" / "projects"
LOCAL_UTC_OFFSET   = _cfg.get("utc_offset_hours", 2)   # Spain CEST = UTC+2
GAP_MINUTES        = 30   # gap > N min between messages = new work block
MIN_BLOCK_MINUTES  = 5    # ignore blocks shorter than this

# Blocked windows: time ranges when Claude was NOT doing your own work
# Format: (weekday, start_hour, start_min, end_hour, end_min)
BLOCKED_WINDOWS = _cfg.get("blocked_windows", [])
WEEKDAY_NAMES = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
# -----------------------------------------------------------------------------

_user_id_cache = None


def parse_args():
    p = argparse.ArgumentParser(description="Log Claude sessions to Clockify")
    p.add_argument("--yesterday", action="store_true",
                   help="Process yesterday instead of today")
    p.add_argument("--date", metavar="YYYY-MM-DD",
                   help="Process a specific date (e.g. 2026-05-23)")
    p.add_argument("--dry-run", action="store_true",
                   help="Show detected blocks without creating Clockify entries")
    return p.parse_args()


def target_date(yesterday=False, date_str=None):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    d = datetime.now(timezone.utc).date()
    if yesterday:
        d -= timedelta(days=1)
    return d


def load_messages_per_session(target_d):
    """Return list of (session_id, [messages]) — one entry per JSONL file."""
    sessions = []
    for jsonl_file in sorted(SESSIONS_DIR.rglob("*.jsonl")):
        msgs = []
        try:
            with open(jsonl_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        t   = obj.get("type")
                        ts  = obj.get("timestamp", "")
                        if t not in ("user", "assistant") or not ts:
                            continue
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        if dt.date() != target_d:
                            continue
                        content = obj.get("message", {}).get("content", "")
                        if isinstance(content, list):
                            text = " ".join(
                                c.get("text", "")
                                for c in content
                                if isinstance(c, dict) and c.get("type") == "text"
                            )
                        else:
                            text = str(content)
                        text = text.strip()
                        if not text:
                            continue
                        if text.startswith("<task-notification>"):
                            continue
                        if text.startswith("<system-reminder>"):
                            continue
                        msgs.append({
                            "role": t,
                            "timestamp": dt,
                            "text": text[:400]
                        })
                    except Exception:
                        continue
        except Exception:
            continue
        if msgs:
            session_id = jsonl_file.stem[:8]
            sessions.append((session_id, sorted(msgs, key=lambda x: x["timestamp"])))
    return sessions


def group_blocks(messages):
    if not messages:
        return []
    blocks  = []
    current = [messages[0]]
    for msg in messages[1:]:
        gap = (msg["timestamp"] - current[-1]["timestamp"]).total_seconds() / 60
        if gap > GAP_MINUTES:
            blocks.append(current)
            current = [msg]
        else:
            current.append(msg)
    blocks.append(current)
    return blocks


def check_blocked_window(start_utc, end_utc):
    offset      = timedelta(hours=LOCAL_UTC_OFFSET)
    start_local = start_utc + offset
    end_local   = end_utc   + offset
    day_name    = WEEKDAY_NAMES[start_local.weekday()]

    for win in BLOCKED_WINDOWS:
        win_day, sh, sm, eh, em = win[0], win[1], win[2], win[3], win[4]
        if day_name != win_day:
            continue
        win_start = start_local.replace(hour=sh, minute=sm, second=0, microsecond=0)
        win_end   = start_local.replace(hour=eh, minute=em, second=0, microsecond=0)
        if start_local < win_end and end_local > win_start:
            return (
                f"WARNING: overlaps {win_day} blocked window "
                f"{sh:02d}:{sm:02d}-{eh:02d}:{em:02d} local"
            )
    return None


def generate_description_multi(all_messages, n_sessions):
    lines = []
    for m in all_messages[:25]:
        role = "User" if m["role"] == "user" else "Claude"
        lines.append(f"{role}: {m['text'][:150]}")

    context = (
        f"These messages come from {n_sessions} parallel Claude Code sessions "
        f"the user had open simultaneously.\n\n"
        if n_sessions > 1
        else ""
    )

    prompt = (
        f"{context}"
        "Write a Clockify time entry description (max 100 chars) covering all the work done. "
        "Format: 'topic1, work1 + topic2, work2' if topics differ, or single description if same topic. "
        "Be honest and concrete. Examples: "
        "'optimus k, Phase 93 auth + Clockify, automation script' / "
        "'exp3rea, funnel analysis and pricing'. "
        "Reply with ONLY the description, no quotes.\n\n"
        "Sessions content:\n" + "\n".join(lines)
    )

    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": ANTHROPIC_MODEL,
                "max_tokens": 100,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=20,
        )
        if r.status_code == 200:
            return r.json()["content"][0]["text"].strip().strip('"').strip("'")
        else:
            print(f"  Claude API error {r.status_code}: {r.text[:80]}")
    except Exception as e:
        print(f"  Claude API error: {e}")

    return "Claude Code session"


def create_entry(start_utc, end_utc, description):
    payload = {
        "start":       start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end":         end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description": description,
        "projectId":   CLOCKIFY_PROJECT,
        "billable":    True,
        "tagIds":      [],
    }
    r = requests.post(
        f"{CLOCKIFY_URL}/workspaces/{CLOCKIFY_WORKSPACE}/time-entries",
        headers={
            "X-Api-Key":    CLOCKIFY_API_KEY,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=10,
    )
    return r.status_code == 201, r.json()


def get_user_id():
    global _user_id_cache
    if _user_id_cache:
        return _user_id_cache
    try:
        r = requests.get(
            f"{CLOCKIFY_URL}/user",
            headers={"X-Api-Key": CLOCKIFY_API_KEY},
            timeout=10,
        )
        if r.status_code == 200:
            _user_id_cache = r.json()["id"]
    except Exception:
        pass
    return _user_id_cache


def get_existing_entries_for_day(target_d):
    user_id = get_user_id()
    if not user_id:
        return []
    day_start = datetime(target_d.year, target_d.month, target_d.day, tzinfo=timezone.utc)
    day_end   = day_start + timedelta(days=1)
    try:
        r = requests.get(
            f"{CLOCKIFY_URL}/workspaces/{CLOCKIFY_WORKSPACE}/user/{user_id}/time-entries",
            headers={"X-Api-Key": CLOCKIFY_API_KEY},
            params={
                "start":     day_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end":       day_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "page-size": 100,
            },
            timeout=10,
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []


def find_overlapping(block_start, block_end, day_entries):
    result = []
    for entry in day_entries:
        ti    = entry.get("timeInterval", {})
        s_raw = ti.get("start")
        e_raw = ti.get("end")
        if not s_raw or not e_raw:
            continue
        ei_s = datetime.fromisoformat(s_raw.replace("Z", "+00:00"))
        ei_e = datetime.fromisoformat(e_raw.replace("Z", "+00:00"))
        if ei_s < block_end and ei_e > block_start:
            result.append(entry)
    return result


def fmt_dur(minutes):
    h, m = int(minutes) // 60, int(minutes) % 60
    return f"{h}h {m:02d}m"


def merge_overlapping_blocks(sessions):
    raw = []
    for session_id, messages in sessions:
        for block in group_blocks(messages):
            s = block[0]["timestamp"]
            e = block[-1]["timestamp"]
            raw.append((s, e, block))

    if not raw:
        return []

    raw.sort(key=lambda x: x[0])

    merged = []
    cur_start, cur_end, cur_msgs = raw[0]

    for s, e, msgs in raw[1:]:
        gap = (s - cur_end).total_seconds() / 60
        if gap <= GAP_MINUTES:
            cur_end  = max(cur_end, e)
            cur_msgs = cur_msgs + msgs
        else:
            merged.append((cur_start, cur_end, cur_msgs))
            cur_start, cur_end, cur_msgs = s, e, msgs

    merged.append((cur_start, cur_end, cur_msgs))
    return merged


def main():
    args   = parse_args()
    target = target_date(args.yesterday, args.date)
    label  = args.date if args.date else ("yesterday" if args.yesterday else "today")

    print(f"\nClockify Daily Log -- {target} ({label})")
    print("-" * 50)

    sessions = load_messages_per_session(target)
    if not sessions:
        print(f"No Claude session messages found for {target}.")
        sys.exit(0)

    total_msgs = sum(len(m) for _, m in sessions)
    print(f"Sessions: {len(sessions)} | Messages: {total_msgs}")

    merged_blocks = merge_overlapping_blocks(sessions)
    print(f"Merged time blocks: {len(merged_blocks)}\n")

    existing_day_entries = get_existing_entries_for_day(target)

    created  = 0
    skipped  = 0
    offset   = timedelta(hours=LOCAL_UTC_OFFSET)

    for i, (start_utc, end_utc, all_msgs) in enumerate(merged_blocks, 1):
        minutes     = (end_utc - start_utc).total_seconds() / 60
        start_local = start_utc + offset
        end_local   = end_utc   + offset
        n_sessions  = len(sessions)

        print(
            f"Block {i}/{len(merged_blocks)}: "
            f"{start_local.strftime('%H:%M')}-{end_local.strftime('%H:%M')} local "
            f"({fmt_dur(minutes)}, {n_sessions} session(s))"
        )

        if minutes < MIN_BLOCK_MINUTES:
            print(f"  -> Skipped (too short: {minutes:.0f} min)\n")
            skipped += 1
            continue

        warn = check_blocked_window(start_utc, end_utc)
        if warn:
            print(f"  {warn}")

        print(f"  Generating description...", end=" ", flush=True)
        description = generate_description_multi(all_msgs, n_sessions)
        print(f"-> '{description}'")

        overlaps = find_overlapping(start_utc, end_utc, existing_day_entries)
        if overlaps:
            n = len(overlaps)
            print(f"  [DUPLICATE] {n} existing entr{'y' if n == 1 else 'ies'} overlap this block:")
            for ov in overlaps:
                ov_s    = datetime.fromisoformat(ov["timeInterval"]["start"].replace("Z", "+00:00")) + offset
                ov_e    = datetime.fromisoformat(ov["timeInterval"]["end"].replace("Z", "+00:00")) + offset
                ov_desc = ov.get("description", "(no description)")[:60]
                print(f"    * {ov_s.strftime('%H:%M')}-{ov_e.strftime('%H:%M')} local: '{ov_desc}'")

        if args.dry_run:
            tag = " (DUPLICATE RISK)" if overlaps else ""
            print(f"  [DRY RUN] Would create entry{tag}.\n")
            continue

        prompt = "  Create anyway? [y/n/e=edit]: " if overlaps else "  Create entry? [y/n/e=edit description]: "
        confirm = input(prompt).strip().lower()
        if confirm == "e":
            description = input("  New description: ").strip() or description
            confirm = "y"
        if confirm != "y":
            print("  Skipped.\n")
            skipped += 1
            continue

        ok, result = create_entry(start_utc, end_utc, description)
        if ok:
            print(f"  OK - Entry created!\n")
            created += 1
        else:
            print(f"  ERROR: {result}\n")
            skipped += 1

    print("-" * 50)
    if args.dry_run:
        eligible = sum(
            1 for s, e, _ in merged_blocks
            if (e - s).total_seconds() / 60 >= MIN_BLOCK_MINUTES
        )
        print(f"DRY RUN complete. {eligible} entries would be created.")
    else:
        print(f"Done. {created} entries created, {skipped} skipped.")


if __name__ == "__main__":
    main()
