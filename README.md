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
