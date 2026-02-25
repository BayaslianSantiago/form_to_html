"""
╔══════════════════════════════════════════════════════════════╗
║   GENERADOR DE TPs Y RESÚMENES — DERECHO CIVIL               ║
║   Streamlit App  · UBA                                       ║
╚══════════════════════════════════════════════════════════════╝

Instalación (una sola vez):
    pip install streamlit

Uso:
    streamlit run generador_tp_streamlit.py

────────────────────────────────────────────────────────────────
SINTAXIS PARA EL MODO RESUMEN
────────────────────────────────────────────────────────────────
TITULO:    Texto del título principal de sección
SUBTITULO: Texto del subtítulo (h3 con borde burdeos)
TEXTO:     Párrafo normal
DEF:       Definición destacada en cuadro resumen
TABLA:     Encabezado col1 | col2 | col3
           fila1 col1 | fila1 col2 | fila1 col3
           fila2 col1 | fila2 col2 | fila2 col3
           ---   (línea de cierre de tabla)
EJ:        Texto de ejemplo (callout ocre)
NOTA:      Nota importante (callout azul)
- texto    Ítem de lista con guion
1. texto   Ítem de lista numerada
SALTO:     (línea en blanco — separador visual)
────────────────────────────────────────────────────────────────
"""

import html
import re
import streamlit as st
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════
#  CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Generador · Derecho Civil",
    page_icon="⚖️",
    layout="wide",
)

