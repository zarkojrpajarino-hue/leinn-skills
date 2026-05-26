---
name: pitch-to-deck
description: "Genera una one-pager HTML imprimible para cualquier proyecto. Siempre una sola página. Pregunta todo lo necesario en UN mensaje (identidad, problema, solución, métricas reales, branding, equipo). Ideal para inversores, clientes, reuniones o equipos LEINN. Imprime desde Chrome como PDF."
allowed-tools:
  - Read
  - Write
argument-hint: [nombre del proyecto, o pegar texto de pitch existente]
---

# Pitch-to-Deck — One-Pager Generator

Genera una one-pager HTML profesional para cualquier proyecto.
**Siempre una sola página. Siempre imprimible. Siempre con datos reales.**

## Cuándo usar
- Para presentar un proyecto en una reunión y dejar algo tangible
- Para enviar un brief del producto antes de una call o reunión
- Para equipos LEINN que necesitan documentar su startup
- Para crear material de prospección que funcione solo, sin presentación en vivo

## Cuándo NO usar
- Presentaciones en vivo con público (usa Reveal.js o Canva)
- Documentos de más de 2 páginas (usa otro formato)

---

## Flujo — 4 pasos en orden

### PASO 1 — Extraer contexto previo (si existe)

Si el usuario tiene texto de un pitch, output de `/pitch-psychologist`, o cualquier descripción del proyecto:
→ Extraer nombre, problema, solución y métricas de ese texto
→ Pre-rellenar las respuestas del PASO 2 donde sea posible
→ Preguntar SOLO lo que falta

Si no hay texto previo → ir directo al PASO 2.

---

### PASO 2 — Recopilar toda la información (UN solo mensaje)

Enviar SIEMPRE las preguntas en UN único mensaje. Nunca fragmentar en mensajes separados.
Los campos marcados (*) son obligatorios. El resto mejora el resultado.

Usar este template exacto:

```
Para generar tu one-pager necesito esta información.
Los campos con (*) son obligatorios. El resto mejora el resultado.
Responde todo en un solo mensaje — cuanto más completo, mejor queda.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A — IDENTIDAD (*)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Nombre del proyecto: (ej: EXP3REA, Optimus-K, NovaTech)
2. Tagline (*): máximo 10 palabras — qué es y para quién
   Ej: "Bootcamp de emprendimiento para jóvenes de 9 a 16 años"
3. Tu nombre y rol (*): (ej: Zarko — Fundador)
4. Email de contacto: (aparece en el footer)
5. Mes y año: (ej: Mayo 2026)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
B — PROBLEMA Y SOLUCIÓN (*)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. El problema — 3 puntos cortos (1 frase cada uno):
   - Problema 1:
   - Problema 2:
   - Problema 3:
7. Tu solución — 3 puntos cortos (1 frase cada uno):
   - Solución 1:
   - Solución 2:
   - Solución 3:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
C — CÓMO FUNCIONA (*)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Los 3 pasos de tu proceso o producto (título + descripción en 1 frase):
8. Paso 1 — Título: / Descripción:
9. Paso 2 — Título: / Descripción:
10. Paso 3 — Título: / Descripción:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
D — MÉTRICAS REALES (*)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Solo números que ya tienes. NUNCA inventar ni poner estimaciones.
Si no tienes métricas todavía, escribe "sin métricas" y se omite la sección.
Formato: Label | Valor | Descripción breve
Ej: Ventas | €19.506 | Histórico validado
    Ediciones | 4 | En 2 años de operación
11. Métrica 1: Label | Valor | Descripción
12. Métrica 2: Label | Valor | Descripción
13. Métrica 3 (opcional): ...
14. Métrica 4 (opcional): ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
E — PARA QUIÉN (recomendado)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hasta 3 perfiles de cliente o audiencia. Formato: emoji | nombre | descripción 1 frase
Ej: 🎓 | Familias LEINN | Equipos que necesitan gestionar su startup con datos reales
15. Perfil 1:
16. Perfil 2 (opcional):
17. Perfil 3 (opcional):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
F — BRANDING (*)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
18. Color principal (hex) (*): el color más representativo de tu marca
    Ej: #f97316 (naranja), #5CE1E6 (cyan), #FF66C4 (rosa)
    Si no tienes → escribe "sin preferencia"
19. Color secundario (hex): segundo color de marca
    Si no tienes → escribe "sin preferencia"
20. Color acento (hex): para highlights y badges
    Si no tienes → escribe "sin preferencia"
21. Logo o emoji: URL de imagen, emoji (🚀), o solo el nombre en texto
22. Tipografía: Google Fonts, ej "Archivo Black + Inter"
    Si no tienes → escribe "sin preferencia"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
G — GUARDAR EN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
23. Ruta completa donde guardar el archivo:
    Ej (Windows): C:\Users\TuNombre\Downloads\
    Ej (Mac): /Users/tunombre/Desktop/
    Si no especificas → se guarda en C:\Users\Zarko\Downloads\
```

