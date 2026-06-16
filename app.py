import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HydroWet · Diseño de Humedales",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PALETTE ────────────────────────────────────────────────────────────────────
VERDE    = "#0E9E63"            # verde principal, mas saturado
VERDE_D  = "#0A7A4C"            # verde oscuro para hover/acentos
VERDE_O  = "rgba(14,158,99,0.10)"
VERDE_O2 = "rgba(14,158,99,0.22)"
AMBAR    = "#C77E1A"            # ambar mas profundo y legible
AMBAR_O  = "rgba(199,126,26,0.14)"
ROJO     = "#D6452B"            # rojo mas vivo
ROJO_O   = "rgba(214,69,43,0.13)"
AZUL     = "#2E7CC4"            # azul de apoyo para graficos
MORADO   = "#7E4FC2"
OSCURO   = "#08160F"            # sidebar / encabezado casi negro verdoso
TEAL     = "#1F4A3A"
BG_APP   = "#E9EFE9"            # fondo app
BG_CARD  = "#FFFFFF"
TEXTO    = "#0F1F18"            # texto principal mucho mas oscuro
TEXTO2   = "#3A4D43"            # texto secundario
GRIS     = "#5C6E62"            # gris de etiquetas con buen contraste
BORDE    = "#CBDBCB"
SOMBRA   = "0 2px 8px rgba(8,22,15,0.08)"

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

/* ── Reset base ── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: {TEXTO};
    font-size: 16.5px;
}}

/* ── Fondo principal ── */
.stApp {{
    background: #F5F8F5;
}}
.block-container {{
    padding-top: 2rem;
    max-width: 1400px;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: #0A1810 !important;
}}
section[data-testid="stSidebar"] {{
    background-color: #0A1810 !important;
    background: #0A1810 !important;
    border-right: 3px solid {VERDE} !important;
}}
section[data-testid="stSidebar"] > div {{
    background-color: #0A1810 !important;
}}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
    color: #FFFFFF !important;
}}
section[data-testid="stSidebar"] label {{
    color: #B8D4BE !important;
    font-weight: 600 !important;
}}
section[data-testid="stSidebar"] input {{
    background: #11261B !important;
    border: 1px solid #2E5C46 !important;
    color: #FFFFFF !important;
}}
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stNumberInput {{
    color: #FFFFFF !important;
}}

/* ── Expand sidebar by default ── */
[data-testid="collapsedControl"] {{
    display: none !important;
}}
section[data-testid="stSidebar"] {{
    transform: translateX(0) !important;
    visibility: visible !important;
    width: 280px !important;
    position: relative !important;
}}
.stMainBlockContainer {{
    margin-left: 0;
}}

/* ── Ensure sidebar is visible ── */
section[data-testid="stSidebar"] > div {{
    width: 280px !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: transparent;
    border-bottom: 2px solid {BORDE};
    padding-bottom: 0;
    margin-bottom: 0;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.02rem;
    color: {TEXTO2};
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    border-radius: 0;
    padding: 12px 20px;
    transition: all 0.2s;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {VERDE_D};
}}
.stTabs [aria-selected="true"] {{
    color: {VERDE_D} !important;
    border-bottom: 3px solid {VERDE} !important;
    background: transparent !important;
}}
.stTabs [data-baseweb="tab-panel"] {{
    padding-top: 28px;
}}

/* ── Cards de metricas ── */
.metric-card {{
    background: white;
    border: 1px solid {BORDE};
    border-radius: 14px;
    padding: 22px 24px;
    margin: 6px 0;
    position: relative;
    overflow: hidden;
    box-shadow: {SOMBRA};
    transition: transform 0.18s, box-shadow 0.18s;
}}
.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(8,22,15,0.12);
}}
.metric-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 5px; height: 100%;
    background: {VERDE};
}}
.metric-card.amber::before {{ background: {AMBAR}; }}
.metric-card.red::before   {{ background: {ROJO}; }}

.metric-label {{
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    color: {GRIS};
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 8px;
}}
.metric-value {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.35rem;
    font-weight: 700;
    color: {TEXTO};
    line-height: 1;
}}
.metric-value span {{
    font-size: 1.1rem;
    font-weight: 500;
    color: {TEXTO2};
    margin-left: 4px;
}}
.metric-delta {{
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: {VERDE_D};
    margin-top: 8px;
    font-weight: 600;
}}
.metric-delta.neg {{ color: {ROJO}; }}

/* ── Eficiencia pill ── */
.eff-container {{
    background: white;
    border: 1px solid {BORDE};
    border-radius: 12px;
    padding: 18px 22px;
    margin: 4px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}}
.eff-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}}
.eff-label {{
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: {TEXTO};
}}
.eff-pct {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: {VERDE_D};
}}
.eff-pct.amber {{ color: {AMBAR}; }}
.eff-pct.red   {{ color: {ROJO}; }}
.eff-bar-bg {{
    height: 11px;
    background: #DDE8DD;
    border-radius: 99px;
    overflow: hidden;
}}
.eff-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, {VERDE_D}, {VERDE});
    border-radius: 99px;
    transition: width 0.8s cubic-bezier(.4,0,.2,1);
}}
.eff-bar-fill.amber {{
    background: linear-gradient(90deg, #A8650F, {AMBAR});
}}
.eff-bar-fill.red {{
    background: linear-gradient(90deg, #B8351F, {ROJO});
}}

/* ── Encabezado de seccion ── */
.section-header {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: {TEXTO};
    margin-bottom: 5px;
    letter-spacing: -0.01em;
}}
.section-sub {{
    font-size: 0.98rem;
    color: {TEXTO2};
    margin-bottom: 22px;
    font-weight: 500;
}}

/* ── Badge ── */
.badge {{
    display: inline-block;
    padding: 4px 11px;
    border-radius: 99px;
    font-size: 0.84rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}}
.badge.green  {{ background: {VERDE_O2};  color: {VERDE_D}; }}
.badge.amber  {{ background: {AMBAR_O};   color: #9A610D; }}
.badge.red    {{ background: {ROJO_O};    color: #B8351F;  }}

/* ── Tabla de parámetros ── */
.param-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid {BORDE};
    font-size: 1rem;
    box-shadow: {SOMBRA};
}}
.param-table thead tr {{
    background: {OSCURO};
}}
.param-table thead th {{
    font-family: 'Space Grotesk', sans-serif;
    color: #B8D4BE;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 15px 18px;
    text-align: left;
    font-weight: 600;
}}
.param-table tbody tr {{
    background: white;
    border-bottom: 1px solid {BORDE};
    transition: background 0.15s;
}}
.param-table tbody tr:nth-child(even) {{
    background: #F8FAF8;
}}
.param-table tbody tr:hover {{
    background: {VERDE_O};
}}
.param-table tbody td {{
    padding: 13px 18px;
    color: {TEXTO};
    font-weight: 500;
}}
.param-table tbody td:first-child {{
    font-weight: 700;
    color: {VERDE_D};
}}

/* ── Card de diseño ── */
.design-card {{
    background: white;
    border: 1px solid {BORDE};
    border-radius: 16px;
    padding: 26px 20px;
    text-align: center;
    box-shadow: {SOMBRA};
    transition: transform 0.18s, box-shadow 0.18s;
    height: 100%;
}}
.design-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(8,22,15,0.13);
}}
.design-icon {{
    font-size: 2.3rem;
    margin-bottom: 8px;
}}
.design-val {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.55rem;
    font-weight: 700;
    color: {VERDE_D};
}}
.design-unit {{
    font-size: 0.98rem;
    color: {TEXTO2};
    font-weight: 600;
    margin-top: 4px;
}}
.design-desc {{
    font-size: 0.88rem;
    color: {GRIS};
    margin-top: 10px;
    line-height: 1.5;
}}

