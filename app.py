"""
╔══════════════════════════════════════════════════════════════╗
║      GENERADOR DE TRABAJOS PRÁCTICOS — DERECHO               ║
║      Streamlit App · UBA                                     ║
╚══════════════════════════════════════════════════════════════╝

Instalación (una sola vez):
    pip install streamlit

Uso:
    streamlit run generador_tp_streamlit.py
"""

import html
import re
import streamlit as st

# ══════════════════════════════════════════════════════════════
#  CONFIGURACIÓN DE LA PÁGINA
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Generador de TPs · Derecho Civil",
    page_icon="⚖️",
    layout="wide",
)

# CSS de la interfaz Streamlit (no del HTML generado)
st.markdown("""
<style>
    /* Acento burdeos en la barra lateral */
    section[data-testid="stSidebar"] { background: #1e1a1a; }
    section[data-testid="stSidebar"] * { color: #e8d8d8 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #d9a0a0 !important; }

    /* Título principal */
    h1 { color: #8b1a1a !important; font-family: Georgia, serif !important; }
    h2 { color: #5a1010 !important; font-family: Georgia, serif !important; border-bottom: 1.5px solid #c8b8b8; padding-bottom: 4px; }
    h3 { color: #3a3a3a !important; font-family: Georgia, serif !important; }

    /* Separadores de sección */
    .seccion-box {
        background: #faf9f7;
        border: 1px solid #e8e0e0;
        border-left: 4px solid #8b1a1a;
        border-radius: 4px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    .caso-box {
        background: #f2efe9;
        border-left: 4px solid #b3a070;
        border-radius: 4px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }
    .badge-v { background:#e6f2ea; color:#2a6e3f; border-radius:3px; padding:1px 7px; font-size:12px; font-weight:700; }
    .badge-f { background:#faeaea; color:#8b1a1a; border-radius:3px; padding:1px 7px; font-size:12px; font-weight:700; }

    /* Botón de descarga */
    div[data-testid="stDownloadButton"] button {
        background: #8b1a1a !important;
        color: white !important;
        font-weight: 600;
        border-radius: 4px;
        border: none;
        padding: 10px 28px;
        font-size: 15px;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: #6a1010 !important;
    }

    /* Eliminar padding extra */
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CONSTANTES
# ══════════════════════════════════════════════════════════════

TIPOS_SECCION = [
    "📋  Casos Prácticos",
    "✅  Verdadero o Falso",
    "📝  Preguntas Teóricas",
]

ROMANO = ["I","II","III","IV","V","VI","VII","VIII","IX","X",
          "XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX"]

LETRAS = list("abcdefghijklmnopqrstuvwxyz")

# ══════════════════════════════════════════════════════════════
#  CSS DEL HTML GENERADO (idéntico al TP original)
# ══════════════════════════════════════════════════════════════

HTML_CSS = """
<style>
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
    /* CASO */
    .case-block { margin:12px 0 8px; page-break-inside:avoid; break-inside:avoid; }
    .case-prompt { display:grid; grid-template-columns:28px 1fr; gap:0 8px; background:var(--case-bg); border-left:3.5px solid var(--case-border); border-radius:0 3px 3px 0; padding:8px 10px 8px 0; margin-bottom:8px; }
    .case-num { font-family:'Cormorant Garamond',serif; font-size:15pt; font-weight:600; color:var(--case-border); line-height:1.2; padding-left:10px; padding-top:1px; }
    .case-text { font-size:10.5pt; font-style:italic; color:var(--ink-light); line-height:1.5; text-align:justify; }
    .case-text p { margin:0; font-size:10.5pt; color:var(--ink-light); }
    /* Q&A */
    .qa-block { margin-bottom:7px; page-break-inside:avoid; break-inside:avoid; }
    h3 { font-family:'EB Garamond',serif; font-size:10.5pt; font-weight:700; color:var(--ink); border-left:2.5px solid var(--accent); padding-left:7px; margin:8px 0 4px; line-height:1.35; page-break-after:avoid; break-after:avoid; }
    .q-label { display:inline-block; font-family:'Cormorant Garamond',serif; font-size:9pt; font-weight:600; color:#fff; background:var(--accent); border-radius:2px; padding:0 5px; margin-right:5px; vertical-align:middle; line-height:1.5; }
    p { font-size:10.5pt; line-height:1.55; text-align:justify; margin-bottom:4px; color:var(--ink-light); }
    strong { font-weight:700; color:var(--ink); }
    em { font-style:italic; }
    ul,ol { margin-bottom:5px; }
    li { font-size:10.5pt; line-height:1.5; text-align:justify; margin-bottom:3px; color:var(--ink-light); }
    ul { list-style:none; padding-left:0; }
    ul>li { padding-left:14px; position:relative; }
    ul>li::before { content:'—'; color:var(--accent); position:absolute; left:0; font-weight:700; }
    ol { list-style:decimal; padding-left:1.3em; }
    /* CALLOUT */
    .callout-note { background:#f0f4f8; border-left:3px solid #4a7ab5; border-radius:0 2px 2px 0; padding:5px 9px; margin:5px 0; font-size:10pt; color:var(--ink-light); line-height:1.45; page-break-inside:avoid; break-inside:avoid; }
    .callout-note strong { color:#4a7ab5; }
    /* SEPARADOR */
    .divider { border:none; border-top:.5px solid var(--rule-light); margin:10px 0; }
    /* DOS COLUMNAS */
    .two-col { display:grid; grid-template-columns:1fr 1fr; gap:0 14px; }
    .two-col>* { min-width:0; }
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
    /* PIE */
    .doc-footer { display:flex; justify-content:space-between; font-size:7.5pt; color:var(--ink-muted); border-top:.5px solid var(--rule-light); padding-top:4px; margin-top:16px; }
    @media print {
        body { background:white; padding:0; }
        .document { box-shadow:none; width:100%; padding:0; background:white; }
        @page { size:A4; margin:16mm 20mm 18mm 20mm; }
        .doc-footer { display:none; }
        h3 { page-break-after:avoid; break-after:avoid; }
        p  { orphans:3; widows:3; }
        .qa-block,.case-prompt,.callout-note,.vf-block,.teorica-block { page-break-inside:avoid; break-inside:avoid; }
    }
</style>
"""

HTML_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap" rel="stylesheet">'

# ══════════════════════════════════════════════════════════════
#  HELPERS HTML
# ══════════════════════════════════════════════════════════════

def e(t):
    return html.escape(str(t))

def parrafos(text):
    """Texto con doble salto → múltiples <p>. Salto simple → <br>."""
    bloques = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    if not bloques:
        return f"<p>{e(text)}</p>"
    return "\n".join(
        "<p>" + "<br>".join(html.escape(l) for l in b.split("\n")) + "</p>"
        for b in bloques
    )

# ══════════════════════════════════════════════════════════════
#  GENERADORES DE SECCIONES HTML
# ══════════════════════════════════════════════════════════════

def html_portada(meta):
    sub = f'<p class="subtitle">{e(meta["subtitulo"])}</p>' if meta.get("subtitulo") else ""
    return f"""
<div class="cover">
  <div class="cover-left">
    <p class="eyebrow">Trabajo Práctico · {e(meta['materia'])}</p>
    <h1>{e(meta['titulo'])}</h1>{sub}
  </div>
  <div class="cover-right">
    <span class="label">Alumno/a</span><br>
    <strong>{e(meta['alumna'])}</strong><br>
    {e(meta['universidad'])}<br>
    {e(meta['facultad'])}
  </div>
</div>"""

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

    # Quitar último divider
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

    return f"""
<div class="two-col">
  <div>{render(col1)}</div>
  <div>{render(col2)}</div>
</div>"""

def html_teoricas(items):
    return "\n".join(f"""
<div class="teorica-block">
  <h3><span class="teorica-num">{it['num']}.</span> {e(it['pregunta'])}</h3>
  {parrafos(it['respuesta'])}
</div>""" for it in items)

def generar_html_completo(meta, secciones):
    GEN = [html_casos, html_vf, html_teoricas]
    body = html_portada(meta)

    for i, sec in enumerate(secciones):
        roman  = ROMANO[i]
        cuerpo = GEN[sec["tipo"]](sec["contenido"])

        # VF: envolver para evitar que el título quede solo al final de página
        if sec["tipo"] == 1:
            body += f"""
<div style="page-break-inside:avoid;break-inside:avoid;">
<div class="section-header">
  <span class="section-num">{roman}</span>
  <span class="section-title">{e(sec['titulo'])}</span>
</div>
{cuerpo}
</div>"""
        else:
            body += f"""
<div class="section-header">
  <span class="section-num">{roman}</span>
  <span class="section-title">{e(sec['titulo'])}</span>
</div>
{cuerpo}"""

    body += f"""
<div class="doc-footer">
  <span>{e(meta['alumna'])} · {e(meta['universidad'])} · {e(meta['materia'])}</span>
  <span>Trabajo Práctico</span>
</div>"""

    nombre = e(f"{meta['titulo']} — {meta['alumna']}")
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
{body}
</div>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════
#  ESTADO DE SESIÓN
# ══════════════════════════════════════════════════════════════

def init_state():
    if "secciones" not in st.session_state:
        st.session_state.secciones = []

init_state()

# ══════════════════════════════════════════════════════════════
#  SIDEBAR — METADATOS
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ⚖️ Datos del TP")
    st.markdown("---")
    titulo      = st.text_input("Título", value="...")
    subtitulo   = st.text_input("Subtítulo", value="...")
    materia     = st.text_input("Materia", value="...")
    alumna      = st.text_input("Alumno/a", value="...")
    universidad = st.text_input("Universidad", value="Universidad de Buenos Aires")
    facultad    = st.text_input("Facultad", value="Facultad de Derecho")

    st.markdown("---")
    st.markdown("### 📥 Descargar")

    meta = {
        "titulo": titulo, "subtitulo": subtitulo,
        "materia": materia, "alumna": alumna,
        "universidad": universidad, "facultad": facultad,
    }

    if st.session_state.secciones:
        html_out = generar_html_completo(meta, st.session_state.secciones)
        nombre_archivo = re.sub(r"[^\w\s-]", "", f"{alumna}_{titulo}").strip()
        nombre_archivo = re.sub(r"\s+", "_", nombre_archivo)[:50] + ".html"
        st.download_button(
            label="⬇️  Descargar HTML",
            data=html_out.encode("utf-8"),
            file_name=nombre_archivo,
            mime="text/html",
        )
        st.caption("Abrí el archivo en Chrome y hacé Ctrl+P → Guardar como PDF")
    else:
        st.info("Agregá al menos una sección para descargar.")

    st.markdown("---")
    st.markdown("**Instrucciones rápidas:**")
    st.markdown("""
- Completá los datos arriba
- Agregá secciones en el panel central
- Descargá el HTML cuando termines
- Para párrafos separados, dejá una línea en blanco entre ellos
""")

# ══════════════════════════════════════════════════════════════
#  PANEL PRINCIPAL
# ══════════════════════════════════════════════════════════════

st.markdown("# ⚖️ Generador de Trabajos Prácticos")
st.markdown("*Derecho Civil — Parte General · Estilo académico UBA*")
st.markdown("---")

# ── AGREGAR SECCIÓN ──────────────────────────────────────────

st.markdown("## Secciones")

col_tipo, col_titulo, col_btn = st.columns([2, 3, 1])
with col_tipo:
    tipo_nuevo = st.selectbox("Tipo de sección", TIPOS_SECCION, label_visibility="collapsed")
with col_titulo:
    titulo_nuevo = st.text_input("Título de la sección", placeholder="Ej: Casos Prácticos", label_visibility="collapsed")
with col_btn:
    if st.button("➕ Agregar", use_container_width=True):
        if titulo_nuevo.strip():
            idx = TIPOS_SECCION.index(tipo_nuevo)
            st.session_state.secciones.append({
                "tipo":     idx,
                "titulo":   titulo_nuevo.strip(),
                "contenido": [],
            })
            st.rerun()
        else:
            st.error("Escribí un título para la sección.")

st.markdown("")

# ── SECCIONES EXISTENTES ─────────────────────────────────────

for sec_i, sec in enumerate(st.session_state.secciones):
    roman = ROMANO[sec_i]
    tipo  = sec["tipo"]
    icono = ["📋","✅","📝"][tipo]

    with st.expander(f"{icono}  **{roman}. {sec['titulo']}**", expanded=True):

        # Botón eliminar sección
        col_espacio, col_del = st.columns([6, 1])
        with col_del:
            if st.button("🗑️ Eliminar sección", key=f"del_sec_{sec_i}"):
                st.session_state.secciones.pop(sec_i)
                st.rerun()

        # ── CASOS PRÁCTICOS ──────────────────────────────────
        if tipo == 0:
            for c_i, caso in enumerate(sec["contenido"]):
                st.markdown(f'<div class="caso-box">', unsafe_allow_html=True)
                st.markdown(f"**Caso {caso['num']}**")

                caso["enunciado"] = st.text_area(
                    "Enunciado del caso",
                    value=caso["enunciado"],
                    key=f"caso_{sec_i}_{c_i}_enunc",
                    height=80,
                )

                st.markdown("*Preguntas y respuestas:*")
                for p_i, preg in enumerate(caso["preguntas"]):
                    pcol1, pcol2, pcol3 = st.columns([0.5, 3, 3])
                    with pcol1:
                        st.markdown(f"**{preg['label'].upper()}.**")
                    with pcol2:
                        preg["pregunta"] = st.text_area(
                            "Pregunta",
                            value=preg["pregunta"],
                            key=f"caso_{sec_i}_{c_i}_preg_{p_i}",
                            height=68,
                            label_visibility="collapsed",
                            placeholder="Texto de la pregunta...",
                        )
                    with pcol3:
                        preg["respuesta"] = st.text_area(
                            "Respuesta",
                            value=preg["respuesta"],
                            key=f"caso_{sec_i}_{c_i}_resp_{p_i}",
                            height=68,
                            label_visibility="collapsed",
                            placeholder="Respuesta...",
                        )
                    if st.button(f"✕ Quitar pregunta {preg['label'].upper()}", key=f"del_preg_{sec_i}_{c_i}_{p_i}"):
                        caso["preguntas"].pop(p_i)
                        # Re-asignar letras
                        for k, p in enumerate(caso["preguntas"]):
                            p["label"] = LETRAS[k]
                        st.rerun()

                bcol1, bcol2 = st.columns([1, 1])
                with bcol1:
                    if st.button(f"➕ Agregar pregunta al caso {caso['num']}", key=f"add_preg_{sec_i}_{c_i}"):
                        caso["preguntas"].append({
                            "label":    LETRAS[len(caso["preguntas"])],
                            "pregunta": "",
                            "respuesta": "",
                        })
                        st.rerun()
                with bcol2:
                    if st.button(f"🗑️ Eliminar caso {caso['num']}", key=f"del_caso_{sec_i}_{c_i}"):
                        sec["contenido"].pop(c_i)
                        for k, ca in enumerate(sec["contenido"]):
                            ca["num"] = k + 1
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("")

            if st.button("➕ Agregar nuevo caso", key=f"add_caso_{sec_i}"):
                sec["contenido"].append({
                    "num":      len(sec["contenido"]) + 1,
                    "enunciado": "",
                    "preguntas": [{"label": "a", "pregunta": "", "respuesta": ""}],
                })
                st.rerun()

        # ── VERDADERO O FALSO ────────────────────────────────
        elif tipo == 1:
            for it_i, item in enumerate(sec["contenido"]):
                icols = st.columns([0.3, 3, 1, 3, 0.5])
                with icols[0]:
                    st.markdown(f"**{item['label'].upper()}.**")
                with icols[1]:
                    item["afirmacion"] = st.text_area(
                        "Afirmación",
                        value=item["afirmacion"],
                        key=f"vf_{sec_i}_{it_i}_afirm",
                        height=80,
                        label_visibility="collapsed",
                        placeholder="Afirmación...",
                    )
                with icols[2]:
                    veredicto = st.radio(
                        "Veredicto",
                        ["Verdadero", "Falso"],
                        index=0 if item["verdadero"] else 1,
                        key=f"vf_{sec_i}_{it_i}_ver",
                        label_visibility="collapsed",
                    )
                    item["verdadero"] = (veredicto == "Verdadero")
                    badge = "badge-v" if item["verdadero"] else "badge-f"
                    st.markdown(f'<span class="{badge}">{veredicto}</span>', unsafe_allow_html=True)
                with icols[3]:
                    item["justificacion"] = st.text_area(
                        "Justificación",
                        value=item["justificacion"],
                        key=f"vf_{sec_i}_{it_i}_just",
                        height=80,
                        label_visibility="collapsed",
                        placeholder="Justificación...",
                    )
                with icols[4]:
                    if st.button("✕", key=f"del_vf_{sec_i}_{it_i}", help="Eliminar ítem"):
                        sec["contenido"].pop(it_i)
                        for k, it in enumerate(sec["contenido"]):
                            it["label"] = LETRAS[k]
                        st.rerun()

            if st.button("➕ Agregar ítem V/F", key=f"add_vf_{sec_i}"):
                sec["contenido"].append({
                    "label":        LETRAS[len(sec["contenido"])],
                    "afirmacion":   "",
                    "verdadero":    True,
                    "justificacion": "",
                })
                st.rerun()

        # ── PREGUNTAS TEÓRICAS ───────────────────────────────
        elif tipo == 2:
            for it_i, item in enumerate(sec["contenido"]):
                tcols = st.columns([0.3, 3, 3, 0.5])
                with tcols[0]:
                    st.markdown(f"**{item['num']}.**")
                with tcols[1]:
                    item["pregunta"] = st.text_area(
                        "Pregunta",
                        value=item["pregunta"],
                        key=f"teo_{sec_i}_{it_i}_preg",
                        height=80,
                        label_visibility="collapsed",
                        placeholder="Pregunta teórica...",
                    )
                with tcols[2]:
                    item["respuesta"] = st.text_area(
                        "Respuesta",
                        value=item["respuesta"],
                        key=f"teo_{sec_i}_{it_i}_resp",
                        height=80,
                        label_visibility="collapsed",
                        placeholder="Respuesta...",
                    )
                with tcols[3]:
                    if st.button("✕", key=f"del_teo_{sec_i}_{it_i}", help="Eliminar pregunta"):
                        sec["contenido"].pop(it_i)
                        for k, it in enumerate(sec["contenido"]):
                            it["num"] = k + 1
                        st.rerun()

            if st.button("➕ Agregar pregunta teórica", key=f"add_teo_{sec_i}"):
                sec["contenido"].append({
                    "num":      len(sec["contenido"]) + 1,
                    "pregunta": "",
                    "respuesta": "",
                })
                st.rerun()

# ── VISTA PREVIA ─────────────────────────────────────────────

if st.session_state.secciones:
    st.markdown("---")
    st.markdown("## 👁️ Vista previa del HTML")
    st.caption("Así va a verse al imprimirlo. Podés hacer zoom con Ctrl+scroll.")

    html_preview = generar_html_completo(meta, st.session_state.secciones)
    st.components.v1.html(html_preview, height=900, scrolling=True)
