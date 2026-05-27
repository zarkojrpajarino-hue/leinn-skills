#!/usr/bin/env python3
"""
clockify_daily_log.py

Reads today's Claude Code session JSONL files, groups work into blocks by
time gaps, generates honest descriptions via Claude API (Haiku), and creates
Clockify entries for each block.

New in v2: asks for manual entries before confirming, shows complete day
table, then confirms everything together.

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
import re
import sys
import argparse
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- CONFIG ------------------------------------------------------------------
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
LOCAL_UTC_OFFSET   = _cfg.get("utc_offset_hours", 2)
GAP_MINUTES        = 30
MIN_BLOCK_MINUTES  = 5

BLOCKED_WINDOWS    = _cfg.get("blocked_windows", [])
WEEKDAY_NAMES      = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
# -----------------------------------------------------------------------------

_user_id_cache = None


# ─── ARGUMENT PARSING ────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="Log Claude sessions to Clockify")
    p.add_argument("--yesterday", action="store_true")
    p.add_argument("--date", metavar="YYYY-MM-DD")
    p.add_argument("--dry-run", action="store_true",
                   help="Show entries without creating them in Clockify")
    return p.parse_args()


def target_date(yesterday=False, date_str=None):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    d = datetime.now(timezone.utc).date()
    if yesterday:
        d -= timedelta(days=1)
    return d


# ─── SESSION LOADING ─────────────────────────────────────────────────────────

def load_messages_per_session(target_d):
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
                        if text.startswith(("<task-notification>", "<system-reminder>")):
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


# ─── BLOCK GROUPING & MERGING ────────────────────────────────────────────────

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


def merge_overlapping_blocks(sessions):
    raw = []
    for _, messages in sessions:
        for block in group_blocks(messages):
            raw.append((block[0]["timestamp"], block[-1]["timestamp"], block))

    if not raw:
        return []

    raw.sort(key=lambda x: x[0])
    merged = []
    cur_start, cur_end, cur_msgs = raw[0]

    for s, e, msgs in raw[1:]:
        if (s - cur_end).total_seconds() / 60 <= GAP_MINUTES:
            cur_end  = max(cur_end, e)
            cur_msgs = cur_msgs + msgs
        else:
            merged.append((cur_start, cur_end, cur_msgs))
            cur_start, cur_end, cur_msgs = s, e, msgs

    merged.append((cur_start, cur_end, cur_msgs))
    return merged


# ─── DESCRIPTION GENERATION ──────────────────────────────────────────────────

def generate_description_multi(all_messages, n_sessions):
    lines = []
    for m in all_messages[:25]:
        role = "User" if m["role"] == "user" else "Claude"
        lines.append(f"{role}: {m['text'][:150]}")

    context = (
        f"These messages come from {n_sessions} parallel Claude Code sessions simultaneously.\n\n"
        if n_sessions > 1 else ""
    )
    prompt = (
        f"{context}"
        "Write a Clockify time entry description (max 100 chars). "
        "Format: 'topic, work done'. Be honest and concrete. Examples: "
        "'optimus k, Phase 93 auth RLS JWT' / 'leinn pitch, one-pager HTML + clockify'. "
        "Reply with ONLY the description, no quotes.\n\nSessions:\n" + "\n".join(lines)
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
        print(f"  Claude API error {r.status_code}: {r.text[:80]}")
    except Exception as e:
        print(f"  Claude API error: {e}")
    return "Claude Code session"


# ─── MANUAL ENTRY PARSING ────────────────────────────────────────────────────

def ask_manual_entries(target_d, offset_hours, dry_run=False):
    """Ask the user for work done outside Claude sessions."""
    W = 60
    print()
    print("─" * W)
    print("  ¿Hay trabajo que añadir fuera de las sesiones?")
    print("  (reuniones, llamadas, trabajo sin ordenador...)")
    print()
    print("  Ejemplos:")
    print("    'reunión con inversores 10:00-11:30'")
    print("    'llamada cliente 15:00-16:00, gym 07:00-08:00'")
    print("    'clase LEINN toda la mañana 9:00-14:00'")
    print()
    print("  Pulsa Enter o escribe 'no' para saltar.")
    print("─" * W)

    try:
        user_input = input("\n  > ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return []

    if not user_input or user_input.lower() in ("no", "n", "nada", "none", "skip", ""):
        return []

    print("  Procesando...", end=" ", flush=True)
    entries = _parse_manual_with_claude(user_input, target_d, offset_hours)
    n = len(entries)
    print(f"{'OK' if n else 'no se detectaron entradas'} — {n} entrada{'s' if n != 1 else ''}")
    return entries


def _parse_manual_with_claude(text, target_d, offset_hours):
    """Use Claude to parse natural language time entries into structured dicts."""
    prompt = (
        f"Parse these work/time entries. Today: {target_d}. "
        f"Local timezone: UTC+{offset_hours}.\n\n"
        f"User input: \"{text}\"\n\n"
        "Return ONLY a JSON array. Each item must have:\n"
        "  \"description\": string (same language as input)\n"
        "  \"start_local\": \"HH:MM\" (24h)\n"
        "  \"end_local\": \"HH:MM\" (24h)\n\n"
        "Rules:\n"
        "- If duration given ('1h meeting'), calculate end = start + duration\n"
        "- If only duration with no start time, use a reasonable estimate\n"
        "- Return [] if nothing parseable\n\n"
        "Example output: "
        "[{\"description\": \"reunión con inversores\", \"start_local\": \"10:00\", \"end_local\": \"11:30\"}]"
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
                "max_tokens": 400,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=20,
        )
        if r.status_code != 200:
            print(f"\n  Claude API error {r.status_code}")
            return []

        raw   = r.json()["content"][0]["text"].strip()
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if not match:
            return []

        parsed    = json.loads(match.group())
        offset_td = timedelta(hours=offset_hours)
        result    = []

        for item in parsed:
            try:
                sh, sm = map(int, item["start_local"].split(":"))
                eh, em = map(int, item["end_local"].split(":"))
                # Build local datetime and convert to UTC
                start_utc = datetime(
                    target_d.year, target_d.month, target_d.day,
                    sh, sm, 0, tzinfo=timezone.utc
                ) - offset_td
                end_utc = datetime(
                    target_d.year, target_d.month, target_d.day,
                    eh, em, 0, tzinfo=timezone.utc
                ) - offset_td
                if end_utc <= start_utc:
                    end_utc += timedelta(hours=24)
                result.append({
                    "start_utc":   start_utc,
                    "end_utc":     end_utc,
                    "description": item["description"],
                    "source":      "manual",
                    "warning":     None,
                })
            except Exception:
                continue
        return result
    except Exception as e:
        print(f"\n  Parse error: {e}")
        return []


# ─── TABLE DISPLAY ───────────────────────────────────────────────────────────

def _fmt_dur(start_utc, end_utc):
    mins = (end_utc - start_utc).total_seconds() / 60
    h, m = int(mins) // 60, int(mins) % 60
    return f"{h}h{m:02d}m", mins


def print_day_table(entries, offset_hours, title):
    """Print a formatted table of time entries."""
    W     = 72
    OFS   = timedelta(hours=offset_hours)
    sep   = "─" * W

    print()
    print("═" * W)
    print(f"  {title}")
    print("═" * W)
    print(f"  {'#':>2}  {'Inicio':>5}  {'Fin':>5}  {'Dur':>6}  {'Tipo':<8}  Descripción")
    print(sep)

    total_mins = 0
    for i, e in enumerate(entries, 1):
        sl   = e["start_utc"] + OFS
        el   = e["end_utc"]   + OFS
        dur, mins = _fmt_dur(e["start_utc"], e["end_utc"])
        total_mins += mins
        tipo = "[AUTO]  " if e["source"] == "auto" else "[MANUAL]"
        desc = e["description"]
        if len(desc) > 36:
            desc = desc[:35] + "…"
        warn = "  ⚠" if e.get("warning") else ""
        print(f"  {i:>2}  {sl.strftime('%H:%M'):>5}  {el.strftime('%H:%M'):>5}  {dur:>6}  {tipo}  {desc}{warn}")

    print(sep)
    th, tm = int(total_mins) // 60, int(total_mins) % 60
    n = len(entries)
    print(f"  Total: {th}h {tm:02d}m  ({n} entrada{'s' if n != 1 else ''})")
    print("═" * W)


# ─── CLOCKIFY API ────────────────────────────────────────────────────────────

def check_blocked_window(start_utc, end_utc):
    OFS         = timedelta(hours=LOCAL_UTC_OFFSET)
    start_local = start_utc + OFS
    end_local   = end_utc   + OFS
    day_name    = WEEKDAY_NAMES[start_local.weekday()]
    for win in BLOCKED_WINDOWS:
        wd, sh, sm, eh, em = win
        if day_name != wd:
            continue
        ws = start_local.replace(hour=sh, minute=sm, second=0, microsecond=0)
        we = start_local.replace(hour=eh, minute=em, second=0, microsecond=0)
        if start_local < we and end_local > ws:
            return f"overlaps {wd} blocked window {sh:02d}:{sm:02d}-{eh:02d}:{em:02d}"
    return None


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
    uid = get_user_id()
    if not uid:
        return []
    day_start = datetime(target_d.year, target_d.month, target_d.day, tzinfo=timezone.utc)
    day_end   = day_start + timedelta(days=1)
    try:
        r = requests.get(
            f"{CLOCKIFY_URL}/workspaces/{CLOCKIFY_WORKSPACE}/user/{uid}/time-entries",
            headers={"X-Api-Key": CLOCKIFY_API_KEY},
            params={
                "start": day_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end":   day_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "page-size": 100,
            },
            timeout=10,
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []


def find_overlapping(start_utc, end_utc, existing):
    result = []
    for entry in existing:
        ti    = entry.get("timeInterval", {})
        s_raw = ti.get("start")
        e_raw = ti.get("end")
        if not s_raw or not e_raw:
            continue
        ei_s = datetime.fromisoformat(s_raw.replace("Z", "+00:00"))
        ei_e = datetime.fromisoformat(e_raw.replace("Z", "+00:00"))
        if ei_s < end_utc and ei_e > start_utc:
            result.append(entry)
    return result


def create_entry(start_utc, end_utc, description):
    r = requests.post(
        f"{CLOCKIFY_URL}/workspaces/{CLOCKIFY_WORKSPACE}/time-entries",
        headers={"X-Api-Key": CLOCKIFY_API_KEY, "Content-Type": "application/json"},
        json={
            "start":       start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end":         end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "description": description,
            "projectId":   CLOCKIFY_PROJECT,
            "billable":    True,
            "tagIds":      [],
        },
        timeout=10,
    )
    return r.status_code == 201, r.json()


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    args   = parse_args()
    target = target_date(args.yesterday, args.date)
    label  = args.date if args.date else ("yesterday" if args.yesterday else "today")

    print(f"\nClockify Daily Log — {target} ({label})")
    print("=" * 60)

    # 1. Load sessions
    sessions = load_messages_per_session(target)
    if not sessions:
        print(f"No Claude session messages found for {target}.")
        sys.exit(0)

    total_msgs = sum(len(m) for _, m in sessions)
    merged_blocks = merge_overlapping_blocks(sessions)
    print(f"Sessions: {len(sessions)} | Messages: {total_msgs} | Blocks: {len(merged_blocks)}")

    # 2. Pre-generate all descriptions
    print()
    auto_entries = []
    skipped_short = 0

    for i, (start_utc, end_utc, all_msgs) in enumerate(merged_blocks, 1):
        _, mins = _fmt_dur(start_utc, end_utc)
        if mins < MIN_BLOCK_MINUTES:
            skipped_short += 1
            continue
        print(f"  Describing block {i}/{len(merged_blocks)}...", end=" ", flush=True)
        desc = generate_description_multi(all_msgs, len(sessions))
        warn = check_blocked_window(start_utc, end_utc)
        print(f"OK")
        auto_entries.append({
            "start_utc":   start_utc,
            "end_utc":     end_utc,
            "description": desc,
            "source":      "auto",
            "warning":     warn,
        })

    if skipped_short:
        print(f"  ({skipped_short} block{'s' if skipped_short > 1 else ''} under {MIN_BLOCK_MINUTES} min — skipped)")

    # 3. Show detected sessions table
    if auto_entries:
        print_day_table(auto_entries, LOCAL_UTC_OFFSET, f"SESIONES DETECTADAS — {target}")
    else:
        print(f"\n  No blocks detected for {target}.")

    # 4. Ask for manual entries
    manual_entries = ask_manual_entries(target, LOCAL_UTC_OFFSET, dry_run=args.dry_run)

    # 5. Build complete entry list (sorted by start time)
    all_entries = sorted(auto_entries + manual_entries, key=lambda x: x["start_utc"])

    # 6. Show complete day table if there are manual entries
    if manual_entries:
        print_day_table(all_entries, LOCAL_UTC_OFFSET, f"PLAN COMPLETO DEL DÍA — {target}")
    elif not auto_entries:
        print("\nNothing to log.")
        sys.exit(0)

    # 7. Get existing Clockify entries for duplicate detection
    existing = get_existing_entries_for_day(target)

    # 8. Confirmation loop
    OFS     = timedelta(hours=LOCAL_UTC_OFFSET)
    created = 0
    skipped = 0
    total   = len(all_entries)

    print()
    print("─" * 60)
    print(f"  Confirmación — {total} entrada{'s' if total != 1 else ''}")
    print("─" * 60)

    for i, entry in enumerate(all_entries, 1):
        sl  = entry["start_utc"] + OFS
        el  = entry["end_utc"]   + OFS
        dur, _ = _fmt_dur(entry["start_utc"], entry["end_utc"])
        src = "[AUTO]  " if entry["source"] == "auto" else "[MANUAL]"

        print(f"\n  [{i}/{total}] {sl.strftime('%H:%M')}–{el.strftime('%H:%M')} {dur}  {src}")
        print(f"  \"{entry['description']}\"")

        if entry.get("warning"):
            print(f"  ⚠  {entry['warning']}")

        overlaps = find_overlapping(entry["start_utc"], entry["end_utc"], existing)
        if overlaps:
            print(f"  ⚠  DUPLICATE — {len(overlaps)} existing entr{'y' if len(overlaps)==1 else 'ies'} overlap:")
            for ov in overlaps:
                ti   = ov.get("timeInterval", {})
                ov_s = datetime.fromisoformat(ti["start"].replace("Z", "+00:00")) + OFS
                ov_e = datetime.fromisoformat(ti["end"].replace("Z", "+00:00"))   + OFS
                print(f"     • {ov_s.strftime('%H:%M')}–{ov_e.strftime('%H:%M')} '{ov.get('description','')[:55]}'")

        if args.dry_run:
            tag = " (DUPLICATE RISK)" if overlaps else ""
            print(f"  → [DRY RUN] Would create{tag}.")
            continue

        has_dup     = bool(overlaps)
        prompt_text = "  Create anyway? [y/n/e=edit]: " if has_dup else "  Create? [y/n/e=edit]: "
        try:
            confirm = input(prompt_text).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Aborted.")
            break

        if confirm == "e":
            try:
                new_desc = input("  New description: ").strip()
                if new_desc:
                    entry["description"] = new_desc
            except (EOFError, KeyboardInterrupt):
                pass
            confirm = "y"

        if confirm != "y":
            print("  Skipped.")
            skipped += 1
            continue

        ok, result = create_entry(entry["start_utc"], entry["end_utc"], entry["description"])
        if ok:
            print("  ✓ Created.")
            created += 1
        else:
            print(f"  ✗ Error: {str(result)[:80]}")
            skipped += 1

    # 9. Summary
    print()
    print("─" * 60)
    if args.dry_run:
        eligible = len(all_entries)
        print(f"  DRY RUN — {eligible} entr{'y' if eligible==1 else 'ies'} would be created.")
    else:
        print(f"  Done — {created} created, {skipped} skipped.")
    print()


if __name__ == "__main__":
    main()