/* ── Reporte card ── */
.reporte-card {{
    background: white;
    border: 1px solid {BORDE};
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 14px;
    box-shadow: {SOMBRA};
}}
.reporte-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: {TEXTO};
    margin-bottom: 14px;
    padding-bottom: 11px;
    border-bottom: 2px solid {VERDE_O2};
}}
.reporte-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    font-size: 0.98rem;
    border-bottom: 1px solid #EDF3ED;
}}
.reporte-row:last-child {{ border-bottom: none; }}
.reporte-key   {{ color: {TEXTO2}; font-weight: 500; }}
.reporte-value {{ font-weight: 700; color: {TEXTO}; font-family: 'Space Grotesk', sans-serif; }}

/* ── Advertencia / Cumplimiento ── */
.cumpl-item {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 11px 0;
    border-bottom: 1px solid #EDF3ED;
    font-size: 0.98rem;
}}
.cumpl-item:last-child {{ border-bottom: none; }}
.cumpl-dot {{
    width: 10px; height: 10px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}}
.cumpl-dot.ok   {{ background: {VERDE}; }}
.cumpl-dot.warn {{ background: {AMBAR}; }}
.cumpl-dot.fail {{ background: {ROJO};  }}

/* ── Plotly override ── */
.js-plotly-plot .plotly .main-svg {{ border-radius: 10px; }}

