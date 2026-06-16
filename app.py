import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HydroWet · Diseño de Humedales",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PALETTE ────────────────────────────────────────────────────────────────────
VERDE    = "#0E9E63"
VERDE_D  = "#0A7A4C"
VERDE_O  = "rgba(14,158,99,0.10)"
VERDE_O2 = "rgba(14,158,99,0.22)"
AMBAR    = "#C77E1A"
AMBAR_O  = "rgba(199,126,26,0.14)"
ROJO     = "#D6452B"
ROJO_O   = "rgba(214,69,43,0.13)"
AZUL     = "#2E7CC4"
MORADO   = "#7E4FC2"
OSCURO   = "#08160F"
TEAL     = "#1F4A3A"
BG_APP   = "#E9EFE9"
BG_CARD  = "#FFFFFF"
TEXTO    = "#0F1F18"
TEXTO2   = "#3A4D43"
GRIS     = "#5C6E62"
BORDE    = "#CBDBCB"
SOMBRA   = "0 2px 8px rgba(8,22,15,0.08)"

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: {TEXTO};
    font-size: 16.5px;
}}

.stApp {{
    background: linear-gradient(180deg, #EAF1EA 0%, #E2EBE2 100%);
}}
.block-container {{
    padding-top: 2rem;
    max-width: 1400px;
}}

section[data-testid="stSidebar"] {{
    background: {OSCURO} !important;
    border-right: 1px solid {TEAL};
}}
section[data-testid="stSidebar"] * {{
    color: #E6F0E6 !important;
    font-family: 'Inter', sans-serif !important;
}}
section[data-testid="stSidebar"] h3 {{
    color: #FFFFFF !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
}}
section[data-testid="stSidebar"] .stMarkdown strong {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
}}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stTextInput label,
section[data-testid="stSidebar"] .stSlider label {{
    color: #9FC4A8 !important;
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
section[data-testid="stSidebar"] input {{
    background: #11261B !important;
    border: 1px solid #2E5C46 !important;
    color: #FFFFFF !important;
    border-radius: 7px !important;
    font-weight: 500 !important;
}}
section[data-testid="stSidebar"] input:focus {{
    border-color: {VERDE} !important;
    box-shadow: 0 0 0 2px rgba(14,158,99,0.25) !important;
}}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {{
    background: #11261B !important;
    border-color: #2E5C46 !important;
}}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {{
    color: #FFFFFF !important;
}}
section[data-testid="stSidebar"] hr {{
    border-color: #234135 !important;
}}

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

.app-header {{
    background: linear-gradient(120deg, {OSCURO} 0%, {TEAL} 100%);
    border-radius: 16px;
    padding: 26px 32px;
    margin-bottom: 26px;
    display: flex;
    align-items: center;
    gap: 18px;
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

#MainMenu, footer {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}
header[data-testid="stHeader"] {{
    background: transparent;
    border-bottom: none;
}}
div[data-testid="stToolbar"] {{ display: none; }}
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

def mpl_style(ax, title=""):
    ax.set_facecolor("white")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDE)
    ax.spines['bottom'].set_color(BORDE)
    ax.tick_params(colors=TEXTO, labelsize=10)
    ax.grid(True, alpha=0.3, color=BORDE, linestyle='--')
    if title:
        ax.set_title(title, fontsize=13, fontweight='bold', color=TEXTO, pad=12)

def show_fig(fig):
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌿 HydroWet")
    st.markdown("---")
    
    modo = st.selectbox(
        "Modo de entrada",
        ["Datos de ejemplo", "Ingreso manual"],
        help="Selecciona la fuente de datos"
    )

    st.markdown("---")
    st.markdown("**Configuración del sistema**")
    
    nombre_proyecto = st.text_input("Nombre del proyecto", "Poza Séptica Piloto")
    
    st.markdown("---")
    
    if modo == "Ingreso manual":
        st.markdown("**Parámetros de entrada**")
        
        c_e = st.number_input("Caudal entrada (L/s)", 0.05, 2.0, 0.162, 0.01)
        c_s = st.number_input("Caudal salida (L/s)",  0.01, 1.0, 0.080, 0.01)
        ph_e = st.number_input("pH entrada", 5.0, 9.0, 6.67, 0.01)
        ph_s = st.number_input("pH salida",  5.0, 9.0, 7.52, 0.01)
        dbo_e = st.number_input("DBO₅ entrada (mg/L)", 10,  5000, 625,  10)
        dbo_s = st.number_input("DBO₅ salida (mg/L)",   1,   500,  41,   1)
        dqo_e = st.number_input("DQO entrada (mg/L)",   50, 10000, 1249,  50)
        dqo_s = st.number_input("DQO salida (mg/L)",    10,  1000,  98,   10)
        sst_e = st.number_input("SST entrada (mg/L)",   50, 10000, 2644, 100)
        sst_s = st.number_input("SST salida (mg/L)",     1,   200,  23,    1)
        sed_e = st.number_input("Sedimentables entrada (mL/L)",  0.0, 200.0, 69.5, 0.5)
        sed_s = st.number_input("Sedimentables salida (mL/L)",   0.0,  10.0,  0.05, 0.01)
        ct_e  = st.number_input("Col. Totales entrada (NMP/100mL)", 100, 10000000, 4551472, 10000)
        ct_s  = st.number_input("Col. Totales salida (NMP/100mL)",   10,  1000000,  393170,  1000)
        cf_e  = st.number_input("Col. Fecales entrada (NMP/100mL)",   10,  1000000,  337465, 10000)
        cf_s  = st.number_input("Col. Fecales salida (NMP/100mL)",     1,   100000,   18009,  1000)
        fen_e = st.number_input("Fenoles entrada (mg/L)", 0.0, 2.0, 0.182, 0.001)
        fen_s = st.number_input("Fenoles salida (mg/L)",  0.0, 0.5, 0.150, 0.001)
        gra_e = st.number_input("Grasas entrada (mg/L)", 0, 5000, 1349, 50)
        gra_s = st.number_input("Grasas salida (mg/L)",  0,  200,   13,  1)
        sur_e = st.number_input("Surfactantes entrada (mg/L)", 0.0, 20.0, 4.92, 0.01)
        sur_s = st.number_input("Surfactantes salida (mg/L)",  0.0, 10.0, 1.96, 0.01)
        temp  = st.number_input("Temperatura (°C)", 20.0, 35.0, 29.1, 0.1)
        cond_e = st.number_input("Conductividad entrada (µS/cm)", 100, 3000, 1052, 10)
        cond_s = st.number_input("Conductividad salida (µS/cm)",  100, 2000, 891,  10)
        alc_e = st.number_input("Alcalinidad entrada (mg CaCO₃/L)", 50, 1000, 316, 5)
        alc_s = st.number_input("Alcalinidad salida (mg CaCO₃/L)",  50,  800, 247, 5)
        
    st.markdown("---")
    st.markdown('<span style="color:#7FA889;font-size:0.74rem;font-weight:500;">HydroWet v1.0 · 2025</span>', unsafe_allow_html=True)


# ─── SELECTOR POZA ──────────────────────────────────────────────────────────────
poza = st.selectbox("Poza de referencia", ["Poza #1", "Poza #2"])


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

# Cálculos de diseño
np.random.seed(42)
caudal_dia   = D["c_e"] * 86.4
tasa_carga   = 6.0
area         = caudal_dia / tasa_carga
profundidad  = 0.8 if D["dbo_e"] > 800 else (0.65 if D["dbo_e"] > 200 else 0.5)
volumen      = area * profundidad
trh          = volumen / caudal_dia * 24
carga_dbo    = D["dbo_e"] * D["c_e"] * 86.4 / 1000

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
st.markdown(f"""
<div class="app-header">
  <div class="app-logo">🌿</div>
  <div>
    <div class="app-title">HydroWet · Diseño de Humedales Verticales</div>
    <div class="app-subtitle">{nombre_proyecto} &nbsp;·&nbsp; {D['poza']} &nbsp;·&nbsp; 
    Eficiencia global promedio: <strong>{eff_global:.1f}%</strong></div>
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
        params  = ["DBO₅", "DQO", "SST", "Sediment.", "Col.Tot.", "Col.Fec.", "Grasas", "Surfact."]
        valores = [eff_dbo, eff_dqo, eff_sst, eff_sed, eff_ct, eff_cf, eff_gra, eff_sur]

        angles = np.linspace(0, 2 * np.pi, len(params), endpoint=False).tolist()
        valores_cerrados = valores + [valores[0]]
        angles_cerrados = angles + [angles[0]]

        fig_radar, ax_r = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax_r.set_facecolor("#F8FAF8")
        ax_r.fill(angles_cerrados, valores_cerrados, color=VERDE, alpha=0.15)
        ax_r.plot(angles_cerrados, valores_cerrados, color=VERDE, linewidth=2, marker='o', markersize=5)
        ax_r.set_thetagrids(np.degrees(angles), params, fontsize=10, color=TEXTO)
        ax_r.set_ylim(0, 100)
        ax_r.set_rticks([20, 40, 60, 80, 100])
        ax_r.set_yticklabels(["20%", "40%", "60%", "80%", "100%"], fontsize=8, color=GRIS)
        ax_r.spines['polar'].set_color(BORDE)
        ax_r.tick_params(colors=TEXTO)
        ax_r.set_title("Perfil de eficiencias", fontsize=14, fontweight='bold', color=TEXTO, pad=20)
        legend_patch = mpatches.Patch(color=VERDE, alpha=0.3, label='Eficiencia por parámetro')
        ax_r.legend(handles=[legend_patch], loc='lower right', bbox_to_anchor=(1.15, -0.05),
                   fontsize=10, frameon=True, edgecolor=BORDE)
        show_fig(fig_radar)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="font-size:1rem;">Tendencia mensual simulada (30 días)</div>', unsafe_allow_html=True)

    dias = np.arange(1, 31)
    var  = np.random.normal(1, 0.07, 30)
    dbo_ent_t = np.clip(D["dbo_e"] * var, D["dbo_e"]*0.75, D["dbo_e"]*1.25)
    dbo_sal_t = np.clip(D["dbo_s"] * np.random.normal(1, 0.12, 30), D["dbo_s"]*0.5, D["dbo_s"]*1.6)

    fig_trend, ax_t = plt.subplots(figsize=(10, 3.5))
    mpl_style(ax_t, "DBO₅ Entrada vs Salida (mg/L)")
    ax_t.fill_between(dias, dbo_ent_t, dbo_sal_t, alpha=0.08, color=VERDE)
    ax_t.plot(dias, dbo_ent_t, color=ROJO, linewidth=2, marker='o', markersize=3, label="DBO₅ Entrada")
    ax_t.plot(dias, dbo_sal_t, color=VERDE, linewidth=2, marker='o', markersize=3, label="DBO₅ Salida")
    ax_t.axhline(y=25, color=AMBAR, linestyle='--', linewidth=1.5, label="Límite norma 25 mg/L")
    ax_t.set_xlabel("Día", fontsize=11, color=TEXTO)
    ax_t.set_ylabel("mg O₂/L", fontsize=11, color=TEXTO)
    ax_t.legend(fontsize=10, frameon=True, edgecolor=BORDE, facecolor='white')
    show_fig(fig_trend)


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

    col_ph, col_cond = st.columns(2)
    with col_ph:
        fig_ph, ax = plt.subplots(figsize=(6, 3.2))
        mpl_style(ax, "pH — Entrada vs Salida")
        x = np.array([0])
        w = 0.35
        ax.bar(x - w/2, [D["ph_e"]], w, color=ROJO, label="Entrada", edgecolor='white')
        ax.bar(x + w/2, [D["ph_s"]], w, color=VERDE, label="Salida", edgecolor='white')
        ax.text(x[0] - w/2, D["ph_e"] + 0.08, f'{D["ph_e"]:.2f}', ha='center', fontsize=9, color=TEXTO, fontweight='bold')
        ax.text(x[0] + w/2, D["ph_s"] + 0.08, f'{D["ph_s"]:.2f}', ha='center', fontsize=9, color=TEXTO, fontweight='bold')
        ax.axhspan(6.5, 8.5, alpha=0.08, color=VERDE)
        ax.text(0.02, 8.7, "Rango óptimo 6.5–8.5", fontsize=8, color=GRIS, transform=ax.get_xaxis_transform())
        ax.set_xticks(x)
        ax.set_xticklabels(["pH"])
        ax.set_ylim(5.5, 9.5)
        ax.legend(fontsize=10, frameon=True, edgecolor=BORDE, facecolor='white')
        show_fig(fig_ph)

    with col_cond:
        categorias = ["Conductividad", "Alcalinidad"]
        fig_cond, ax = plt.subplots(figsize=(6, 3.2))
        mpl_style(ax, "Conductividad (µS/cm) y Alcalinidad (mg CaCO₃/L)")
        x = np.arange(len(categorias))
        w = 0.35
        ax.bar(x - w/2, [D["cond_e"], D["alc_e"]], w, color=ROJO, label="Entrada", edgecolor='white')
        ax.bar(x + w/2, [D["cond_s"], D["alc_s"]], w, color=VERDE, label="Salida", edgecolor='white')
        ax.set_xticks(x)
        ax.set_xticklabels(categorias)
        ax.legend(fontsize=10, frameon=True, edgecolor=BORDE, facecolor='white')
        show_fig(fig_cond)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANÁLISIS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Análisis de calidad del agua</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Distribución y comparación detallada de parámetros de tratamiento</div>', unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:
        categorias_org = ["DBO₅", "DQO"]
        entrada_org = [D["dbo_e"], D["dqo_e"]]
        salida_org  = [D["dbo_s"], D["dqo_s"]]

        fig_org, ax = plt.subplots(figsize=(6, 4))
        mpl_style(ax, "Carga orgánica (mg O₂/L)")
        x = np.arange(len(categorias_org))
        w = 0.35
        bars1 = ax.bar(x - w/2, entrada_org, w, color=ROJO, label="Entrada", alpha=0.85, edgecolor='white')
        bars2 = ax.bar(x + w/2, salida_org, w, color=VERDE, label="Salida", edgecolor='white')
        for bar in bars1:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
                   f'{bar.get_height():.1f}', ha='center', fontsize=9, color=TEXTO, fontweight='bold')
        for bar in bars2:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
                   f'{bar.get_height():.1f}', ha='center', fontsize=9, color=TEXTO, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categorias_org)
        ax.legend(fontsize=10, frameon=True, edgecolor=BORDE, facecolor='white')
        show_fig(fig_org)

    with colB:
        fig_sol, ax = plt.subplots(figsize=(6, 4))
        mpl_style(ax, "Sólidos totales: SST (mg/L) y Sedimentables (mL/L)")
        cats = ["SST Entrada", "SST Salida", "Sed. Entrada", "Sed. Salida"]
        vals = [D["sst_e"], D["sst_s"], D["sed_e"], D["sed_s"]]
        cols = [ROJO, VERDE, ROJO, VERDE]
        bars = ax.bar(cats, vals, color=cols, edgecolor='white')
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(vals)*0.02,
                   f'{v:.1f}', ha='center', fontsize=9, color=TEXTO, fontweight='bold')
        ax.tick_params(axis='x', rotation=15)
        legend_elements = [mpatches.Patch(facecolor=ROJO, label='Entrada'),
                          mpatches.Patch(facecolor=VERDE, label='Salida')]
        ax.legend(handles=legend_elements, fontsize=10, frameon=True, edgecolor=BORDE, facecolor='white')
        show_fig(fig_sol)

    colC, colD = st.columns(2)

    with colC:
        cats_col = ["Col. Totales", "Col. Fecales"]
        fig_col, ax = plt.subplots(figsize=(6, 4))
        mpl_style(ax, "Coliformes (NMP/100mL) — escala logarítmica")
        x = np.arange(len(cats_col))
        w = 0.35
        ax.bar(x - w/2, [D["ct_e"], D["cf_e"]], w, color=ROJO, label="Entrada", alpha=0.85, edgecolor='white')
        ax.bar(x + w/2, [D["ct_s"], D["cf_s"]], w, color=VERDE, label="Salida", edgecolor='white')
        ax.set_yscale('log')
        ax.set_xticks(x)
        ax.set_xticklabels(cats_col)
        ax.set_ylabel("NMP/100mL (log)", fontsize=11, color=TEXTO)
        ax.legend(fontsize=10, frameon=True, edgecolor=BORDE, facecolor='white')
        show_fig(fig_col)

    with colD:
        cats_esp = ["Grasas\n(mg/L)", "Surfactantes\n(mg/L)", "Fenoles\n(×100)"]
        e_vals = [D["gra_e"], D["sur_e"], D["fen_e"] * 100]
        s_vals = [D["gra_s"], D["sur_s"], D["fen_s"] * 100]

        fig_esp, ax = plt.subplots(figsize=(6, 4))
        mpl_style(ax, "Contaminantes específicos (Fenoles ×100 para escala)")
        x = np.arange(len(cats_esp))
        ax.fill_between(x, e_vals, alpha=0.07, color=ROJO)
        ax.fill_between(x, s_vals, alpha=0.10, color=VERDE)
        ax.plot(x, e_vals, color=ROJO, linewidth=2, marker='o', markersize=8, label="Entrada")
        ax.plot(x, s_vals, color=VERDE, linewidth=2, marker='o', markersize=8, label="Salida")
        ax.set_xticks(x)
        ax.set_xticklabels(cats_esp)
        ax.legend(fontsize=10, frameon=True, edgecolor=BORDE, facecolor='white')
        show_fig(fig_esp)




# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DISEÑO
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Dimensionamiento del humedal vertical</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Parámetros de diseño calculados con criterios EPA y CEPIS para humedales verticales de flujo subsuperficial</div>', unsafe_allow_html=True)

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

    colX, colY = st.columns([3, 2])

    with colX:
        st.markdown('<div class="section-header" style="font-size:1rem;">Perfil esquemático del humedal vertical</div>', unsafe_allow_html=True)

        capas_y   = [0, 0.1, 0.25, 0.65, 0.8]
        capas_col = [MORADO, AMBAR, AZUL, "#6B8A72", AMBAR]
        capas_nom = ["Drenaje inferior", "Grava fina (4–8 mm)", "Arena media (0.5–2 mm)", "Arena gruesa (2–6 mm)", "Capa de distribución"]
        capas_esp = [0.1, 0.15, 0.40, 0.15, 0.1]

        fig_perfil, ax = plt.subplots(figsize=(7, 5))
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.05, 0.9)
        ax.set_facecolor("#F8FAF8")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])

        for i, (y0, col, nom, esp) in enumerate(zip(capas_y[:-1], capas_col, capas_nom, capas_esp)):
            y1 = capas_y[i+1]
            rect = plt.Rectangle((0.05, y0), 0.90, y1-y0, facecolor=col, alpha=0.6, edgecolor='white', linewidth=1)
            ax.add_patch(rect)
            ax.text(0.5, (y0+y1)/2, f"{nom} ({esp*100:.0f} cm)", ha='center', va='center',
                   fontsize=10, color='white', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.25, edgecolor='none'))

        ax.text(0.02, 0.82, "▼ Entrada", fontsize=11, color=VERDE, fontweight='bold', va='top')
        ax.text(0.02, 0.02, "▲ Salida", fontsize=11, color=AMBAR, fontweight='bold', va='bottom')
        ax.set_ylabel("Profundidad (m)", fontsize=11, color=TEXTO)
        ax.set_title(f"Corte transversal — Profundidad total: {profundidad} m", fontsize=13, fontweight='bold', color=TEXTO, pad=12)
        show_fig(fig_perfil)

    with colY:
        st.markdown('<div class="section-header" style="font-size:1rem;">Distribución granulométrica</div>', unsafe_allow_html=True)

        capas_lbl = ["Capa distribución\ngrava 10–20 mm", "Arena gruesa\n2–6 mm", "Arena media\n0.5–2 mm", "Grava fina\n4–8 mm", "Drén inferior\ngrava 20–40 mm"]
        capas_pct = [12.5, 18.75, 50.0, 18.75, 12.5]
        capas_colors = [AMBAR, VERDE, AZUL, MORADO, TEAL]

        fig_gran, ax = plt.subplots(figsize=(5, 4))
        wedges, texts, autotexts = ax.pie(
            capas_pct, labels=capas_lbl, autopct='%1.1f%%',
            colors=capas_colors, startangle=90, pctdistance=0.75,
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
            textprops=dict(fontsize=8, color=TEXTO)
        )
        for t in autotexts:
            t.set_fontsize(8)
            t.set_fontweight('bold')
            t.set_color(TEXTO)
        ax.set_title("% del perfil por capa", fontsize=13, fontweight='bold', color=TEXTO, pad=12)
        ax.legend(wedges, capas_lbl, loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8, frameon=True, edgecolor=BORDE)
        show_fig(fig_gran)

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

    st.markdown('<div class="section-header" style="font-size:1rem;margin-top:10px;">Sensibilidad del área ante variación de caudal</div>', unsafe_allow_html=True)

    caudales_rango = np.linspace(D["c_e"] * 0.4, D["c_e"] * 2.5, 80)
    areas_rango    = caudales_rango * 86.4 / tasa_carga

    fig_sens, ax = plt.subplots(figsize=(10, 3.5))
    mpl_style(ax, f"Área superficial requerida vs caudal (tasa: {tasa_carga} m²/m³·día)")
    ax.fill_between(caudales_rango, areas_rango, alpha=0.10, color=VERDE)
    ax.plot(caudales_rango, areas_rango, color=VERDE, linewidth=2.5, label="Área necesaria")
    ax.axvline(x=D["c_e"], color=AMBAR, linestyle='--', linewidth=1.5,
              label=f"Q actual: {D['c_e']:.3f} L/s")
    ax.axhline(y=area, color=ROJO, linestyle=':', linewidth=1.5,
              label=f"Área actual: {area:.2f} m²")
    ax.set_xlabel("Caudal entrada (L/s)", fontsize=11, color=TEXTO)
    ax.set_ylabel("Área superficial (m²)", fontsize=11, color=TEXTO)
    ax.legend(fontsize=10, frameon=True, edgecolor=BORDE, facecolor='white')
    show_fig(fig_sens)


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
          <div class="reporte-row"><span class="reporte-key">Sistema</span>        <span class="reporte-value">{D['poza']}</span></div>
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