---

### PASO 3 — Generar la one-pager HTML

Aplicar estas reglas antes de generar:

**Colores:**
- Si el usuario dice "sin preferencia" → usar paleta por defecto: `#6366f1` principal, `#0891b2` secundario, `#f97316` acento
- Para cada color principal, computar su tint (fondo claro) y borde:
  - Hex dado → tint ≈ color al 8-10% de opacidad sobre blanco → convertir a hex
  - Alternativa rápida: para `#RRGGBB` → card = rgb(R,G,B) con `background: rgba(R,G,B,0.07)`, border = `rgba(R,G,B,0.25)`
  - O usar la tabla de referencia al final de esta skill

**Tipografía:**
- "sin preferencia" → Archivo Black (títulos) + Inter (cuerpo)
- Si especifica una sola fuente → usarla para ambos roles
- Siempre cargar desde Google Fonts

**Secciones dinámicas:**
- Métricas: incluir SOLO si el usuario proporcionó números reales. Si dijo "sin métricas" → omitir la sección entera
- Para quién: incluir solo si proporcionó al menos 1 perfil
- Email en footer: incluir solo si fue proporcionado

**KPI grid dinámico según cantidad de métricas:**
- 2 métricas → `grid-template-columns: 1fr 1fr`
- 3 métricas → `grid-template-columns: 1fr 1fr 1fr`
- 4 métricas → `grid-template-columns: 1fr 1fr 1fr 1fr`
- 5-6 métricas → `grid-template-columns: repeat(3, 1fr)` en 2 filas

**Colores de KPI boxes** (usar en orden, rotar si hay más):
1. --primary (color principal)
2. --secondary (color secundario)
3. --accent (color acento)
4. #059669 (verde)

**Reglas de contenido:**
- Solo datos reales proporcionados por el usuario — nunca inventar ni completar
- Tagline ≤ 10 palabras — recortar si excede
- Textos de problema/solución: máximo 1 frase por bullet
- Nombres de archivo: `[nombre-proyecto]-brief-[mes][año].html` (todo minúsculas, sin espacios)

---

### PASO 4 — Guardar y confirmar

Guardar en la ruta indicada con el nombre correcto.

Mensaje al usuario al terminar:
> ✅ **[nombre]-brief-[mes][año].html** guardado en `[ruta]`
>
> **Para abrir:** doble clic en el archivo → Chrome
> **Para PDF:** Ctrl+P (Cmd+P en Mac) → Guardar como PDF → Desactivar "Encabezados y pies de página"
> **Para compartir:** envía el archivo .html por email o Slack

---

## Plantilla HTML — one-pager completa

Usar esta plantilla. Sustituir TODAS las variables `[VARIABLE]`.

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[NOMBRE] — Product Brief</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=[FONT_TITULO_ENCODED]&family=[FONT_CUERPO_ENCODED]:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --primary:    [COLOR_PRINCIPAL];
  --secondary:  [COLOR_SECUNDARIO];
  --accent:     [COLOR_ACENTO];
  --text:       #0f172a;
  --muted:      #64748b;
  --light:      #334155;
  --red:        #dc2626;
  --green:      #059669;
  /* Tints derivados del branding — computar al generar */
  --p-card:     [COLOR_PRINCIPAL_TINT];
  --p-border:   [COLOR_PRINCIPAL_BORDER];
  --s-card:     [COLOR_SECUNDARIO_TINT];
  --s-border:   [COLOR_SECUNDARIO_BORDER];
  --a-card:     [COLOR_ACENTO_TINT];
  --a-border:   [COLOR_ACENTO_BORDER];
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0 }