/* ── Header app ── */
.app-header-left {{
    background: linear-gradient(120deg, {OSCURO} 0%, {TEAL} 100%);
    border-radius: 14px;
    padding: 20px 28px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 16px rgba(8,22,15,0.18);
}}
.app-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.95rem;
    font-weight: 700;
    color: white;
    margin: 0;
    letter-spacing: -0.01em;
}}
.app-subtitle {{
    font-size: 1rem;
    color: #C5DCC9;
    margin-top: 5px;
    font-weight: 500;
}}
.app-subtitle strong {{ color: #5FD99A; }}
.app-logo {{
    font-size: 2.8rem;
    line-height: 1;
}}

/* ── Ocultar elementos default de Streamlit ── */
#MainMenu, footer {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}
header[data-testid="stHeader"] {{
    background: transparent;
    border-bottom: none;
}}
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ────────────────────────────────────────────────────────────────────
def eff(entrada, salida):
    if entrada == 0: return 0.0
    return max(0.0, min(100.0, (entrada - salida) / entrada * 100))

def color_eff(e):
    if e >= 80: return "green"
    if e >= 55: return "amber"
    return "red"

def badge(label, cls="green"):
    return f'<span class="badge {cls}">{label}</span>'

def eff_bar(label, entrada, salida):
    e = eff(entrada, salida)
    cls = color_eff(e)
    return f"""
    <div class="eff-container">
      <div class="eff-header">
        <span class="eff-label">{label}</span>
        <span class="eff-pct {cls}">{e:.1f}%</span>
      </div>
      <div class="eff-bar-bg">
        <div class="eff-bar-fill {cls}" style="width:{e:.1f}%"></div>
      </div>
    </div>
    """

def metric_card(label, value, unit, delta="", cls=""):
    delta_cls = "" if not delta.startswith("▼") else "neg"
    return f"""
    <div class="metric-card {cls}">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}<span>{unit}</span></div>
      <div class="metric-delta {delta_cls}">{delta}</div>
    </div>
    """

def tabla_row(param, entrada, salida, unidad, norma="—"):
    e = eff(entrada, salida) if isinstance(entrada, (int, float)) else None
    if e is not None:
        if e >= 80:    badge_html = f'<span class="badge green">{e:.1f}%</span>'
        elif e >= 55:  badge_html = f'<span class="badge amber">{e:.1f}%</span>'
        else:          badge_html = f'<span class="badge red">{e:.1f}%</span>'
    else:
        badge_html = "—"
    
    e_str = str(entrada) if not isinstance(entrada, float) else f"{entrada:.3g}"
    s_str = str(salida)  if not isinstance(salida,  float) else f"{salida:.3g}"
    return f"""
    <tr>
      <td>{param}</td>
      <td>{e_str} {unidad}</td>
      <td>{s_str} {unidad}</td>
      <td>{badge_html}</td>
      <td>{norma}</td>
    </tr>
    """

PLOTLY_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Inter", size=15, color=TEXTO),
    title_font=dict(family="Space Grotesk", color=TEXTO, size=16),
    paper_bgcolor="white",
    plot_bgcolor="white",
    colorway=[VERDE, AMBAR, AZUL, MORADO],
)
# Margin por defecto reutilizable (no va en PLOTLY_LAYOUT para evitar conflictos)
MARGIN_DEFAULT = dict(l=30, r=20, t=50, b=40)
MARGIN_POLAR   = dict(l=50, r=50, t=60, b=50)


# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────
nombre_proyecto = "Poza Séptica Piloto"
modo = "Datos de ejemplo"
poza = "Poza #1 + #2 (Promedio)"  # Datos representativos



# ─── DATOS ───────────────────────────────────────────────────────────────────────
if modo == "Datos de ejemplo":
    D = dict(
        poza=poza,
        c_e=0.162,  c_s=0.080,
        ph_e=6.67,  ph_s=7.52,
        temp=29.12,
        dbo_e=625.0,   dbo_s=40.7,
        dqo_e=1248.9,  dqo_s=97.8,
        sst_e=2644.0,  sst_s=23.3,
        sed_e=69.5,    sed_s=0.05,
        ct_e=4551471.7, ct_s=393169.6,
        cf_e=337465.0,  cf_s=18008.6,
        fen_e=0.182,   fen_s=0.150,
        gra_e=1348.9,  gra_s=12.7,
        sur_e=4.92,    sur_s=1.96,
        cond_e=1052.0, cond_s=891.4,
        alc_e=316.9,   alc_s=247.4,
    )
else:
    D = dict(
        poza=poza,
        c_e=c_e,    c_s=c_s,
        ph_e=ph_e,  ph_s=ph_s,
        temp=temp,
        dbo_e=float(dbo_e), dbo_s=float(dbo_s),
        dqo_e=float(dqo_e), dqo_s=float(dqo_s),
        sst_e=float(sst_e), sst_s=float(sst_s),
        sed_e=sed_e, sed_s=sed_s,
        ct_e=float(ct_e),  ct_s=float(ct_s),
        cf_e=float(cf_e),  cf_s=float(cf_s),
        fen_e=fen_e, fen_s=fen_s,
        gra_e=float(gra_e), gra_s=float(gra_s),
        sur_e=sur_e, sur_s=sur_s,
        cond_e=float(cond_e), cond_s=float(cond_s),
        alc_e=float(alc_e),  alc_s=float(alc_s),
    )

# Parámetros adicionales (si ingreso manual)
if modo == "Ingreso manual":
    with st.expander("📊 Parámetros detallados (Ingreso manual)", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            c_e = st.number_input("Caudal entrada (L/s)", 0.05, 2.0, 0.162, 0.01)
            ph_e = st.number_input("pH entrada", 5.0, 9.0, 6.67, 0.01)
            dbo_e = st.number_input("DBO₅ entrada (mg/L)", 10, 5000, 625, 10)
        with col2:
            c_s = st.number_input("Caudal salida (L/s)", 0.01, 1.0, 0.080, 0.01)
            ph_s = st.number_input("pH salida", 5.0, 9.0, 7.52, 0.01)
            dbo_s = st.number_input("DBO₅ salida (mg/L)", 1, 500, 41, 1)
        with col3:
            dqo_e = st.number_input("DQO entrada (mg/L)", 50, 10000, 1249, 50)
            dqo_s = st.number_input("DQO salida (mg/L)", 10, 1000, 98, 10)
            sst_e = st.number_input("SST entrada (mg/L)", 50, 10000, 2644, 100)
        with col4:
            sst_s = st.number_input("SST salida (mg/L)", 1, 200, 23, 1)
            sed_e = st.number_input("Sedimentables entrada (mL/L)", 0.0, 200.0, 69.5, 0.5)
            sed_s = st.number_input("Sedimentables salida (mL/L)", 0.0, 10.0, 0.05, 0.01)
        
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            ct_e = st.number_input("Col. Totales entrada (NMP/100mL)", 100, 10000000, 4551472, 10000)
            cf_e = st.number_input("Col. Fecales entrada (NMP/100mL)", 10, 1000000, 337465, 10000)
        with col6:
            ct_s = st.number_input("Col. Totales salida (NMP/100mL)", 10, 1000000, 393170, 1000)
            cf_s = st.number_input("Col. Fecales salida (NMP/100mL)", 1, 100000, 18009, 1000)
        with col7:
            fen_e = st.number_input("Fenoles entrada (mg/L)", 0.0, 2.0, 0.182, 0.001)
            gra_e = st.number_input("Grasas entrada (mg/L)", 0, 5000, 1349, 50)
        with col8:
            fen_s = st.number_input("Fenoles salida (mg/L)", 0.0, 0.5, 0.150, 0.001)
            gra_s = st.number_input("Grasas salida (mg/L)", 0, 200, 13, 1)
        
        col9, col10, col11 = st.columns(3)
        with col9:
            sur_e = st.number_input("Surfactantes entrada (mg/L)", 0.0, 20.0, 4.92, 0.01)
            temp = st.number_input("Temperatura (°C)", 20.0, 35.0, 29.1, 0.1)
        with col10:
            sur_s = st.number_input("Surfactantes salida (mg/L)", 0.0, 10.0, 1.96, 0.01)
            cond_e = st.number_input("Conductividad entrada (µS/cm)", 100, 3000, 1052, 10)
        with col11:
            alc_e = st.number_input("Alcalinidad entrada (mg CaCO₃/L)", 50, 1000, 316, 5)
            alc_s = st.number_input("Alcalinidad salida (mg CaCO₃/L)", 50, 800, 247, 5)
            cond_s = st.number_input("Conductividad salida (µS/cm)", 100, 2000, 891, 10)


# Cálculos de diseño
np.random.seed(42)
caudal_dia   = D["c_e"] * 86.4          # m³/día
tasa_carga   = 6.0                       # m²/(m³/día)
area         = caudal_dia / tasa_carga
profundidad  = 0.8 if D["dbo_e"] > 800 else (0.65 if D["dbo_e"] > 200 else 0.5)
volumen      = area * profundidad
trh          = volumen / caudal_dia * 24  # horas
carga_dbo    = D["dbo_e"] * D["c_e"] * 86.4 / 1000  # kg/día

# Eficiencias
eff_dbo  = eff(D["dbo_e"],  D["dbo_s"])
eff_dqo  = eff(D["dqo_e"],  D["dqo_s"])
eff_sst  = eff(D["sst_e"],  D["sst_s"])
eff_sed  = eff(D["sed_e"],  D["sed_s"])
eff_ct   = eff(D["ct_e"],   D["ct_s"])
eff_cf   = eff(D["cf_e"],   D["cf_s"])
eff_fen  = eff(D["fen_e"],  D["fen_s"])
eff_gra  = eff(D["gra_e"],  D["gra_s"])
eff_sur  = eff(D["sur_e"],  D["sur_s"])

eff_global = np.mean([eff_dbo, eff_dqo, eff_sst, eff_ct])


# ─── HEADER ──────────────────────────────────────────────────────────────────────
# Header simplificado
st.markdown(f"""
<div class="app-header-left">
  <div class="app-logo">🌿</div>
  <div>
    <div class="app-title">HydroWet · Diseño de Humedales Verticales</div>
    <div class="app-subtitle">{nombre_proyecto} &nbsp;·&nbsp; {poza} &nbsp;·&nbsp; ⚡ {eff_global:.1f}%</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── TABS ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "   📊  Dashboard   ",
    "   🧪  Parámetros   ",
    "   📈  Análisis   ",
    "   🏗️  Diseño   ",
    "   📋  Reporte   ",
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Resumen operacional</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Vista general de los indicadores clave del sistema de tratamiento</div>', unsafe_allow_html=True)

    # Fila 1 — métricas rápidas
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("Eficiencia Global", f"{eff_global:.1f}", "%",
                                f"▲ {eff_dbo:.1f}% remoción DBO₅"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("Caudal Tratado", f"{caudal_dia:.2f}", "m³/día",
                                f"▲ {D['c_e']:.3f} L/s entrada", "amber"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("DBO₅ Salida", f"{D['dbo_s']:.1f}", "mg/L",
                                f"▼ Desde {D['dbo_e']:.0f} mg/L entrada"), unsafe_allow_html=True)
    with c4:
        norma_col = "red" if D["ct_s"] > 1000 else "green"
        st.markdown(metric_card("Col. Totales Salida", f"{D['ct_s']/1000:.1f}", "×10³ NMP",
                                f"{'⚠ Sobre norma' if D['ct_s']>1000 else '✓ Dentro norma'}", norma_col), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Fila 2 — barras de eficiencia + gráfico polar
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="section-header" style="font-size:1rem;">Eficiencia de remoción por parámetro</div>', unsafe_allow_html=True)
        st.markdown(eff_bar("DBO₅ — Demanda bioquímica de oxígeno", D["dbo_e"], D["dbo_s"]), unsafe_allow_html=True)
        st.markdown(eff_bar("DQO — Demanda química de oxígeno",      D["dqo_e"], D["dqo_s"]), unsafe_allow_html=True)
        st.markdown(eff_bar("SST — Sólidos suspendidos totales",      D["sst_e"], D["sst_s"]), unsafe_allow_html=True)
        st.markdown(eff_bar("Sólidos Sedimentables",                  D["sed_e"], D["sed_s"]), unsafe_allow_html=True)
        st.markdown(eff_bar("Coliformes Totales",                     D["ct_e"],  D["ct_s"]),  unsafe_allow_html=True)
        st.markdown(eff_bar("Coliformes Fecales",                     D["cf_e"],  D["cf_s"]),  unsafe_allow_html=True)
        st.markdown(eff_bar("Grasas y Aceites",                       D["gra_e"], D["gra_s"]), unsafe_allow_html=True)
        st.markdown(eff_bar("Surfactantes Aniónicos",                 D["sur_e"], D["sur_s"]), unsafe_allow_html=True)

    with col_right:
        params  = ["DBO₅", "DQO", "SST", "Sedimentables", "Col. Totales", "Col. Fecales", "Grasas", "Surfactantes"]
        valores = [eff_dbo, eff_dqo, eff_sst, eff_sed, eff_ct, eff_cf, eff_gra, eff_sur]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=valores + [valores[0]],
            theta=params + [params[0]],
            fill="toself",
            fillcolor="rgba(14,158,99,0.18)",
            line=dict(color=VERDE_D, width=2.5),
            marker=dict(size=9, color=VERDE_D, symbol="circle",
                        line=dict(color="white", width=2)),
            name="Eficiencia",
            hovertemplate="<b>%{theta}</b><br>Eficiencia: <b>%{r:.1f}%</b><extra></extra>",
        ))
        # Zona objetivo ≥80%
        fig_radar.add_trace(go.Scatterpolar(
            r=[80]*len(params) + [80],
            theta=params + [params[0]],
            mode="lines",
            line=dict(color=AMBAR, width=1.5, dash="dot"),
            name="Objetivo 80%",
            hoverinfo="skip",
        ))
        fig_radar.update_layout(
            **{**PLOTLY_LAYOUT, "margin": dict(l=60, r=60, t=70, b=60)},
            polar=dict(
                bgcolor="white",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    ticksuffix="%",
                    tickfont=dict(size=12, color=GRIS),
                    gridcolor="#E8F0E8",
                    linecolor=BORDE,
                    tickvals=[20, 40, 60, 80, 100],
                ),
                angularaxis=dict(
                    tickfont=dict(size=13, color=TEXTO, family="Space Grotesk"),
                    linecolor=BORDE,
                    gridcolor="#E8F0E8",
                )
            ),
            legend=dict(
                orientation="h", x=0.5, xanchor="center", y=-0.12,
                bgcolor="white", bordercolor=BORDE, borderwidth=1,
                font=dict(size=13),
            ),
            title=dict(
                text="Perfil de eficiencia de remoción",
                font=dict(family="Space Grotesk", size=16, color=TEXTO),
                x=0.5, xanchor="center",
            ),
            height=460,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Fila 3 — tendencia simulada mensual
    st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PARÁMETROS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Parámetros fisicoquímicos y microbiológicos</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Comparativa entrada / salida del sistema con eficiencia de remoción calculada</div>', unsafe_allow_html=True)

    tabla_html = f"""
    <table class="param-table">
      <thead>
        <tr>
          <th>Parámetro</th>
          <th>Entrada</th>
          <th>Salida</th>
          <th>Remoción</th>
          <th>Norma ref.</th>
        </tr>
      </thead>
      <tbody>
        {tabla_row("pH",                    f"{D['ph_e']:.2f}",   f"{D['ph_s']:.2f}", "u pH",        "6.5 – 8.5")}
        {tabla_row("Temperatura",            f"{D['temp']:.1f}", f"{D['temp']:.1f}", "°C",           "< 30 °C")}
        {tabla_row("Conductividad",         D['cond_e'],          D['cond_s'],       "µS/cm",        "< 1500")}
        {tabla_row("Alcalinidad Total",     D['alc_e'],           D['alc_s'],        "mg CaCO₃/L",   "—")}
        {tabla_row("DBO₅",                 D['dbo_e'],            D['dbo_s'],        "mg O₂/L",      "< 25 mg/L")}
        {tabla_row("DQO",                  D['dqo_e'],            D['dqo_s'],        "mg O₂/L",      "< 100 mg/L")}
        {tabla_row("SST",                  D['sst_e'],            D['sst_s'],        "mg/L",         "< 30 mg/L")}
        {tabla_row("Sólidos Sedimentables",D['sed_e'],            D['sed_s'],        "mL/L",         "< 1 mL/L")}
        {tabla_row("Grasas y Aceites",     D['gra_e'],            D['gra_s'],        "mg/L",         "< 20 mg/L")}
        {tabla_row("Fenoles",              D['fen_e'],            D['fen_s'],        "mg/L",         "< 0.15 mg/L")}
        {tabla_row("Surfactantes",         D['sur_e'],            D['sur_s'],        "mg SAAM/L",    "< 2 mg/L")}
        {tabla_row("Coliformes Totales",   f"{D['ct_e']:.0f}",   f"{D['ct_s']:.0f}","NMP/100mL",    "< 1000")}
        {tabla_row("Coliformes Fecales",   f"{D['cf_e']:.0f}",   f"{D['cf_s']:.0f}","NMP/100mL",    "< 200")}
      </tbody>
    </table>
    """
    st.markdown(tabla_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico de barras de pH y temperatura
    col_ph, col_cond = st.columns(2)
    with col_ph:
        fig_ph = go.Figure(data=[
            go.Bar(name="Entrada", x=["pH"],
                   y=[D["ph_e"]], marker_color=ROJO,
                   marker_line=dict(color="white", width=2),
                   text=[f"<b>{D['ph_e']:.2f}</b>"], textposition="outside",
                   textfont=dict(size=14, color=ROJO),
                   width=0.3,
                   hovertemplate="<b>pH Entrada</b><br>%{y:.2f} u pH<extra></extra>"),
            go.Bar(name="Salida", x=["pH"],
                   y=[D["ph_s"]], marker_color=VERDE,
                   marker_line=dict(color="white", width=2),
                   text=[f"<b>{D['ph_s']:.2f}</b>"], textposition="outside",
                   textfont=dict(size=14, color=VERDE_D),
                   width=0.3,
                   hovertemplate="<b>pH Salida</b><br>%{y:.2f} u pH<extra></extra>"),
        ])
        fig_ph.add_hrect(y0=6.5, y1=8.5, fillcolor="rgba(14,158,99,0.07)",
                         line_width=1.5, line_color=VERDE_O2, line_dash="dot",
                         annotation_text="Rango óptimo (6.5–8.5)",
                         annotation_position="top right",
                         annotation_font=dict(size=12, color=VERDE_D))
        fig_ph.update_layout(**{**PLOTLY_LAYOUT, "margin": dict(l=40, r=20, t=60, b=40)},
            height=310, barmode="group",
            title=dict(text="⬤ pH — Entrada vs Salida", font=dict(family="Space Grotesk", size=15, color=TEXTO)),
            yaxis=dict(range=[5.0, 10.2], gridcolor="#EDF3ED", title="Unidades de pH",
                       title_font=dict(size=12), tickfont=dict(size=12)),
            xaxis=dict(showgrid=False, tickfont=dict(size=13)),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15,
                        font=dict(size=13), bgcolor="white", bordercolor=BORDE, borderwidth=1),
            bargap=0.4,
        )
        st.plotly_chart(fig_ph, use_container_width=True)

    with col_cond:
        categorias = ["Conductividad (µS/cm)", "Alcalinidad (mg CaCO₃/L)"]
        e_vals_cond = [D["cond_e"], D["alc_e"]]
        s_vals_cond = [D["cond_s"], D["alc_s"]]
        eff_cond_vals = [eff(D["cond_e"], D["cond_s"]), eff(D["alc_e"], D["alc_s"])]

        fig_cond = go.Figure(data=[
            go.Bar(name="Entrada",
                   x=categorias, y=e_vals_cond,
                   marker_color=ROJO, marker_opacity=0.88,
                   marker_line=dict(color="white", width=2),
                   text=[f"<b>{v:.0f}</b>" for v in e_vals_cond],
                   textposition="outside", textfont=dict(size=13, color=ROJO),
                   hovertemplate="<b>%{x}</b><br>Entrada: <b>%{y:.1f}</b><extra></extra>"),
            go.Bar(name="Salida",
                   x=categorias, y=s_vals_cond,
                   marker_color=VERDE, marker_opacity=0.88,
                   marker_line=dict(color="white", width=2),
                   text=[f"<b>{v:.0f}</b>" for v in s_vals_cond],
                   textposition="outside", textfont=dict(size=13, color=VERDE_D),
                   hovertemplate="<b>%{x}</b><br>Salida: <b>%{y:.1f}</b><extra></extra>"),
        ])
        for xi, (cat, ef) in enumerate(zip(categorias, eff_cond_vals)):
            fig_cond.add_annotation(
                x=cat, y=max(e_vals_cond[xi], s_vals_cond[xi]) * 1.28,
                text=f"<b>↓{ef:.0f}%</b>",
                showarrow=False, font=dict(size=12, color=VERDE_D, family="Space Grotesk"),
                bgcolor=VERDE_O2, borderpad=3, borderwidth=0
            )
        fig_cond.update_layout(**{**PLOTLY_LAYOUT, "margin": dict(l=40, r=20, t=70, b=40)},
            height=310, barmode="group",
            title=dict(text="⬤ Conductividad y Alcalinidad", font=dict(family="Space Grotesk", size=15, color=TEXTO)),
            yaxis=dict(gridcolor="#EDF3ED", title="Concentración",
                       title_font=dict(size=12), tickfont=dict(size=12)),
            xaxis=dict(showgrid=False, tickfont=dict(size=12)),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15,
                        font=dict(size=13), bgcolor="white", bordercolor=BORDE, borderwidth=1),
            bargap=0.35,
        )
        st.plotly_chart(fig_cond, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANÁLISIS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Análisis de calidad del agua</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Distribución y comparación detallada de parámetros de tratamiento</div>', unsafe_allow_html=True)

    # Fila A — Carga orgánica
    colA, colB = st.columns(2)

    with colA:
        categorias_org = ["DBO₅", "DQO"]
        entrada_org = [D["dbo_e"], D["dqo_e"]]
        salida_org  = [D["dbo_s"], D["dqo_s"]]

        effs_org = [eff(e, s) for e, s in zip(entrada_org, salida_org)]
        fig_org = go.Figure()
        fig_org.add_trace(go.Bar(
            name="Entrada",
            x=categorias_org, y=entrada_org,
            marker=dict(color=ROJO, opacity=0.88, line=dict(color="white", width=2)),
            text=[f"<b>{v:.1f}</b>" for v in entrada_org],
            textposition="outside", textfont=dict(size=14, color=ROJO),
            hovertemplate="<b>%{x} Entrada</b><br>%{y:.1f} mg O₂/L<extra></extra>",
            width=0.35,
        ))
        fig_org.add_trace(go.Bar(
            name="Salida",
            x=categorias_org, y=salida_org,
            marker=dict(color=VERDE, opacity=0.90, line=dict(color="white", width=2)),
            text=[f"<b>{v:.1f}</b>" for v in salida_org],
            textposition="outside", textfont=dict(size=14, color=VERDE_D),
            hovertemplate="<b>%{x} Salida</b><br>%{y:.1f} mg O₂/L<extra></extra>",
            width=0.35,
        ))
        max_org = max(entrada_org)
        for xi, (cat, ef) in enumerate(zip(categorias_org, effs_org)):
            fig_org.add_annotation(
                x=cat, y=entrada_org[xi] * 1.22,
                text=f"<b>↓{ef:.1f}%</b> remoción",
                showarrow=False, font=dict(size=12, color=VERDE_D, family="Space Grotesk"),
                bgcolor=VERDE_O2, borderpad=4, borderwidth=0
            )
        fig_org.update_layout(**{**PLOTLY_LAYOUT, "margin": dict(l=40, r=20, t=75, b=40)},
            barmode="group", height=380,
            title=dict(text="⬤ Carga orgánica — Demanda de Oxígeno (mg O₂/L)", font=dict(family="Space Grotesk", size=15, color=TEXTO)),
            yaxis=dict(gridcolor="#EDF3ED", title="mg O₂/L", title_font=dict(size=13),
                       tickfont=dict(size=12), range=[0, max_org * 1.4]),
            xaxis=dict(showgrid=False, tickfont=dict(size=14, family="Space Grotesk")),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12,
                        font=dict(size=13), bgcolor="white", bordercolor=BORDE, borderwidth=1),
            bargap=0.3,
        )
        st.plotly_chart(fig_org, use_container_width=True)

    with colB:
        eff_sst_g = eff(D["sst_e"], D["sst_s"])
        eff_sed_g = eff(D["sed_e"], D["sed_s"])
        fig_sol = go.Figure()
        # Solo dos grupos: SST y Sedimentables
        fig_sol.add_trace(go.Bar(
            name="Entrada", x=["SST (mg/L)", "Sedimentables (mL/L)"],
            y=[D["sst_e"], D["sed_e"]],
            marker=dict(color=ROJO, opacity=0.88, line=dict(color="white", width=2)),
            text=[f"<b>{D['sst_e']:.0f}</b>", f"<b>{D['sed_e']:.1f}</b>"],
            textposition="outside", textfont=dict(size=14, color=ROJO),
            hovertemplate="<b>%{x} Entrada</b><br>%{y:.2f}<extra></extra>",
            width=0.35,
        ))
        fig_sol.add_trace(go.Bar(
            name="Salida", x=["SST (mg/L)", "Sedimentables (mL/L)"],
            y=[D["sst_s"], D["sed_s"]],
            marker=dict(color=VERDE, opacity=0.90, line=dict(color="white", width=2)),
            text=[f"<b>{D['sst_s']:.1f}</b>", f"<b>{D['sed_s']:.2f}</b>"],
            textposition="outside", textfont=dict(size=14, color=VERDE_D),
            hovertemplate="<b>%{x} Salida</b><br>%{y:.2f}<extra></extra>",
            width=0.35,
        ))
        for xi, (cat, ef) in enumerate(zip(["SST (mg/L)", "Sedimentables (mL/L)"], [eff_sst_g, eff_sed_g])):
            fig_sol.add_annotation(
                x=cat, y=[D["sst_e"], D["sed_e"]][xi] * 1.22,
                text=f"<b>↓{ef:.1f}%</b> remoción",
                showarrow=False, font=dict(size=12, color=VERDE_D, family="Space Grotesk"),
                bgcolor=VERDE_O2, borderpad=4, borderwidth=0
            )
        fig_sol.update_layout(**{**PLOTLY_LAYOUT, "margin": dict(l=40, r=20, t=75, b=40)},
            barmode="group", height=380,
            title=dict(text="⬤ Sólidos — SST y Sedimentables", font=dict(family="Space Grotesk", size=15, color=TEXTO)),
            yaxis=dict(gridcolor="#EDF3ED", title="Concentración", title_font=dict(size=13),
                       tickfont=dict(size=12)),
            xaxis=dict(showgrid=False, tickfont=dict(size=13, family="Space Grotesk")),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12,
                        font=dict(size=13), bgcolor="white", bordercolor=BORDE, borderwidth=1),
            bargap=0.3,
        )
        st.plotly_chart(fig_sol, use_container_width=True)

    # Fila B — Coliformes (log) y contaminantes específicos
    colC, colD = st.columns(2)

    with colC:
        cats_col = ["Coliformes Totales", "Coliformes Fecales"]
        e_col = [D["ct_e"], D["cf_e"]]
        s_col = [D["ct_s"], D["cf_s"]]
        eff_col_vals = [eff(D["ct_e"], D["ct_s"]), eff(D["cf_e"], D["cf_s"])]
        normas_col = [1000, 200]

        fig_col = go.Figure()
        fig_col.add_trace(go.Bar(
            name="Entrada (NMP/100mL)", x=cats_col, y=e_col,
            marker=dict(color=ROJO, opacity=0.88, line=dict(color="white", width=2)),
            text=[f"<b>{v:.2e}</b>" for v in e_col],
            textposition="outside", textfont=dict(size=12, color=ROJO),
            hovertemplate="<b>%{x} Entrada</b><br>%{y:,.0f} NMP/100mL<extra></extra>",
            width=0.35,
        ))
        fig_col.add_trace(go.Bar(
            name="Salida (NMP/100mL)", x=cats_col, y=s_col,
            marker=dict(color=VERDE, opacity=0.90, line=dict(color="white", width=2)),
            text=[f"<b>{v:.2e}</b>" for v in s_col],
            textposition="outside", textfont=dict(size=12, color=VERDE_D),
            hovertemplate="<b>%{x} Salida</b><br>%{y:,.0f} NMP/100mL<extra></extra>",
            width=0.35,
        ))
        for xi, (ef, norma) in enumerate(zip(eff_col_vals, normas_col)):
            fig_col.add_annotation(
                x=cats_col[xi], y=e_col[xi] * 3.5,
                text=f"<b>↓{ef:.1f}%</b> remoción",
                showarrow=False, font=dict(size=12, color=VERDE_D, family="Space Grotesk"),
                bgcolor=VERDE_O2, borderpad=4, borderwidth=0
            )
            fig_col.add_hline(y=norma, line_dash="dot", line_color=AMBAR, line_width=1.5,
                annotation_text=f"Límite {norma} NMP",
                annotation_position="right",
                annotation_font=dict(size=11, color=AMBAR))
        fig_col.update_layout(**{**PLOTLY_LAYOUT, "margin": dict(l=40, r=80, t=75, b=40)},
            barmode="group", height=380,
            title=dict(text="⬤ Coliformes — Escala logarítmica", font=dict(family="Space Grotesk", size=15, color=TEXTO)),
            yaxis=dict(type="log", gridcolor="#EDF3ED", title="NMP/100mL (escala log)",
                       title_font=dict(size=13), tickfont=dict(size=12)),
            xaxis=dict(showgrid=False, tickfont=dict(size=13, family="Space Grotesk")),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12,
                        font=dict(size=13), bgcolor="white", bordercolor=BORDE, borderwidth=1),
            bargap=0.3,
        )
        st.plotly_chart(fig_col, use_container_width=True)

    with colD:
        cats_esp = ["Grasas", "Surfactantes", "Fenoles (×100)"]
        e_vals_esp = [D["gra_e"], D["sur_e"], D["fen_e"] * 100]
        s_vals_esp = [D["gra_s"], D["sur_s"], D["fen_s"] * 100]
        eff_esp = [eff(D["gra_e"], D["gra_s"]), eff(D["sur_e"], D["sur_s"]), eff(D["fen_e"], D["fen_s"])]
        unidades_esp = ["mg/L", "mg/L", "×100 mg/L"]
        normas_esp = [20, 2, 15]  # fenoles 0.15 ×100

        fig_esp = go.Figure()
        fig_esp.add_trace(go.Bar(
            name="Entrada", x=cats_esp, y=e_vals_esp,
            marker=dict(color=ROJO, opacity=0.88, line=dict(color="white", width=2)),
            text=[f"<b>{v:.1f}</b>" for v in e_vals_esp],
            textposition="outside", textfont=dict(size=13, color=ROJO),
            hovertemplate="<b>%{x} Entrada</b><br>%{y:.2f}<extra></extra>",
            width=0.35,
        ))
        fig_esp.add_trace(go.Bar(
            name="Salida", x=cats_esp, y=s_vals_esp,
            marker=dict(color=VERDE, opacity=0.90, line=dict(color="white", width=2)),
            text=[f"<b>{v:.2f}</b>" for v in s_vals_esp],
            textposition="outside", textfont=dict(size=13, color=VERDE_D),
            hovertemplate="<b>%{x} Salida</b><br>%{y:.2f}<extra></extra>",
            width=0.35,
        ))
        for xi, (cat, ef, norma) in enumerate(zip(cats_esp, eff_esp, normas_esp)):
            fig_esp.add_annotation(
                x=cat, y=e_vals_esp[xi] * 1.22,
                text=f"<b>↓{ef:.1f}%</b>",
                showarrow=False, font=dict(size=12, color=VERDE_D, family="Space Grotesk"),
                bgcolor=VERDE_O2, borderpad=3, borderwidth=0
            )
            fig_esp.add_hline(y=norma, line_dash="dot", line_color=AMBAR, line_width=1.5)
        fig_esp.update_layout(**{**PLOTLY_LAYOUT, "margin": dict(l=40, r=20, t=75, b=40)},
            barmode="group", height=380,
            title=dict(text="⬤ Grasas, Surfactantes y Fenoles (Fenoles ×100)", font=dict(family="Space Grotesk", size=15, color=TEXTO)),
            yaxis=dict(gridcolor="#EDF3ED", title="mg/L", title_font=dict(size=13), tickfont=dict(size=12)),
            xaxis=dict(showgrid=False, tickfont=dict(size=13, family="Space Grotesk")),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12,
                        font=dict(size=13), bgcolor="white", bordercolor=BORDE, borderwidth=1),
            bargap=0.3,
        )
        st.plotly_chart(fig_esp, use_container_width=True)

    # Fila C — Diagrama de Sankey simplificado
    st.markdown('<div class="section-header" style="font-size:1rem;margin-top:10px;">Flujo de remoción de contaminantes</div>', unsafe_allow_html=True)

    # Sankey con flujo: Afluente → Removido + Efluente
    s_labels = [
        "Afluente",
        f"DBO₅ Removida<br>({eff_dbo:.1f}%)",
        f"DQO Removida<br>({eff_dqo:.1f}%)",
        f"SST Removida<br>({eff_sst:.1f}%)",
        "DBO₅ en Efluente",
        "DQO en Efluente",
        "SST en Efluente",
    ]
    s_source = [0, 0, 0, 0, 0, 0]
    s_target = [1, 4, 2, 5, 3, 6]
    s_values = [
        D["dbo_e"] - D["dbo_s"], D["dbo_s"],
        D["dqo_e"] - D["dqo_s"], D["dqo_s"],
        D["sst_e"] - D["sst_s"], D["sst_s"],
    ]
    s_colors_node = [
        "#1F4A3A",        # Afluente
        VERDE, VERDE, VERDE,  # Removidas
        ROJO, ROJO, ROJO,     # Efluentes
    ]
    s_colors_link = [
        "rgba(14,158,99,0.30)", "rgba(214,69,43,0.22)",
        "rgba(14,158,99,0.30)", "rgba(214,69,43,0.22)",
        "rgba(14,158,99,0.30)", "rgba(214,69,43,0.22)",
    ]
    fig_sank = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=28, thickness=22,
            color=s_colors_node,
            label=s_labels,
            line=dict(color="white", width=1),
            hovertemplate="<b>%{label}</b><br>Flujo: %{value:.1f}<extra></extra>",
        ),
        link=dict(
            source=s_source, target=s_target, value=s_values,
            color=s_colors_link,
            hovertemplate="Flujo: %{value:.1f}<extra></extra>",
        )
    ))
    fig_sank.update_layout(
        **{**PLOTLY_LAYOUT, "margin": dict(l=20, r=20, t=65, b=20),
           "font": dict(family="Inter", size=13, color=TEXTO)},
        height=340,
        title=dict(
            text="⬤ Flujo de remoción de contaminantes (mg/L)",
            font=dict(family="Space Grotesk", size=15, color=TEXTO),
        ),
    )
    st.plotly_chart(fig_sank, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DISEÑO
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Dimensionamiento del humedal vertical</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Parámetros de diseño calculados con criterios EPA y CEPIS para humedales verticales de flujo subsuperficial</div>', unsafe_allow_html=True)

    # Métricas de diseño
    d1, d2, d3, d4, d5 = st.columns(5)
    with d1:
        st.markdown(f"""
        <div class="design-card">
          <div class="design-icon">📐</div>
          <div class="design-val">{area:.2f}</div>
          <div class="design-unit">m² — Área superficial</div>
          <div class="design-desc">Basada en tasa de carga<br>hidráulica de 6 m²/m³·día</div>
        </div>""", unsafe_allow_html=True)
    with d2:
        st.markdown(f"""
        <div class="design-card">
          <div class="design-icon">📏</div>
          <div class="design-val">{profundidad:.2f}</div>
          <div class="design-unit">m — Profundidad</div>
          <div class="design-desc">Medio filtrante según<br>DBO₅ de entrada</div>
        </div>""", unsafe_allow_html=True)
    with d3:
        st.markdown(f"""
        <div class="design-card">
          <div class="design-icon">🧱</div>
          <div class="design-val">{volumen:.2f}</div>
          <div class="design-unit">m³ — Volumen total</div>
          <div class="design-desc">Volumen de medio<br>granular requerido</div>
        </div>""", unsafe_allow_html=True)
    with d4:
        st.markdown(f"""
        <div class="design-card">
          <div class="design-icon">⏱️</div>
          <div class="design-val">{trh:.1f}</div>
          <div class="design-unit">h — Tiempo retención</div>
          <div class="design-desc">Tiempo hidráulico de<br>retención nominal</div>
        </div>""", unsafe_allow_html=True)
    with d5:
        st.markdown(f"""
        <div class="design-card">
          <div class="design-icon">⚖️</div>
          <div class="design-val">{carga_dbo:.2f}</div>
          <div class="design-unit">kg/día — Carga DBO₅</div>
          <div class="design-desc">Carga orgánica total<br>al sistema por día</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Perfil del humedal y granulometría
    colX, colY = st.columns([3, 2])

    with colX:
        st.markdown('<div class="section-header" style="font-size:1rem;">Perfil esquemático del humedal vertical</div>', unsafe_allow_html=True)

        capas_y   = [0, 0.1, 0.25, 0.65, 0.8]
        capas_col = [MORADO, AMBAR, AZUL, "#6B8A72", AMBAR]
        capas_nom = ["Drenaje inferior", "Grava fina (4–8 mm)", "Arena media (0.5–2 mm)", "Arena gruesa (2–6 mm)", "Capa de distribución"]
        capas_esp = [0.1, 0.15, 0.40, 0.15, 0.1]

        fig_perfil = go.Figure()
        for i, (y0, col, nom, esp) in enumerate(zip(capas_y[:-1], capas_col, capas_nom, capas_esp)):
            y1 = capas_y[i+1]
            fig_perfil.add_shape(type="rect",
                x0=0.05, x1=0.95, y0=y0, y1=y1,
                fillcolor=col, opacity=0.6, line=dict(color="white", width=1))
            fig_perfil.add_annotation(x=0.5, y=(y0+y1)/2,
                text=f"<b>{nom}</b> ({esp*100:.0f} cm)", showarrow=False,
                font=dict(size=13, family="Inter", color="white"),
                bgcolor="rgba(0,0,0,0.25)", borderpad=3)

        # Flecha de flujo
        fig_perfil.add_annotation(x=0.02, y=0.8, text="▼ Entrada", showarrow=False,
            font=dict(color=VERDE, size=13, family="Space Grotesk"), xanchor="left")
        fig_perfil.add_annotation(x=0.02, y=0.0, text="▲ Salida", showarrow=False,
            font=dict(color=AMBAR, size=13, family="Space Grotesk"), xanchor="left")

        fig_perfil.update_layout(**{**PLOTLY_LAYOUT, "margin": MARGIN_DEFAULT, "plot_bgcolor": "#F8FAF8"}, height=380,
            title=dict(text=f"Corte transversal — Profundidad total: {profundidad} m", font=dict(family="Space Grotesk", size=15)),
            xaxis=dict(visible=False), yaxis=dict(title="Profundidad (m)", range=[-0.05, 0.9], gridcolor=BORDE))
        st.plotly_chart(fig_perfil, use_container_width=True)

    with colY:
        st.markdown('<div class="section-header" style="font-size:1rem;">Distribución granulométrica</div>', unsafe_allow_html=True)

        capas_lbl = ["Capa distribución<br>grava 10–20 mm", "Arena gruesa<br>2–6 mm", "Arena media<br>0.5–2 mm", "Grava fina<br>4–8 mm", "Drén inferior<br>grava 20–40 mm"]
        capas_pct = [12.5, 18.75, 50.0, 18.75, 12.5]

        fig_gran = go.Figure(go.Pie(
            labels=capas_lbl,
            values=capas_pct,
            hole=0.5,
            marker=dict(colors=[AMBAR, VERDE, AZUL, MORADO, TEAL]),
            textfont=dict(size=12, family="Inter"),
        ))
        fig_gran.update_layout(**{**PLOTLY_LAYOUT, "margin": MARGIN_DEFAULT}, height=300,
            title=dict(text="% del perfil por capa", font=dict(family="Space Grotesk", size=15)),
            showlegend=True, legend=dict(font=dict(size=12)))
        st.plotly_chart(fig_gran, use_container_width=True)

        # Dimensiones planta
        largo  = np.sqrt(area * 1.5)
        ancho  = area / largo
        st.markdown(f"""
        <div class="reporte-card" style="margin-top:0;">
          <div class="reporte-title">Dimensiones en planta</div>
          <div class="reporte-row"><span class="reporte-key">Largo recomendado</span> <span class="reporte-value">{largo:.2f} m</span></div>
          <div class="reporte-row"><span class="reporte-key">Ancho recomendado</span> <span class="reporte-value">{ancho:.2f} m</span></div>
          <div class="reporte-row"><span class="reporte-key">Relación L:W</span>       <span class="reporte-value">1.5 : 1</span></div>
          <div class="reporte-row"><span class="reporte-key">Tipo de flujo</span>      <span class="reporte-value">Subsuperficial vertical</span></div>
          <div class="reporte-row"><span class="reporte-key">Pendiente fondo</span>    <span class="reporte-value">1 – 2%</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico de sensibilidad
    st.markdown('<div class="section-header" style="font-size:1rem;margin-top:10px;">Sensibilidad del área ante variación de caudal</div>', unsafe_allow_html=True)

    caudales_rango = np.linspace(D["c_e"] * 0.4, D["c_e"] * 2.5, 80)
    areas_rango    = caudales_rango * 86.4 / tasa_carga

    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(x=caudales_rango, y=areas_rango,
        line=dict(color=VERDE, width=2.5), name="Área necesaria",
        fill="tozeroy", fillcolor=VERDE_O))
    fig_sens.add_vline(x=D["c_e"], line_dash="dash", line_color=AMBAR,
        annotation_text=f"Q actual: {D['c_e']:.3f} L/s", annotation_position="top right",
        annotation_font=dict(color=AMBAR, size=11))
    fig_sens.add_hline(y=area, line_dash="dot", line_color=ROJO,
        annotation_text=f"Área actual: {area:.2f} m²", annotation_position="bottom right",
        annotation_font=dict(color=ROJO, size=11))
    fig_sens.update_layout(**{**PLOTLY_LAYOUT, "margin": MARGIN_DEFAULT}, height=270,
        xaxis=dict(title="Caudal entrada (L/s)", gridcolor=BORDE),
        yaxis=dict(title="Área superficial (m²)", gridcolor=BORDE),
        title=dict(text=f"Área superficial requerida vs caudal (tasa: {tasa_carga} m²/m³·día)", font=dict(family="Space Grotesk", size=15)))
    st.plotly_chart(fig_sens, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — REPORTE
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Reporte técnico de diseño</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Resumen consolidado del sistema — apto para memoria de cálculo</div>', unsafe_allow_html=True)

    colR1, colR2 = st.columns(2)

    with colR1:
        st.markdown(f"""
        <div class="reporte-card">
          <div class="reporte-title">📌 Datos del proyecto</div>
          <div class="reporte-row"><span class="reporte-key">Proyecto</span>       <span class="reporte-value">{nombre_proyecto}</span></div>
          <div class="reporte-row"><span class="reporte-key">Sistema</span>        <span class="reporte-value">{poza}</span></div>
          <div class="reporte-row"><span class="reporte-key">Tipo de humedal</span><span class="reporte-value">Vertical — flujo subsuperficial</span></div>
          <div class="reporte-row"><span class="reporte-key">Norma de ref.</span>  <span class="reporte-value">EPA 832-F-00-023 / CEPIS</span></div>
        </div>

        <div class="reporte-card">
          <div class="reporte-title">💧 Hidráulica del sistema</div>
          <div class="reporte-row"><span class="reporte-key">Caudal entrada</span>      <span class="reporte-value">{D['c_e']:.4f} L/s</span></div>
          <div class="reporte-row"><span class="reporte-key">Caudal salida</span>       <span class="reporte-value">{D['c_s']:.4f} L/s</span></div>
          <div class="reporte-row"><span class="reporte-key">Caudal diario</span>       <span class="reporte-value">{caudal_dia:.3f} m³/día</span></div>
          <div class="reporte-row"><span class="reporte-key">TRH nominal</span>         <span class="reporte-value">{trh:.2f} h</span></div>
          <div class="reporte-row"><span class="reporte-key">Tasa carga hidráulica</span><span class="reporte-value">{tasa_carga:.1f} m²/m³·día</span></div>
        </div>

        <div class="reporte-card">
          <div class="reporte-title">🏗️ Dimensionamiento</div>
          <div class="reporte-row"><span class="reporte-key">Área superficial</span>  <span class="reporte-value">{area:.3f} m²</span></div>
          <div class="reporte-row"><span class="reporte-key">Profundidad medio</span> <span class="reporte-value">{profundidad:.2f} m</span></div>
          <div class="reporte-row"><span class="reporte-key">Volumen medio</span>     <span class="reporte-value">{volumen:.3f} m³</span></div>
          <div class="reporte-row"><span class="reporte-key">Carga DBO₅</span>       <span class="reporte-value">{carga_dbo:.4f} kg/día</span></div>
          <div class="reporte-row"><span class="reporte-key">Relación L:W</span>     <span class="reporte-value">1.5 : 1</span></div>
        </div>
        """, unsafe_allow_html=True)

    with colR2:
        st.markdown(f"""
        <div class="reporte-card">
          <div class="reporte-title">📊 Calidad del efluente</div>
          <div class="reporte-row"><span class="reporte-key">pH salida</span>         <span class="reporte-value">{D['ph_s']:.2f} u pH</span></div>
          <div class="reporte-row"><span class="reporte-key">DBO₅ salida</span>       <span class="reporte-value">{D['dbo_s']:.2f} mg/L</span></div>
          <div class="reporte-row"><span class="reporte-key">DQO salida</span>        <span class="reporte-value">{D['dqo_s']:.2f} mg/L</span></div>
          <div class="reporte-row"><span class="reporte-key">SST salida</span>        <span class="reporte-value">{D['sst_s']:.2f} mg/L</span></div>
          <div class="reporte-row"><span class="reporte-key">Col. Totales salida</span><span class="reporte-value">{D['ct_s']:.0f} NMP/100mL</span></div>
          <div class="reporte-row"><span class="reporte-key">Col. Fecales salida</span><span class="reporte-value">{D['cf_s']:.0f} NMP/100mL</span></div>
          <div class="reporte-row"><span class="reporte-key">Grasas salida</span>     <span class="reporte-value">{D['gra_s']:.2f} mg/L</span></div>
        </div>

        <div class="reporte-card">
          <div class="reporte-title">✅ Eficiencias de remoción</div>
          <div class="reporte-row"><span class="reporte-key">DBO₅</span>          <span class="reporte-value">{eff_dbo:.2f}%</span></div>
          <div class="reporte-row"><span class="reporte-key">DQO</span>           <span class="reporte-value">{eff_dqo:.2f}%</span></div>
          <div class="reporte-row"><span class="reporte-key">SST</span>           <span class="reporte-value">{eff_sst:.2f}%</span></div>
          <div class="reporte-row"><span class="reporte-key">Sedimentables</span> <span class="reporte-value">{eff_sed:.2f}%</span></div>
          <div class="reporte-row"><span class="reporte-key">Coliformes Totales</span><span class="reporte-value">{eff_ct:.2f}%</span></div>
          <div class="reporte-row"><span class="reporte-key">Grasas y Aceites</span> <span class="reporte-value">{eff_gra:.2f}%</span></div>
          <div class="reporte-row"><span class="reporte-key">Global (promedio)</span><span class="reporte-value">{eff_global:.2f}%</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Cumplimiento normativo
    st.markdown('<div class="section-header" style="font-size:1rem;margin-top:10px;">Verificación de cumplimiento normativo</div>', unsafe_allow_html=True)

    normas = [
        ("DBO₅ salida",         D["dbo_s"],  25,    "mg/L"),
        ("DQO salida",          D["dqo_s"],  100,   "mg/L"),
        ("SST salida",          D["sst_s"],  30,    "mg/L"),
        ("Grasas y Aceites",    D["gra_s"],  20,    "mg/L"),
        ("Surfactantes",        D["sur_s"],  2.0,   "mg/L"),
        ("Coliformes Totales",  D["ct_s"],   1000,  "NMP/100mL"),
        ("Coliformes Fecales",  D["cf_s"],   200,   "NMP/100mL"),
        ("Fenoles",             D["fen_s"],  0.15,  "mg/L"),
    ]

    colN1, colN2 = st.columns(2)
    mitad = len(normas) // 2

    for col_obj, grupo in zip([colN1, colN2], [normas[:mitad], normas[mitad:]]):
        with col_obj:
            html = '<div class="reporte-card"><div class="reporte-title">Verificación</div>'
            for param, val, lim, un in grupo:
                ok = val <= lim
                cls = "ok" if ok else "fail"
                icon = "✓" if ok else "✗"
                col_txt = VERDE_D if ok else ROJO
                badge_cls = "green" if ok else "red"
                estado = "CUMPLE" if ok else "NO CUMPLE"
                html += (
                    f'<div class="cumpl-item">'
                    f'<div class="cumpl-dot {cls}"></div>'
                    f'<div style="flex:1">'
                    f'<div style="font-weight:600;color:{TEXTO}">{param}</div>'
                    f'<div style="color:{TEXTO2};font-size:0.82rem;margin-top:2px;">'
                    f'Valor: <strong style="color:{col_txt}">{val:.3g} {un}</strong>'
                    f'&nbsp;&middot;&nbsp; Límite: {lim} {un} &nbsp;'
                    f'<span class="badge {badge_cls}">{icon} {estado}</span>'
                    f'</div></div></div>'
                )
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

    # Conclusiones
    n_cumple  = sum(1 for _, v, l, _ in normas if v <= l)
    n_total   = len(normas)
    pct_norma = n_cumple / n_total * 100

    st.markdown(f"""
    <div class="reporte-card" style="border-left: 4px solid {VERDE if pct_norma>=75 else AMBAR};">
      <div class="reporte-title">📝 Conclusiones y recomendaciones</div>
      <div style="font-size:0.85rem;line-height:1.7;color:{TEXTO}">
        <p>El sistema de humedal vertical diseñado para <strong>{nombre_proyecto}</strong> muestra una eficiencia global de remoción de 
        <strong style="color:{VERDE}">{eff_global:.1f}%</strong> sobre los parámetros principales, cumpliendo 
        <strong>{n_cumple} de {n_total}</strong> parámetros normativos evaluados ({pct_norma:.0f}%).</p>
        {"<p>⚠️ <strong>Se recomienda incluir etapa de desinfección UV o cloración</strong> previa a la descarga, dado que los coliformes superan los límites normativos de referencia.</p>" if D['ct_s'] > 1000 else "<p>✓ Los coliformes se encuentran dentro del rango normativo de referencia.</p>"}
        {"<p>⚠️ <strong>Instalar trampa de grasas</strong> en el afluente del sistema, ya que la carga de grasas de entrada supera 100 mg/L.</p>" if D['gra_e'] > 100 else ""}
        <p>El área superficial calculada de <strong>{area:.2f} m²</strong> con profundidad de medio filtrante de 
        <strong>{profundidad:.2f} m</strong> es adecuada para el caudal de diseño de <strong>{caudal_dia:.3f} m³/día</strong>.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
