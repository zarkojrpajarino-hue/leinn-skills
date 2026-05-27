# Clockify Agent — Time Tracker Automático

Registra automáticamente tu trabajo diario en Clockify leyendo tus sesiones de Claude Code.
No necesitas escribir nada a mano: el agente agrupa el trabajo por bloques de tiempo,
genera una descripción honesta con IA, y crea las entradas.

---

## Qué hace exactamente

1. **Lee tus sesiones** — escanea los archivos JSONL de `~/.claude/projects/` del día
2. **Agrupa por bloques** — un gap de >30 min entre mensajes = nuevo bloque de trabajo
3. **Genera descripciones** — llama a Claude Haiku con el contexto del bloque → descripción ≤100 chars
   - Ejemplo: `optimus k, Phase 93 auth RLS JWT`
   - Ejemplo: `leinn pitch, one-pager HTML + book-to-skill setup`
4. **Crea entradas en Clockify** — con las timestamps reales de tu sesión
5. **Detecta duplicados** — antes de crear, comprueba si ya existe una entrada solapada
6. **Ventanas bloqueadas** — puedes definir franjas (ej: horas de clase) que no se registran

---

## Setup — 5 minutos

### 1. Instalar dependencia

```bash
pip install requests
```

### 2. Copiar la plantilla de configuración

```bash
# En la carpeta donde clonaste el repo
cp clockify_config.example.json clockify_config.json
```

### 3. Rellenar tus keys en `clockify_config.json`

```json
{
  "clockify_api_key": "...",
  "clockify_workspace": "...",
  "clockify_project": "...",
  "anthropic_api_key": "...",
  "anthropic_model": "claude-haiku-4-5-20251001",
  "utc_offset_hours": 2,
  "blocked_windows": [
    ["Monday", 14, 0, 17, 0],
    ["Wednesday", 10, 30, 16, 0]
  ]
}
```

**Dónde conseguir cada key:**

| Key | Dónde |
|-----|-------|
| `clockify_api_key` | clockify.me → Preferences → API → Generate |
| `clockify_workspace` | URL de Clockify: `clockify.me/workspaces/`**ESTE_ID** |
| `clockify_project` | clockify.me → Projects → click en tu proyecto → URL: `...projects/`**ESTE_ID** |
| `anthropic_api_key` | console.anthropic.com → API Keys |

**`utc_offset_hours`:** tu zona horaria (España = 2 en verano, 1 en invierno)

**`blocked_windows`:** franjas en las que NO quieres registrar trabajo (ej: horas de clase LEINN).
Formato: `["Weekday", hora_inicio, min_inicio, hora_fin, min_fin]`. Dejar `[]` si no necesitas.

---

## Uso

```bash
# Registrar hoy
python3 clockify_daily_log.py

# Registrar ayer
python3 clockify_daily_log.py --yesterday

# Ver qué bloques detectaría sin crear nada (recomendado la primera vez)
python3 clockify_daily_log.py --dry-run

# Fecha específica
python3 clockify_daily_log.py --date 2026-05-23
```

**Recomendado:** usa `--dry-run` la primera vez para ver qué detecta antes de crear entradas.

---

## Flujo interactivo

Para cada bloque detectado, el script pregunta:

```
Block 1/3: 09:15-11:42 local (2h 27m, 1 session(s))
  Generating description... -> 'leinn pitch, one-pager HTML brief'
  Create entry? [y/n/e=edit description]: y
  OK - Entry created!
```

- `y` → crear la entrada
- `n` → saltar este bloque
- `e` → editar la descripción antes de crear

---

## Ejemplo de output completo

```
Clockify Daily Log -- 2026-05-26 (today)
--------------------------------------------------
Sessions: 2 | Messages: 347
Merged time blocks: 3

Block 1/3: 09:15-11:42 local (2h 27m, 2 session(s))
  Generating description... -> 'optimus k, Phase 151 Operator mode + pitch deck'
  Create entry? [y/n/e=edit description]: y
  OK - Entry created!

Block 2/3: 14:05-14:22 local (0h 17m, 1 session(s))
  WARNING: overlaps Monday blocked window 14:00-17:00 local
  Generating description... -> 'leinn skills, clockify setup'
  [DUPLICATE] 1 existing entry overlaps this block:
    * 14:00-15:00 local: 'LEINN class'
  Create anyway? [y/n/e=edit]: n
  Skipped.

Block 3/3: 17:30-19:45 local (2h 15m, 1 session(s))
  Generating description... -> 'exp3rea, funnel pricing analysis'
  Create entry? [y/n/e=edit description]: y
  OK - Entry created!

--------------------------------------------------
Done. 2 entries created, 1 skipped.
```

---

## Preguntas frecuentes

**¿Cuesta dinero?**
Sí, una cantidad mínima. Cada bloque usa Claude Haiku (~$0.00025 por descripción). Un día normal con 5 bloques cuesta menos de $0.002.

**¿Qué pasa si tengo varias sesiones en paralelo?**
El script las fusiona: si dos sesiones se solapan en el tiempo, se cuentan como un único bloque de trabajo.

**¿Lee el contenido de mis conversaciones?**
Lee los primeros 150 caracteres de cada mensaje para generar la descripción. No almacena nada, no envía nada más allá de lo necesario para generar el título.

**¿Funciona en Mac/Linux?**
Sí. El path de sesiones se resuelve automáticamente con `Path.home()`.