body {
  font-family: '[FONT_CUERPO]', sans-serif;
  background: #f8fafc;
  color: var(--text);
  padding: 32px 24px;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page {
  max-width: 900px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 32px rgba(0,0,0,.08);
}

/* BARRA SUPERIOR */
.topbar {
  height: 5px;
  background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
}

/* HEADER */
.header {
  padding: 32px 48px 28px;
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: start;
  gap: 24px;
  border-bottom: 1px solid #f1f5f9;
}
.product-name {
  font-family: '[FONT_TITULO]', sans-serif;
  font-size: 2.8rem;
  text-transform: uppercase;
  line-height: 1;
  letter-spacing: -1px;
  margin-bottom: 8px;
}
.product-tagline {
  font-size: 13px;
  color: var(--muted);
  max-width: 420px;
  line-height: 1.55;
  margin-bottom: 16px;
}
.chips { display: flex; gap: 8px; flex-wrap: wrap }
.chip {
  font-size: 10px; font-weight: 600; letter-spacing: .5px;
  padding: 4px 12px; border-radius: 20px; border: 1px solid;
}
.chip-p { border-color: var(--p-border); color: var(--primary); background: var(--p-card) }
.chip-s { border-color: var(--s-border); color: var(--secondary); background: var(--s-card) }
.chip-a { border-color: var(--a-border); color: var(--accent); background: var(--a-card) }

.header-meta {
  text-align: right;
  font-size: 11px;
  color: #94a3b8;
  line-height: 1.9;
}
.header-meta strong { color: #475569 }
.demo-badge {
  display: inline-block;
  font-size: 10px; background: var(--p-card);
  border: 1px solid var(--p-border); border-radius: 4px;
  padding: 2px 8px; color: var(--primary);
}

/* CUERPO */
.body { padding: 0 48px }

.section {
  padding: 22px 0;
  border-bottom: 1px solid #f1f5f9;
}
.section:last-child { border-bottom: none }

.section-label {
  font-size: 9px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 3px;
  color: var(--secondary); margin-bottom: 14px;
}
.section-label.accent  { color: var(--accent) }
.section-label.primary { color: var(--primary) }
.section-label.neutral { color: #94a3b8 }

/* PROBLEMA / SOLUCIÓN */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px }

.prob-col, .sol-col {
  padding: 16px 18px; border-radius: 10px; border: 1px solid;
}
.prob-col { background: #fff7ed; border-color: #fed7aa }
.sol-col  { background: var(--p-card); border-color: var(--p-border) }

.col-title {
  font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;
}
.prob-col .col-title { color: #c2410c }
.sol-col  .col-title { color: var(--primary) }

.bullet-list { list-style: none }
.bullet-list li {
  font-size: 12px; color: var(--light);
  line-height: 1.55; padding: 4px 0;
  display: flex; align-items: flex-start; gap: 8px;
}
.bullet-list li::before { content: '—'; flex-shrink: 0; font-weight: 600; margin-top: 1px }
.prob-col .bullet-list li::before { color: #dc2626 }
.sol-col  .bullet-list li::before { color: var(--primary) }

/* KPI GRID */
.kpi-grid { display: grid; gap: 12px }
.kpi-cols-2 { grid-template-columns: 1fr 1fr }
.kpi-cols-3 { grid-template-columns: 1fr 1fr 1fr }
.kpi-cols-4 { grid-template-columns: 1fr 1fr 1fr 1fr }

.kpi {
  padding: 14px 16px; border-radius: 10px;
  border: 1px solid; position: relative; overflow: hidden;
}
.kpi::before {
  content: ''; position: absolute;
  top: 0; left: 0; right: 0; height: 3px;
}
.kpi-p  { background: var(--p-card); border-color: var(--p-border) }
.kpi-p::before  { background: var(--primary) }
.kpi-s  { background: var(--s-card); border-color: var(--s-border) }
.kpi-s::before  { background: var(--secondary) }
.kpi-a  { background: var(--a-card); border-color: var(--a-border) }
.kpi-a::before  { background: var(--accent) }
.kpi-g  { background: #f0fdf4; border-color: #86efac }
.kpi-g::before  { background: var(--green) }

.kpi-label  { font-size: 9px; text-transform: uppercase; letter-spacing: 1.5px; color: #94a3b8; margin-bottom: 4px }
.kpi-value  { font-family: '[FONT_TITULO]', sans-serif; font-size: 1.8rem; line-height: 1; margin-bottom: 4px }
.kpi-p .kpi-value  { color: var(--primary) }
.kpi-s .kpi-value  { color: var(--secondary) }
.kpi-a .kpi-value  { color: var(--accent) }
.kpi-g .kpi-value  { color: var(--green) }
.kpi-desc   { font-size: 10px; color: #94a3b8; line-height: 1.4 }

/* PASOS */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px }
.step {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 14px 16px; border-radius: 10px;
  background: #f8fafc; border: 1px solid #e2e8f0;
}
.step-num {
  width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: '[FONT_TITULO]', sans-serif; font-size: 11px;
  color: #fff;
  background: linear-gradient(135deg, var(--secondary), var(--accent));
}
.step-title { font-size: 12px; font-weight: 700; color: var(--text); margin-bottom: 3px }
.step-body  { font-size: 11px; color: var(--muted); line-height: 1.5 }

/* AUDIENCIA */
.audience-grid { display: grid; gap: 12px }
.audience-cols-1 { grid-template-columns: 1fr }
.audience-cols-2 { grid-template-columns: 1fr 1fr }
.audience-cols-3 { grid-template-columns: 1fr 1fr 1fr }

.audience-card {
  padding: 14px 16px; border-radius: 10px;
  border: 1px solid #e2e8f0; background: #f8fafc;
}
.audience-icon  { font-size: 20px; margin-bottom: 6px }
.audience-title { font-size: 12px; font-weight: 700; color: var(--text); margin-bottom: 4px }
.audience-desc  { font-size: 11px; color: var(--muted); line-height: 1.5 }

/* EQUIPO (opcional) */
.team-row { display: flex; align-items: center; gap: 12px; margin-bottom: 8px }
.team-avatar {
  width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: '[FONT_TITULO]', sans-serif; font-size: 14px; color: #fff;
  background: linear-gradient(135deg, var(--primary), var(--accent));
}
.team-name { font-size: 13px; font-weight: 600; color: var(--text) }
.team-role { font-size: 11px; color: var(--muted) }

/* FOOTER CTA */
.footer-cta {
  padding: 24px 48px;
  background: #0f172a;
  display: flex; align-items: center;
  justify-content: space-between; gap: 24px;
}
.cta-question {
  font-family: '[FONT_TITULO]', sans-serif;
  font-size: 1rem; text-transform: uppercase;
  color: #fff; line-height: 1.3;
}
.cta-question span { color: var(--primary) }
.cta-contact {
  text-align: right; font-size: 11px;
  color: #94a3b8; line-height: 1.9; flex-shrink: 0;
}
.cta-contact strong { color: #e2e8f0 }
.live-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--primary); display: inline-block;
  margin-right: 5px;
  animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

/* PRINT */
@media print {
  body { background: #fff; padding: 0 }
  .page { box-shadow: none; border-radius: 0; max-width: 100% }
  @page { margin: 1cm; size: A4 }
}
</style>
</head>
<body>
<div class="page">

  <div class="topbar"></div>

  <!-- HEADER -->
  <div class="header">
    <div>
      <div class="product-name">[NOMBRE]</div>
      <div class="product-tagline">[TAGLINE]</div>
      <div class="chips">
        <span class="chip chip-p">[CHIP_1]</span>
        <span class="chip chip-s">[CHIP_2]</span>
        <span class="chip chip-a">[CHIP_3]</span>
      </div>
    </div>
    <div class="header-meta">
      <strong>[NOMBRE_FUNDADOR]</strong><br>
      [ROL]<br>
      [MES_AÑO]<br><br>
      <span class="demo-badge">Demo disponible</span>
    </div>
  </div>

  <div class="body">

    <!-- PROBLEMA / SOLUCIÓN -->
    <div class="section">
      <div class="section-label">El problema y la solución</div>
      <div class="two-col">
        <div class="prob-col">
          <div class="col-title">❌ Hoy: [TÍTULO_PROBLEMA]</div>
          <ul class="bullet-list">
            <li>[PROBLEMA_1]</li>
            <li>[PROBLEMA_2]</li>
            <li>[PROBLEMA_3]</li>
          </ul>
        </div>
        <div class="sol-col">
          <div class="col-title">✅ Con [NOMBRE]: [TÍTULO_SOLUCIÓN]</div>
          <ul class="bullet-list">
            <li>[SOLUCIÓN_1]</li>
            <li>[SOLUCIÓN_2]</li>
            <li>[SOLUCIÓN_3]</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- MÉTRICAS — solo si hay datos reales -->
    <!-- OMITIR esta sección si el usuario dijo "sin métricas" -->
    <div class="section">
      <div class="section-label primary">Tracción real — números de producción</div>
      <div class="kpi-grid [KPI_COLS_CLASS]">
        <div class="kpi kpi-p">
          <div class="kpi-label">[KPI_1_LABEL]</div>
          <div class="kpi-value">[KPI_1_VALOR]</div>
          <div class="kpi-desc">[KPI_1_DESC]</div>
        </div>
        <div class="kpi kpi-s">
          <div class="kpi-label">[KPI_2_LABEL]</div>
          <div class="kpi-value">[KPI_2_VALOR]</div>
          <div class="kpi-desc">[KPI_2_DESC]</div>
        </div>
        <!-- Repetir para cada KPI adicional con clases kpi-a, kpi-g, kpi-p, kpi-s en orden -->
      </div>
    </div>

    <!-- CÓMO FUNCIONA -->
    <div class="section">
      <div class="section-label accent">Cómo funciona</div>
      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <div>
            <div class="step-title">[PASO_1_TITULO]</div>
            <div class="step-body">[PASO_1_DESC]</div>
          </div>
        </div>
        <div class="step">
          <div class="step-num">2</div>
          <div>
            <div class="step-title">[PASO_2_TITULO]</div>
            <div class="step-body">[PASO_2_DESC]</div>
          </div>
        </div>
        <div class="step">
          <div class="step-num">3</div>
          <div>
            <div class="step-title">[PASO_3_TITULO]</div>
            <div class="step-body">[PASO_3_DESC]</div>
          </div>
        </div>
      </div>
    </div>

    <!-- PARA QUIÉN — solo si se proporcionaron perfiles -->
    <!-- OMITIR esta sección completa si no hay perfiles -->
    <div class="section">
      <div class="section-label neutral">Para quién</div>
      <div class="audience-grid [AUDIENCE_COLS_CLASS]">
        <div class="audience-card">
          <div class="audience-icon">[PERFIL_1_EMOJI]</div>
          <div class="audience-title">[PERFIL_1_NOMBRE]</div>
          <div class="audience-desc">[PERFIL_1_DESC]</div>
        </div>
        <!-- Repetir para cada perfil adicional -->
      </div>
    </div>

    <!-- EQUIPO — sección mínima siempre presente -->
    <div class="section">
      <div class="section-label neutral">Quién hay detrás</div>
      <div class="team-row">
        <div class="team-avatar">[INICIAL_NOMBRE]</div>
        <div>
          <div class="team-name">[NOMBRE_FUNDADOR]</div>
          <div class="team-role">[ROL]</div>
        </div>
      </div>
    </div>

  </div><!-- /body -->

  <!-- FOOTER CTA -->
  <div class="footer-cta">
    <div class="cta-question">
      [CTA_LÍNEA_1]<br>
      <span>[CTA_LÍNEA_2_ACENTO]</span><br>
      [CTA_LÍNEA_3]?
    </div>
    <div class="cta-contact">
      <span class="live-dot"></span><strong>Demo disponible</strong><br>
      [NOMBRE_FUNDADOR]<br>
      <!-- Incluir solo si se proporcionó email -->
      [EMAIL_CONTACTO]<br>
      <span style="font-size:10px;color:#475569">[MES_AÑO]</span>
    </div>
  </div>

</div><!-- /page -->
</body>
</html>
```

---

## Referencia de variables

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `[NOMBRE]` | Nombre del proyecto | EXP3REA |
| `[TAGLINE]` | Tagline ≤10 palabras | Bootcamp de emprendimiento para jóvenes |
| `[NOMBRE_FUNDADOR]` | Nombre del fundador | Zarko |
| `[ROL]` | Rol del fundador | Fundador & CEO |
| `[MES_AÑO]` | Fecha | Mayo 2026 |
| `[EMAIL_CONTACTO]` | Email (si se proporcionó) | hola@proyecto.com |
| `[CHIP_1..3]` | Datos clave para el header | 🚀 En producción |
| `[COLOR_PRINCIPAL]` | Hex del color principal | #f97316 |
| `[COLOR_PRINCIPAL_TINT]` | Fondo claro derivado del principal | #fff7ed |
| `[COLOR_PRINCIPAL_BORDER]` | Borde claro derivado del principal | #fed7aa |
| `[FONT_TITULO]` | Nombre exacto de la fuente título | Archivo Black |
| `[FONT_TITULO_ENCODED]` | Fuente título para Google Fonts URL | Archivo+Black |
| `[FONT_CUERPO]` | Nombre exacto de la fuente cuerpo | Inter |
| `[FONT_CUERPO_ENCODED]` | Fuente cuerpo para Google Fonts URL | Inter |
| `[KPI_COLS_CLASS]` | Clase CSS para el grid de KPIs | kpi-cols-3 |
| `[AUDIENCE_COLS_CLASS]` | Clase CSS para audiencia | audience-cols-2 |
| `[INICIAL_NOMBRE]` | Primera letra del nombre fundador | Z |
| `[CTA_LÍNEA_1..3]` | Pregunta de cierre dividida en 3 líneas | ¿Quieres ver |

---

## Tabla de tints por color

Para derivar `--p-card` y `--p-border` desde el color principal:

| Color principal | Tint (card bg) | Border |
|----------------|----------------|--------|
| `#f97316` naranja | `#fff7ed` | `#fed7aa` |
| `#5CE1E6` cyan   | `#f0fdfe` | `#a5f3fc` |
| `#FF66C4` rosa   | `#fff0f7` | `#fbb6df` |
| `#7C3AED` violeta | `#f5f0ff` | `#c4b5fd` |
| `#0891b2` azul   | `#ecfeff` | `#a5f3fc` |
| `#059669` verde  | `#f0fdf4` | `#86efac` |
| `#dc2626` rojo   | `#fef2f2` | `#fecaca` |
| `#6366f1` índigo | `#eef2ff` | `#c7d2fe` |
| `#d97706` ámbar  | `#fffbeb` | `#fde68a` |
| `#ec4899` fucsia | `#fdf2f8` | `#f9a8d4` |

Para colores no listados: usar `rgba([R],[G],[B], 0.07)` para card y `rgba([R],[G],[B], 0.25)` para border.

---

## Reglas de calidad — verificar antes de guardar

- [ ] Ningún número es inventado ni estimado — solo datos reales del usuario
- [ ] La sección Métricas está AUSENTE si el usuario dijo "sin métricas"
- [ ] La sección Para quién está AUSENTE si no se proporcionaron perfiles
- [ ] Tagline ≤ 10 palabras
- [ ] El CTA es una pregunta específica, no "Gracias" ni "Contacta con nosotros"
- [ ] Nombre de archivo: `[proyecto]-brief-[mesaño].html` (minúsculas, sin espacios)
- [ ] Todas las variables `[VARIABLE]` están sustituidas — ninguna en el HTML final
- [ ] CSS incluye `@media print` para impresión desde Chrome