st.markdown("""
<style>
    section[data-testid="stSidebar"] { background: #1e1a1a; }
    section[data-testid="stSidebar"] * { color: #e8d8d8 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #d9a0a0 !important; }

    h1 { color: #8b1a1a !important; font-family: Georgia, serif !important; }
    h2 { color: #5a1010 !important; font-family: Georgia, serif !important;
         border-bottom: 1.5px solid #c8b8b8; padding-bottom: 4px; }
    h3 { color: #3a3a3a !important; font-family: Georgia, serif !important; }

    .caso-box {
        background: #f2efe9; border-left: 4px solid #b3a070;
        border-radius: 4px; padding: 12px 16px; margin-bottom: 12px;
    }
    .badge-v { background:#e6f2ea; color:#2a6e3f; border-radius:3px;
               padding:1px 7px; font-size:12px; font-weight:700; }
    .badge-f { background:#faeaea; color:#8b1a1a; border-radius:3px;
               padding:1px 7px; font-size:12px; font-weight:700; }

    div[data-testid="stDownloadButton"] button {
        background: #8b1a1a !important; color: white !important;
        font-weight: 600; border-radius: 4px; border: none;
        padding: 10px 28px; font-size: 15px;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: #6a1010 !important;
    }
    .block-container { padding-top: 2rem; }

    /* Resaltar área de texto del resumen */
    .resumen-area textarea {
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        background: #1e1e2e !important;
        color: #cdd6f4 !important;
        border: 1px solid #8b1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CSS DEL HTML GENERADO (mismo estilo académico en ambos modos)
# ══════════════════════════════════════════════════════════════

HTML_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond'
    ':ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Cormorant+'
    'Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap" rel="stylesheet">'
)

HTML_CSS = """<style>
:root {
    --ink:#1a1a1a; --ink-light:#3a3a3a; --ink-muted:#666;
    --accent:#8b1a1a; --accent-bg:#f9f2f2;
    --rule:#c8b8b8; --rule-light:#e8e0e0;
    --bg-page:#faf9f7; --bg-viewer:#4a4a4d;
    --case-bg:#f2efe9; --case-border:#b3a070;
}
* { box-sizing:border-box; margin:0; padding:0; }
body {
    background:var(--bg-viewer);
    font-family:'EB Garamond',Georgia,serif;
    color:var(--ink); padding:28px 0 56px;
    -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
.document {
    background:var(--bg-page); width:210mm; margin:0 auto;
    padding:16mm 22mm 18mm 22mm; box-shadow:0 4px 28px rgba(0,0,0,.5);
}
/* PORTADA */
.cover {
    display:grid; grid-template-columns:1fr auto;
    align-items:end; gap:0 16px;
    border-bottom:2px solid var(--accent);
    padding-bottom:8px; margin-bottom:14px;
}
.cover-left .eyebrow { font-size:7pt; text-transform:uppercase; letter-spacing:.18em; color:var(--ink-muted); margin-bottom:3px; }
.cover-left h1 { font-family:'Cormorant Garamond',serif; font-size:20pt; font-weight:600; line-height:1.15; color:var(--ink); }
.cover-left .subtitle { font-size:10.5pt; font-style:italic; color:var(--ink-light); margin-top:2px; }
.cover-right { text-align:right; font-size:9pt; color:var(--ink-muted); line-height:1.6; padding-bottom:2px; }
.cover-right strong { color:var(--ink); font-weight:600; font-size:10pt; }
.cover-right .label { font-size:7.5pt; text-transform:uppercase; letter-spacing:.1em; color:var(--ink-muted); }
/* SECCIÓN */
.section-header {
    display:flex; align-items:center; gap:8px;
    margin:14px 0 10px; padding-bottom:5px;
    border-bottom:1.5px solid var(--accent);
    page-break-after:avoid; break-after:avoid;
}
.section-num { font-family:'Cormorant Garamond',serif; font-size:22pt; font-weight:300; color:var(--accent); line-height:1; opacity:.55; min-width:26px; }
.section-title { font-family:'Cormorant Garamond',serif; font-size:13.5pt; font-weight:600; color:var(--ink); line-height:1.2; }
/* SUBTÍTULO */
h3 { font-family:'EB Garamond',serif; font-size:10.5pt; font-weight:700; color:var(--ink); border-left:2.5px solid var(--accent); padding-left:7px; margin:10px 0 4px; line-height:1.35; page-break-after:avoid; break-after:avoid; }
/* TEXTO */
p { font-size:10.5pt; line-height:1.55; text-align:justify; margin-bottom:4px; color:var(--ink-light); }
strong { font-weight:700; color:var(--ink); }
em { font-style:italic; }
/* LISTAS */
ul,ol { margin-bottom:5px; }
li { font-size:10.5pt; line-height:1.5; text-align:justify; margin-bottom:3px; color:var(--ink-light); }
ul { list-style:none; padding-left:0; }
ul>li { padding-left:14px; position:relative; }
ul>li::before { content:'—'; color:var(--accent); position:absolute; left:0; font-weight:700; }
ol { list-style:decimal; padding-left:1.3em; }
/* CALLOUTS */
.callout { background:#f5f0e8; border-left:3px solid #b8932a; border-radius:0 2px 2px 0; padding:5px 9px; margin:5px 0; font-size:10pt; font-style:italic; color:var(--ink-light); line-height:1.45; page-break-inside:avoid; break-inside:avoid; }
.callout::before { content:'Ej. '; font-weight:700; font-style:normal; color:#b8932a; }
.callout-note { background:#f0f4f8; border-left:3px solid #4a7ab5; border-radius:0 2px 2px 0; padding:5px 9px; margin:5px 0; font-size:10pt; color:var(--ink-light); line-height:1.45; page-break-inside:avoid; break-inside:avoid; }
.callout-note strong { color:#4a7ab5; }
/* CUADRO DEFINICIÓN */
.summary-box { border:.5px solid var(--rule); border-radius:2px; padding:6px 10px; margin:6px 0; background:white; page-break-inside:avoid; break-inside:avoid; }
.summary-box .box-title { font-size:7.5pt; text-transform:uppercase; letter-spacing:.1em; color:var(--accent); font-weight:700; margin-bottom:4px; border-bottom:.5px solid var(--rule-light); padding-bottom:2px; }
/* TABLAS */
.compare-table { width:100%; border-collapse:collapse; margin:6px 0 8px; font-size:9.5pt; page-break-inside:avoid; break-inside:avoid; }
.compare-table th { background:var(--accent); color:#fff; padding:4px 8px; text-align:left; font-weight:700; font-size:8.5pt; letter-spacing:.03em; }
.compare-table td { padding:3px 8px; border-bottom:.5px solid var(--rule-light); vertical-align:top; line-height:1.45; color:var(--ink-light); }
.compare-table tr:nth-child(even) td { background:#f5f2ef; }
.compare-table tr:last-child td { border-bottom:1px solid var(--rule); }
/* Q&A (TP) */
.case-block { margin:12px 0 8px; page-break-inside:avoid; break-inside:avoid; }
.case-prompt { display:grid; grid-template-columns:28px 1fr; gap:0 8px; background:var(--case-bg); border-left:3.5px solid var(--case-border); border-radius:0 3px 3px 0; padding:8px 10px 8px 0; margin-bottom:8px; }
.case-num { font-family:'Cormorant Garamond',serif; font-size:15pt; font-weight:600; color:var(--case-border); line-height:1.2; padding-left:10px; padding-top:1px; }
.case-text { font-size:10.5pt; font-style:italic; color:var(--ink-light); line-height:1.5; text-align:justify; }
.case-text p { margin:0; }
.qa-block { margin-bottom:7px; page-break-inside:avoid; break-inside:avoid; }
.q-label { display:inline-block; font-family:'Cormorant Garamond',serif; font-size:9pt; font-weight:600; color:#fff; background:var(--accent); border-radius:2px; padding:0 5px; margin-right:5px; vertical-align:middle; line-height:1.5; }
/* V/F */
.vf-block { margin-bottom:8px; page-break-inside:avoid; break-inside:avoid; display:grid; grid-template-columns:22px 1fr; gap:0 8px; align-items:start; }
.vf-letter { font-family:'Cormorant Garamond',serif; font-size:11pt; font-weight:600; color:var(--ink-muted); padding-top:2px; text-align:right; }
.vf-question { font-size:10.5pt; font-weight:600; color:var(--ink); margin-bottom:3px; line-height:1.4; }
.badge { display:inline-block; font-size:7.5pt; font-weight:700; letter-spacing:.08em; text-transform:uppercase; padding:1px 6px; border-radius:2px; margin-right:5px; vertical-align:middle; }
.badge-v { background:#e6f2ea; color:#2a6e3f; border:.5px solid #9ecfad; }
.badge-f { background:#faeaea; color:#8b1a1a; border:.5px solid #d9a0a0; }
.vf-justification { font-size:10.5pt; line-height:1.52; color:var(--ink-light); text-align:justify; margin:0; }
/* TEÓRICAS */
.teorica-block { margin-bottom:10px; page-break-inside:avoid; break-inside:avoid; }
.teorica-num { font-family:'Cormorant Garamond',serif; font-size:11pt; font-weight:600; color:var(--accent); margin-right:4px; }
/* DOS COLUMNAS */
.two-col { display:grid; grid-template-columns:1fr 1fr; gap:0 14px; }
.two-col>* { min-width:0; }
/* SEPARADOR */
.divider { border:none; border-top:.5px solid var(--rule-light); margin:10px 0; }
/* PIE */
.doc-footer { display:flex; justify-content:space-between; font-size:7.5pt; color:var(--ink-muted); border-top:.5px solid var(--rule-light); padding-top:4px; margin-top:16px; }
@media print {
    body { background:white; padding:0; }
    .document { box-shadow:none; width:100%; padding:0; background:white; }
    @page { size:A4; margin:16mm 20mm 18mm 20mm; }
    .doc-footer { display:none; }
    h3 { page-break-after:avoid; break-after:avoid; }
    p  { orphans:3; widows:3; }
    .qa-block,.case-prompt,.callout-note,.callout,.vf-block,
    .teorica-block,.summary-box,.compare-table { page-break-inside:avoid; break-inside:avoid; }
}
</style>"""

ROMANO = ["I","II","III","IV","V","VI","VII","VIII","IX","X",
          "XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX"]
LETRAS = list("abcdefghijklmnopqrstuvwxyz")

# ══════════════════════════════════════════════════════════════
#  HELPERS HTML COMUNES
# ══════════════════════════════════════════════════════════════

def e(t):
    return html.escape(str(t))

def parrafos(text):
    bloques = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    if not bloques:
        return f"<p>{e(text)}</p>"
    return "\n".join(
        "<p>" + "<br>".join(html.escape(l) for l in b.split("\n")) + "</p>"
        for b in bloques
    )

def html_portada(meta, modo="tp"):
    tipo_doc = "Trabajo Práctico" if modo == "tp" else "Resumen de Estudio"
    sub = f'<p class="subtitle">{e(meta["subtitulo"])}</p>' if meta.get("subtitulo") else ""
    return f"""
<div class="cover">
  <div class="cover-left">
    <p class="eyebrow">{tipo_doc} · {e(meta['materia'])}</p>
    <h1>{e(meta['titulo'])}</h1>{sub}
  </div>
  <div class="cover-right">
    <span class="label">Alumno/a</span><br>
    <strong>{e(meta['alumna'])}</strong><br>
    {e(meta['universidad'])}<br>
    {e(meta['facultad'])}
  </div>
</div>"""

def html_doc_completo(meta, cuerpo, modo="tp"):
    nombre = e(f"{meta['titulo']} — {meta['alumna']}")
    pie = f"""
<div class="doc-footer">
  <span>{e(meta['alumna'])} · {e(meta['universidad'])} · {e(meta['materia'])}</span>
  <span>{"Trabajo Práctico" if modo == "tp" else "Resumen"}</span>
</div>"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{nombre}</title>
  {HTML_FONTS}
  {HTML_CSS}
</head>
<body>
<div class="document">
  {html_portada(meta, modo)}
  {cuerpo}
  {pie}
</div>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════
#  MODO TP — generadores (igual que antes)
# ══════════════════════════════════════════════════════════════

def html_casos(casos):
    out = []
    for c in casos:
        pregs = c.get("preguntas", [])
        mitad = (len(pregs) + 1) // 2
        col1, col2 = pregs[:mitad], pregs[mitad:]
        def render_qa(lista):
            return "\n".join(f"""
<div class="qa-block">
  <h3><span class="q-label">{e(p['label'])}</span> {e(p['pregunta'])}</h3>
  {parrafos(p['respuesta'])}
</div>""" for p in lista)
        out.append(f"""
<div class="case-block">
  <div class="case-prompt">
    <span class="case-num">{c['num']}.</span>
    <div class="case-text">{parrafos(c['enunciado'])}</div>
  </div>
  <div class="two-col">
    <div>{render_qa(col1)}</div>
    <div>{render_qa(col2)}</div>
  </div>
</div>
<hr class="divider">""")
    return "\n".join(out).rstrip().removesuffix('<hr class="divider">')

def html_vf(items):
    mitad = (len(items) + 1) // 2
    col1, col2 = items[:mitad], items[mitad:]
    def render(lista):
        rows = []
        for it in lista:
            badge = 'badge-v">Verdadero' if it["verdadero"] else 'badge-f">Falso'
            rows.append(f"""
<div class="vf-block">
  <span class="vf-letter">{e(it['label'])}.</span>
  <div>
    <p class="vf-question"><span class="badge {badge}</span>{e(it['afirmacion'])}</p>
    <p class="vf-justification">{e(it['justificacion'])}</p>
  </div>
</div>""")
        return "\n".join(rows)
    return f'<div class="two-col"><div>{render(col1)}</div><div>{render(col2)}</div></div>'

def html_teoricas(items):
    return "\n".join(f"""
<div class="teorica-block">
  <h3><span class="teorica-num">{it['num']}.</span> {e(it['pregunta'])}</h3>
  {parrafos(it['respuesta'])}
</div>""" for it in items)

def generar_html_tp(meta, secciones):
    GEN = [html_casos, html_vf, html_teoricas]
    cuerpo = ""
    for i, sec in enumerate(secciones):
        roman  = ROMANO[i]
        cuerpo_sec = GEN[sec["tipo"]](sec["contenido"])
        if sec["tipo"] == 1:
            cuerpo += f"""
<div style="page-break-inside:avoid;break-inside:avoid;">
<div class="section-header">
  <span class="section-num">{roman}</span>
  <span class="section-title">{e(sec['titulo'])}</span>
</div>
{cuerpo_sec}
</div>"""
        else:
            cuerpo += f"""
<div class="section-header">
  <span class="section-num">{roman}</span>
  <span class="section-title">{e(sec['titulo'])}</span>
</div>
{cuerpo_sec}"""
    return html_doc_completo(meta, cuerpo, modo="tp")

# ══════════════════════════════════════════════════════════════
#  MODO RESUMEN — PARSER DE PALABRAS CLAVE
# ══════════════════════════════════════════════════════════════

# Regex para detectar palabras clave al inicio de línea
RE_KW = re.compile(
    r'^(TITULO|SUBTITULO|TEXTO|DEF|TABLA|EJ|NOTA|SALTO)\s*:\s*',
    re.IGNORECASE
)
RE_BULLET  = re.compile(r'^\s*-\s+')
RE_NUMLIST = re.compile(r'^\s*\d+\.\s+')
RE_PIPE    = re.compile(r'\s*\|\s*')

def parsear_resumen(texto_raw):
    """
    Convierte el texto con palabras clave en una lista de tokens:
    [{"tipo": "...", "contenido": "..."}]
    """
    lineas = texto_raw.split("\n")
    tokens = []
    i = 0

    # Acumular ítems de lista consecutivos
    lista_activa = None   # "ul" | "ol"
    lista_items  = []

    def cerrar_lista():
        nonlocal lista_activa, lista_items
        if lista_activa and lista_items:
            tokens.append({"tipo": lista_activa, "items": lista_items[:]})
        lista_activa = None
        lista_items  = []

    while i < len(lineas):
        linea = lineas[i]

        # ── Lista bullet ──────────────────────────────────────
        if RE_BULLET.match(linea):
            if lista_activa != "ul":
                cerrar_lista()
                lista_activa = "ul"
            lista_items.append(RE_BULLET.sub("", linea).strip())
            i += 1
            continue

        # ── Lista numerada ────────────────────────────────────
        if RE_NUMLIST.match(linea):
            if lista_activa != "ol":
                cerrar_lista()
                lista_activa = "ol"
            lista_items.append(RE_NUMLIST.sub("", linea).strip())
            i += 1
            continue

        # Cerrar lista si la línea no es un ítem
        cerrar_lista()

        # ── Línea vacía → ignorar ─────────────────────────────
        if not linea.strip():
            i += 1
            continue

        # ── Detectar palabra clave ────────────────────────────
        m = RE_KW.match(linea)
        if not m:
            # Línea sin palabra clave → párrafo normal
            tokens.append({"tipo": "texto", "contenido": linea.strip()})
            i += 1
            continue

        kw      = m.group(1).upper()
        resto   = linea[m.end():].strip()

        if kw == "TITULO":
            tokens.append({"tipo": "titulo", "contenido": resto})

        elif kw == "SUBTITULO":
            tokens.append({"tipo": "subtitulo", "contenido": resto})

        elif kw == "TEXTO":
            tokens.append({"tipo": "texto", "contenido": resto})

        elif kw == "DEF":
            tokens.append({"tipo": "def", "contenido": resto})

        elif kw == "EJ":
            tokens.append({"tipo": "ej", "contenido": resto})

        elif kw == "NOTA":
            tokens.append({"tipo": "nota", "contenido": resto})

        elif kw == "SALTO":
            tokens.append({"tipo": "salto"})

        elif kw == "TABLA":
            # La primera línea tras TABLA: es el encabezado
            # Las siguientes son filas hasta encontrar ---
            encabezado = [c.strip() for c in RE_PIPE.split(resto)] if resto else []
            filas = []
            i += 1
            while i < len(lineas):
                fila_raw = lineas[i].strip()
                if fila_raw == "---":
                    i += 1
                    break
                if fila_raw:
                    filas.append([c.strip() for c in RE_PIPE.split(fila_raw)])
                i += 1
            tokens.append({"tipo": "tabla", "encabezado": encabezado, "filas": filas})
            continue   # i ya fue incrementado dentro del while

        i += 1

    cerrar_lista()   # por si el texto termina con una lista
    return tokens

def tokens_a_html(tokens):
    """Convierte la lista de tokens en HTML."""
    out       = []
    sec_count = 0

    for tok in tokens:
        tipo = tok["tipo"]

        if tipo == "titulo":
            roman = ROMANO[sec_count] if sec_count < len(ROMANO) else "·"
            sec_count += 1
            out.append(f"""
<div class="section-header">
  <span class="section-num">{roman}</span>
  <span class="section-title">{e(tok['contenido'])}</span>
</div>""")

        elif tipo == "subtitulo":
            out.append(f"<h3>{e(tok['contenido'])}</h3>")

        elif tipo == "texto":
            out.append(f"<p>{e(tok['contenido'])}</p>")

        elif tipo == "def":
            # Separar título opcional: si hay " - " tomamos lo anterior como título
            partes = tok["contenido"].split(" - ", 1)
            if len(partes) == 2:
                box_title = partes[0].strip()
                box_body  = partes[1].strip()
            else:
                box_title = "Definición"
                box_body  = tok["contenido"]
            out.append(f"""
<div class="summary-box">
  <p class="box-title">{e(box_title)}</p>
  <p>{e(box_body)}</p>
</div>""")

        elif tipo == "ej":
            out.append(f'<div class="callout">{e(tok["contenido"])}</div>')

        elif tipo == "nota":
            out.append(f'<div class="callout-note"><strong>Nota:</strong> {e(tok["contenido"])}</div>')

        elif tipo == "salto":
            out.append('<hr class="divider">')

        elif tipo == "ul":
            items_html = "\n".join(f"<li>{e(it)}</li>" for it in tok["items"])
            out.append(f"<ul>{items_html}</ul>")

        elif tipo == "ol":
            items_html = "\n".join(f"<li>{e(it)}</li>" for it in tok["items"])
            out.append(f"<ol>{items_html}</ol>")

        elif tipo == "tabla":
            enc = tok["encabezado"]
            filas = tok["filas"]
            if not enc and not filas:
                continue
            ths = "".join(f"<th>{e(c)}</th>" for c in enc)
            trs = ""
            for fila in filas:
                tds = "".join(f"<td>{e(c)}</td>" for c in fila)
                trs += f"<tr>{tds}</tr>"
            out.append(f"""
<table class="compare-table">
  <thead><tr>{ths}</tr></thead>
  <tbody>{trs}</tbody>
</table>""")

    return "\n".join(out)

def generar_html_resumen(meta, texto_raw):
    tokens = parsear_resumen(texto_raw)
    cuerpo = tokens_a_html(tokens)
    return html_doc_completo(meta, cuerpo, modo="resumen")

# ══════════════════════════════════════════════════════════════
#  ESTADO DE SESIÓN
# ══════════════════════════════════════════════════════════════

if "secciones" not in st.session_state:
    st.session_state.secciones = []

# ══════════════════════════════════════════════════════════════
#  SIDEBAR — METADATOS (compartidos por ambos modos)
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ⚖️ Datos del documento")
    st.markdown("---")
    titulo      = st.text_input("Título",      value="...")
    subtitulo   = st.text_input("Subtítulo",   value="...")
    materia     = st.text_input("Materia",     value="...")
    alumna      = st.text_input("Alumno/a",    value="...")
    universidad = st.text_input("Universidad", value="Universidad de Buenos Aires")
    facultad    = st.text_input("Facultad",    value="Facultad de Derecho")

    meta = {
        "titulo": titulo, "subtitulo": subtitulo,
        "materia": materia, "alumna": alumna,
        "universidad": universidad, "facultad": facultad,
    }

    st.markdown("---")
    st.markdown("### 📥 Descarga")

    # El botón de descarga se llena desde cada pestaña
    if "html_para_descargar" in st.session_state and st.session_state.html_para_descargar:
        nombre_archivo = re.sub(r"[^\w\s-]", "", f"{alumna}_{titulo}").strip()
        nombre_archivo = re.sub(r"\s+", "_", nombre_archivo)[:50] + ".html"
        st.download_button(
            label="⬇️  Descargar HTML",
            data=st.session_state.html_para_descargar.encode("utf-8"),
            file_name=nombre_archivo,
            mime="text/html",
        )
        st.caption("Abrí en Chrome → Ctrl+P → Guardar como PDF → A4")
    else:
        st.info("Generá el documento primero.")

    st.markdown("---")
    st.markdown("**Sintaxis rápida (modo Resumen):**")
    st.code(
        "TITULO: Nombre de sección\n"
        "SUBTITULO: Nombre de subtítulo\n"
        "TEXTO: Párrafo normal\n"
        "DEF: Término - Definición\n"
        "TABLA: Col1 | Col2 | Col3\n"
        "       dato | dato | dato\n"
        "       ---\n"
        "EJ: Texto de ejemplo\n"
        "NOTA: Nota importante\n"
        "- ítem de lista\n"
        "1. ítem numerado\n"
        "SALTO:",
        language="text",
    )

# ══════════════════════════════════════════════════════════════
#  PESTAÑAS PRINCIPALES
# ══════════════════════════════════════════════════════════════

st.markdown("# ⚖️ Generador de Documentos Académicos")
st.markdown("*Espero puedas hacer uso de esta herramienta, lo hice para vos con mucho cariño*")
st.markdown("---")

tab_tp, tab_resumen = st.tabs(["📋  Trabajo Práctico", "📖  Resumen de Estudio"])

# ══════════════════════════════════════════════════════════════
#  PESTAÑA 1 — TRABAJO PRÁCTICO (igual que antes)
# ══════════════════════════════════════════════════════════════

with tab_tp:
    st.markdown("## Secciones del TP")

    TIPOS_SECCION = [
        "📋  Casos Prácticos",
        "✅  Verdadero o Falso",
        "📝  Preguntas Teóricas",
    ]

    col_tipo, col_titulo_sec, col_btn = st.columns([2, 3, 1])
    with col_tipo:
        tipo_nuevo = st.selectbox("Tipo", TIPOS_SECCION, label_visibility="collapsed")
    with col_titulo_sec:
        titulo_nuevo = st.text_input("Título sección", placeholder="Ej: Casos Prácticos", label_visibility="collapsed")
    with col_btn:
        if st.button("➕ Agregar", use_container_width=True, key="btn_add_sec"):
            if titulo_nuevo.strip():
                idx = TIPOS_SECCION.index(tipo_nuevo)
                st.session_state.secciones.append({
                    "tipo": idx, "titulo": titulo_nuevo.strip(), "contenido": [],
                })
                st.rerun()
            else:
                st.error("Escribí un título.")

    st.markdown("")

    for sec_i, sec in enumerate(st.session_state.secciones):
        roman = ROMANO[sec_i]
        tipo  = sec["tipo"]
        icono = ["📋","✅","📝"][tipo]

        with st.expander(f"{icono}  **{roman}. {sec['titulo']}**", expanded=True):
            _, col_del = st.columns([6, 1])
            with col_del:
                if st.button("🗑️ Eliminar sección", key=f"del_sec_{sec_i}"):
                    st.session_state.secciones.pop(sec_i)
                    st.rerun()

            # ── CASOS ────────────────────────────────────────
            if tipo == 0:
                for c_i, caso in enumerate(sec["contenido"]):
                    st.markdown(f'<div class="caso-box">', unsafe_allow_html=True)
                    st.markdown(f"**Caso {caso['num']}**")
                    caso["enunciado"] = st.text_area(
                        "Enunciado", value=caso["enunciado"],
                        key=f"caso_{sec_i}_{c_i}_enunc", height=80,
                    )
                    for p_i, preg in enumerate(caso["preguntas"]):
                        pcols = st.columns([0.4, 3, 3, 0.4])
                        with pcols[0]: st.markdown(f"**{preg['label'].upper()}.**")
                        with pcols[1]:
                            preg["pregunta"] = st.text_area(
                                "Pregunta", value=preg["pregunta"],
                                key=f"caso_{sec_i}_{c_i}_preg_{p_i}", height=68,
                                label_visibility="collapsed", placeholder="Pregunta...",
                            )
                        with pcols[2]:
                            preg["respuesta"] = st.text_area(
                                "Respuesta", value=preg["respuesta"],
                                key=f"caso_{sec_i}_{c_i}_resp_{p_i}", height=68,
                                label_visibility="collapsed", placeholder="Respuesta...",
                            )
                        with pcols[3]:
                            if st.button("✕", key=f"del_preg_{sec_i}_{c_i}_{p_i}"):
                                caso["preguntas"].pop(p_i)
                                for k, p in enumerate(caso["preguntas"]): p["label"] = LETRAS[k]
                                st.rerun()
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button(f"➕ Pregunta al caso {caso['num']}", key=f"add_preg_{sec_i}_{c_i}"):
                            caso["preguntas"].append({"label": LETRAS[len(caso["preguntas"])], "pregunta": "", "respuesta": ""})
                            st.rerun()
                    with bc2:
                        if st.button(f"🗑️ Eliminar caso {caso['num']}", key=f"del_caso_{sec_i}_{c_i}"):
                            sec["contenido"].pop(c_i)
                            for k, ca in enumerate(sec["contenido"]): ca["num"] = k + 1
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("")
                if st.button("➕ Nuevo caso", key=f"add_caso_{sec_i}"):
                    sec["contenido"].append({"num": len(sec["contenido"]) + 1, "enunciado": "", "preguntas": [{"label": "a", "pregunta": "", "respuesta": ""}]})
                    st.rerun()

            # ── V/F ──────────────────────────────────────────
            elif tipo == 1:
                for it_i, item in enumerate(sec["contenido"]):
                    icols = st.columns([0.3, 3, 1, 3, 0.4])
                    with icols[0]: st.markdown(f"**{item['label'].upper()}.**")
                    with icols[1]:
                        item["afirmacion"] = st.text_area(
                            "Afirmación", value=item["afirmacion"],
                            key=f"vf_{sec_i}_{it_i}_afirm", height=80,
                            label_visibility="collapsed", placeholder="Afirmación...",
                        )
                    with icols[2]:
                        ver = st.radio("V/F", ["Verdadero","Falso"],
                                       index=0 if item["verdadero"] else 1,
                                       key=f"vf_{sec_i}_{it_i}_ver",
                                       label_visibility="collapsed")
                        item["verdadero"] = (ver == "Verdadero")
                        badge = "badge-v" if item["verdadero"] else "badge-f"
                        st.markdown(f'<span class="{badge}">{ver}</span>', unsafe_allow_html=True)
                    with icols[3]:
                        item["justificacion"] = st.text_area(
                            "Justificación", value=item["justificacion"],
                            key=f"vf_{sec_i}_{it_i}_just", height=80,
                            label_visibility="collapsed", placeholder="Justificación...",
                        )
                    with icols[4]:
                        if st.button("✕", key=f"del_vf_{sec_i}_{it_i}"):
                            sec["contenido"].pop(it_i)
                            for k, it in enumerate(sec["contenido"]): it["label"] = LETRAS[k]
                            st.rerun()
                if st.button("➕ Agregar ítem V/F", key=f"add_vf_{sec_i}"):
                    sec["contenido"].append({"label": LETRAS[len(sec["contenido"])], "afirmacion": "", "verdadero": True, "justificacion": ""})
                    st.rerun()

            # ── TEÓRICAS ─────────────────────────────────────
            elif tipo == 2:
                for it_i, item in enumerate(sec["contenido"]):
                    tcols = st.columns([0.3, 3, 3, 0.4])
                    with tcols[0]: st.markdown(f"**{item['num']}.**")
                    with tcols[1]:
                        item["pregunta"] = st.text_area(
                            "Pregunta", value=item["pregunta"],
                            key=f"teo_{sec_i}_{it_i}_preg", height=80,
                            label_visibility="collapsed", placeholder="Pregunta...",
                        )
                    with tcols[2]:
                        item["respuesta"] = st.text_area(
                            "Respuesta", value=item["respuesta"],
                            key=f"teo_{sec_i}_{it_i}_resp", height=80,
                            label_visibility="collapsed", placeholder="Respuesta...",
                        )
                    with tcols[3]:
                        if st.button("✕", key=f"del_teo_{sec_i}_{it_i}"):
                            sec["contenido"].pop(it_i)
                            for k, it in enumerate(sec["contenido"]): it["num"] = k + 1
                            st.rerun()
                if st.button("➕ Agregar pregunta teórica", key=f"add_teo_{sec_i}"):
                    sec["contenido"].append({"num": len(sec["contenido"]) + 1, "pregunta": "", "respuesta": ""})
                    st.rerun()

    # Vista previa TP
    if st.session_state.secciones:
        st.markdown("---")
        st.markdown("## 👁️ Vista previa")
        html_tp = generar_html_tp(meta, st.session_state.secciones)
        st.session_state.html_para_descargar = html_tp
        components.html(html_tp, height=860, scrolling=True)

# ══════════════════════════════════════════════════════════════
#  PESTAÑA 2 — RESUMEN DE ESTUDIO
# ══════════════════════════════════════════════════════════════

EJEMPLO_RESUMEN = """\
TITULO: Hecho y Acto Jurídico

SUBTITULO: 1. Hecho Jurídico — Art. 257

TEXTO: Es cualquier acontecimiento que, conforme al ordenamiento jurídico, produce el nacimiento, modificación o extinción de relaciones o situaciones jurídicas.

TABLA: Tipo | Descripción | Ejemplo
       Natural | Sin intervención humana | Rayo que incendia casa asegurada
       Humano (Acto) | Realizado por el hombre | Celebración de un contrato
       Lícito | Conforme a la ley | Pago de una deuda
       Ilícito | Contrario a la ley | Daño por culpa o dolo
       ---

SUBTITULO: 2. Actos Voluntarios e Involuntarios — Arts. 260–261

TEXTO: Un acto es voluntario cuando se ejecuta con discernimiento, intención y libertad, y se manifiesta exteriormente.

DEF: Discernimiento - Aptitud para distinguir lo bueno de lo malo y apreciar las consecuencias de las acciones.

DEF: Intención - El querer realizar el acto concreto. Se afecta por el error o el dolo.

DEF: Libertad - Facultad de elegir sin coacciones. Se afecta por la violencia o intimidación.

NOTA: El acto involuntario carece de discernimiento: actos de quien está privado de razón, ilícitos de menores de 10 años, lícitos de menores de 13 años.

SUBTITULO: 3. Formas de Manifestación de la Voluntad — Art. 262

- Expresa: oral, escrita, por signos inequívocos o ejecución de un hecho material.
- Tácita (Art. 264): se infiere de conductas que permiten conocer la voluntad con certidumbre.
- Silencio (Art. 263): por regla general NO es manifestación de voluntad.

EJ: Consumir un producto en un comercio antes de pagarlo es manifestación tácita de voluntad.

SALTO:

TITULO: Vicios de la Voluntad

SUBTITULO: 1. El Error — Arts. 265 a 270

TEXTO: Falso conocimiento o ignorancia de la realidad. Afecta la intención. Para causar nulidad debe ser esencial y reconocible por el destinatario.

TABLA: Tipo de Error | Consecuencia | Norma
       Esencial y reconocible | Nulidad relativa | Art. 265
       De cálculo | Solo rectificación | Art. 268
       En la declaración | "Compro" por "alquilo" | Art. 270
       ---

NOTA: El acto subsiste si la otra parte ofrece ejecutarlo tal como lo entendió el errante (Art. 269).
"""

with tab_resumen:
    st.markdown("## Resumen de Estudio")
    st.markdown(
        "Pegá o escribí tu texto usando las **palabras clave** de la barra lateral. "
        "El documento se genera automáticamente con el estilo académico."
    )

    col_editor, col_ayuda = st.columns([3, 1])

    with col_ayuda:
        st.markdown("#### 🗒️ Referencia rápida")
        st.markdown("""
| Palabra clave | Resultado |
|---|---|
| `TITULO:` | Título de sección |
| `SUBTITULO:` | Subtítulo h3 |
| `TEXTO:` | Párrafo |
| `DEF: Término - ...` | Cuadro definición |
| `TABLA: col\|col` / `---` | Tabla comparativa |
| `EJ:` | Callout ejemplo (ocre) |
| `NOTA:` | Callout nota (azul) |
| `- texto` | Lista con guión |
| `1. texto` | Lista numerada |
| `SALTO:` | Separador |
        """)
        if st.button("📋 Cargar texto de ejemplo", key="btn_ejemplo"):
            st.session_state.texto_resumen = EJEMPLO_RESUMEN
            st.rerun()
        if st.button("🗑️ Limpiar", key="btn_limpiar"):
            st.session_state.texto_resumen = ""
            st.rerun()

    with col_editor:
        texto_resumen = st.text_area(
            "Texto del resumen",
            value=st.session_state.get("texto_resumen", ""),
            height=480,
            placeholder="TITULO: Hechos y Actos Jurídicos\n\nSUBTITULO: 1. Hecho Jurídico\n\nTEXTO: Es cualquier acontecimiento...\n\nDEF: Discernimiento - Aptitud para distinguir...\n\nEJ: El pago de una deuda es un acto lícito.\n\nNOTA: El silencio no es manifestación de voluntad.",
            label_visibility="collapsed",
        )
        st.session_state.texto_resumen = texto_resumen

    # Vista previa en tiempo real
    if texto_resumen.strip():
        st.markdown("---")
        st.markdown("## 👁️ Vista previa")
        html_res = generar_html_resumen(meta, texto_resumen)
        st.session_state.html_para_descargar = html_res
        components.html(html_res, height=860, scrolling=True)
    else:
        st.info("Empezá a escribir arriba para ver la vista previa en tiempo real.")
