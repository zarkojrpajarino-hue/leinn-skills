# LEINN Skills

Skills para Claude Code del equipo LEINN / NOVA.
Convierten a Claude en un asistente experto en emprendimiento, pitches y metodología Lean Startup.

---

## Skills incluidas

| Skill | Qué hace | Invocar con |
|-------|----------|-------------|
| `pitch-to-deck` | Genera una one-pager HTML imprimible para cualquier proyecto. Pregunta todo: branding, datos, equipo, métricas. | `/pitch-to-deck` |
| `ries-lean-startup` | Carga los 10 frameworks de El método Lean Startup. Responde preguntas sobre MVP, pivot, métricas, motor de crecimiento. | `/ries-lean-startup` |
| `pitch-psychologist` | Estructura un pitch usando psicología de persuasión: construye deseo antes de presentar la solución. | `/pitch-psychologist` |
| `book-to-skill` | Convierte cualquier libro (PDF, EPUB, DOCX…) en una skill de Claude. El equipo puede cargar sus propios libros. | `/book-to-skill` |

## Agentes incluidos

| Agente | Qué hace | Cómo usar |
|--------|----------|-----------|
| `clockify-agent` | Registra automáticamente tu trabajo diario en Clockify leyendo tus sesiones de Claude Code. Genera descripciones con IA. | `python3 clockify_daily_log.py` |

---

## Instalación (5 minutos)

### Requisitos previos
- [Claude Code](https://claude.ai/download) instalado

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/zarkojrpajarino-hue/leinn-skills.git
```

Si no tienes git, descarga el ZIP desde GitHub → botón verde "Code" → "Download ZIP".

### Paso 2 — Copiar las skills

**Windows:**
```powershell
# Crear la carpeta de skills si no existe
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"

# Copiar todas las skills
Copy-Item -Recurse -Force "leinn-skills\pitch-to-deck"    "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse -Force "leinn-skills\ries-lean-startup" "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse -Force "leinn-skills\pitch-psychologist" "$env:USERPROFILE\.claude\skills\"
```

**Mac / Linux:**
```bash
mkdir -p ~/.claude/skills
cp -r leinn-skills/pitch-to-deck ~/.claude/skills/
cp -r leinn-skills/ries-lean-startup ~/.claude/skills/
cp -r leinn-skills/pitch-psychologist ~/.claude/skills/
```

### Paso 3 — Verificar

Abre Claude Code y escribe `/pitch-to-deck`. Si aparece la skill, todo está listo.

---

## Cómo usar cada skill

### `/pitch-to-deck` — One-pager de tu proyecto

Invoca la skill y responde las preguntas en un solo mensaje:
- Nombre y tagline del proyecto
- El problema que resuelve y tu solución
- Cómo funciona (3 pasos)
- Métricas reales (ventas, usuarios, etc.)
- Branding: colores, tipografía
- Ruta donde guardar el archivo

El resultado es un archivo HTML que abres en Chrome y puedes imprimir como PDF.

```
/pitch-to-deck
```

---

### `/ries-lean-startup` — Frameworks del libro

Carga los 10 frameworks de Eric Ries. Puedes preguntarle:

```
/ries-lean-startup ¿Cuándo es el momento de pivotar?
```
```
/ries-lean-startup Tenemos 50 encuestas positivas pero nadie paga. ¿Pivotamos o seguimos?
```
```
/ries-lean-startup Explícame el motor de crecimiento viral
```

---

### `/pitch-psychologist` — Estructura tu pitch

Usa psicología de persuasión para ordenar tu pitch: primero el mundo del cliente, luego el deseo, luego la solución.

```
/pitch-psychologist [pega aquí el texto de tu proyecto]
```

Combina con `/pitch-to-deck` para convertir el pitch estructurado en una one-pager:
1. `/pitch-psychologist` → estructura el pitch
2. Pega el resultado en `/pitch-to-deck` → genera el HTML

---

### `/book-to-skill` — Carga cualquier libro como skill

Tienes un libro en PDF, EPUB o DOCX que quieres que Claude pueda usar como referencia.

```
/book-to-skill /ruta/al/libro.pdf nombre-skill
```

Ejemplo:
```
/book-to-skill /Users/ana/Downloads/zero-to-one.pdf zero-to-one
```

Claude extrae los frameworks, principios y técnicas del libro y crea una skill que puedes usar con `/zero-to-one`. El proceso tarda unos minutos según el tamaño del libro.

Una vez creada, la skill queda en `~/.claude/skills/zero-to-one/` y puedes añadirla a este repo con un Pull Request para que todo el equipo la tenga.

---

### `clockify-agent` — Time tracker automático

No necesitas instalar como skill de Claude. Es un script Python que corres al final del día.

**Setup (una sola vez):**
```bash
pip install requests
cd leinn-skills/clockify-agent
cp clockify_config.example.json clockify_config.json
# Edita clockify_config.json con tus keys (ver SKILL.md para instrucciones)
```

**Uso diario:**
```bash
python3 clockify_daily_log.py           # registrar hoy
python3 clockify_daily_log.py --dry-run # ver bloques sin crear nada
python3 clockify_daily_log.py --yesterday
```

Lee el `SKILL.md` dentro de la carpeta para saber dónde conseguir cada API key.

---

## Flujo recomendado para crear un pitch completo

1. `/pitch-psychologist` — estructura el pitch con el arco emocional correcto
2. `/pitch-to-deck` — convierte el pitch en una one-pager HTML imprimible

---

## Mantener las skills actualizadas

```bash
cd leinn-skills
git pull
# Volver a copiar al directorio de skills (mismo proceso que la instalación)
```

---

## Contribuir

Si creas una skill útil para el equipo, abre un Pull Request con tu `SKILL.md`.

Estructura mínima de una skill:
```
tu-skill/
  SKILL.md    ← instrucciones para Claude
```
