[13:57, 24/03/2026] Dioney Benfica Roteirizador: import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
import os
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Devoluções Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS Global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    font-family: '…
[10:19, 26/03/2026] Dioney Benfica Roteirizador: 798882 - super bastos (TOP)
[15:48, 26/03/2026] Dioney Benfica Roteirizador: import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
from datetime import datetime, date

st.set_page_config(
    page_title="Gestão de Devoluções Delly's",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');
,::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,.stApp{font-family:'Space Grotesk',sans-serif;color:#e2e8f0;background:#060d1f;}
.bg-overlay{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;}
.bg-img{position:absolute;inset:0;width:100%;height:100%;
  background-image:url('https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1920&q=80');
  background-size:cover;background-position:center center;
  filter:blur(3px) brightness(0.38) saturate(0.6);transform:scale(1.06);}
.bg-tint{position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(4,9,20,0.70) 0%,rgba(6,14,35,0.62) 50%,rgba(4,12,28,0.72) 100%);}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stToolbar"]{background:transparent!important;}
[data-testid="stAppViewContainer"]>section{background:transparent!important;}
.main .block-container{position:relative;z-index:1;}
#MainMenu,footer,header{visibility:hidden!important;display:none!important;}
.stDeployButton{display:none!important;}

[data-testid="stStatusWidget"]{display:none!important;visibility:hidden!important;}
[data-testid="stToolbar"]{display:none!important;visibility:hidden!important;}
[data-testid="stHeader"]{display:none!important;visibility:hidden!important;}
[data-testid="stDecoration"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
iframe[title="streamlit_cloud_info"]{display:none!important;}
div[class*="StatusWidget"]{display:none!important;}
div[class*="viewerBadge"]{display:none!important;}
div[class*="streamlit-badge"]{display:none!important;}
.viewerBadge_container__1QSob{display:none!important;}
.styles_viewerBadge_1yB5{display:none!important;}
#stDecoration{display:none!important;}
.stApp > header{display:none!important;}
[data-baseweb="avatar"]{display:none!important;}
[aria-label*="user"],[aria-label*="profile"],[aria-label*="account"]{display:none!important;}
button[kind="header"]{display:none!important;}
div[class*="badge"]{display:none!important;}
a[href*="streamlit.io"]{pointer-events:none!important;opacity:0!important;}

/* ══ TOPBAR ══════════════════════════════════════════════════ */
.topbar{
  background:linear-gradient(100deg,rgba(4,10,26,0.98) 0%,rgba(7,18,44,0.98) 60%,rgba(5,14,34,0.98) 100%);
  border-bottom:1px solid rgba(56,189,248,0.18);
  padding:0 48px;
  height:88px;
  display:flex;align-items:center;justify-content:flex-start;
  margin:-6rem -1rem 0;
  position:sticky;top:0;z-index:999;
  backdrop-filter:blur(28px);
  box-shadow:0 2px 60px rgba(0,0,0,0.75),0 1px 0 rgba(56,189,248,0.08);}

.topbar-inner{display:flex;align-items:center;gap:24px;width:100%;}

.topbar-icon{
  width:52px;height:52px;
  background:linear-gradient(135deg,#0284c7 0%,#1d4ed8 100%);
  border-radius:14px;
  display:flex;align-items:center;justify-content:center;
  font-size:24px;flex-shrink:0;
  box-shadow:0 0 0 1px rgba(56,189,248,0.25),0 0 24px rgba(14,165,233,0.4);}

.topbar-divider{
  width:1px;height:48px;
  background:linear-gradient(180deg,transparent,rgba(56,189,248,0.3),transparent);
  flex-shrink:0;margin:0 4px;}

.topbar-text{display:flex;flex-direction:column;justify-content:center;gap:4px;}

.topbar-title{
  font-family:'Bebas Neue',sans-serif!important;
  font-size:2.15rem!important;
  font-weight:400!important;
  color:#f8fafc!important;
  letter-spacing:0.18em;
  line-height:1;
  margin:0!important;
  text-shadow:0 0 32px rgba(56,189,248,0.28),0 2px 8px rgba(0,0,0,0.6);}

.topbar-sub{
  font-family:'Space Grotesk',sans-serif;
  font-size:0.64rem;
  color:#334e6e;
  font-weight:600;
  letter-spacing:0.22em;
  text-transform:uppercase;
  margin:0;}

.filter-bar{background:linear-gradient(135deg,rgba(10,18,42,0.93),rgba(12,22,50,0.93));
  border:1px solid rgba(56,189,248,0.2);border-radius:18px;padding:20px 28px 16px;
  margin:20px 0 20px;backdrop-filter:blur(14px);box-shadow:0 4px 30px rgba(0,0,0,0.35);}
.filter-bar-title{font-family:'Bebas Neue',sans-serif;font-size:0.92rem;color:#7dd3fc;
  letter-spacing:0.14em;margin-bottom:14px;display:flex;align-items:center;gap:8px;}

.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:28px;}
.kpi-grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:28px;}
.kpi-card{background:linear-gradient(135deg,rgba(13,31,60,0.9),rgba(15,36,68,0.9));
  border:1px solid rgba(56,189,248,0.14);border-radius:18px;padding:20px 22px;
  position:relative;overflow:hidden;transition:border-color .3s,transform .3s,box-shadow .3s;
  backdrop-filter:blur(10px);}
.kpi-card:hover{border-color:rgba(56,189,248,0.46);transform:translateY(-4px);
  box-shadow:0 12px 40px rgba(14,165,233,0.16);}
.kpi-card::before{content:'';position:absolute;top:-40px;right:-40px;width:110px;height:110px;
  border-radius:50%;background:radial-gradient(circle,rgba(56,189,248,0.07),transparent 70%);}
.kpi-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(56,189,248,0.42),transparent);}
.kpi-icon{font-size:1.4rem;margin-bottom:10px;}
.kpi-label{font-size:0.67rem;color:#64748b;font-weight:600;letter-spacing:0.08em;
  text-transform:uppercase;margin-bottom:7px;}
.kpi-value{font-family:'Bebas Neue',sans-serif;font-size:1.65rem;font-weight:400;
  color:#38bdf8;line-height:1;letter-spacing:0.03em;}
.kpi-value-green{font-family:'Bebas Neue',sans-serif;font-size:1.65rem;font-weight:400;
  color:#4ade80;line-height:1;letter-spacing:0.03em;}
.kpi-value-amber{font-family:'Bebas Neue',sans-serif;font-size:1.65rem;font-weight:400;
  color:#f59e0b;line-height:1;letter-spacing:0.03em;}
.kpi-sub{font-size:0.67rem;color:#475569;margin-top:7px;}

.sec-header{display:flex;align-items:center;gap:12px;margin-bottom:16px;}
.sec-header .bar{width:3px;height:24px;background:linear-gradient(180deg,#38bdf8,#2563eb);
  border-radius:2px;box-shadow:0 0 10px rgba(56,189,248,0.5);}
.sec-header .bar-green{width:3px;height:24px;background:linear-gradient(180deg,#4ade80,#16a34a);
  border-radius:2px;box-shadow:0 0 10px rgba(74,222,128,0.5);}
.sec-header h3{font-family:'Bebas Neue',sans-serif;font-size:1.05rem;font-weight:400;
  color:#e2e8f0;margin:0;letter-spacing:0.1em;}

.stTabs [data-baseweb="tab-list"]{background:rgba(8,15,35,0.87)!important;
  border-radius:16px!important;padding:5px!important;gap:4px!important;
  border:1px solid rgba(56,189,248,0.17)!important;margin-bottom:6px;backdrop-filter:blur(10px);}
.stTabs [data-baseweb="tab"]{background:transparent!important;border-radius:12px!important;
  color:#64748b!important;font-weight:600!important;font-size:0.84rem!important;
  padding:10px 24px!important;transition:all .25s!important;border:none!important;letter-spacing:.04em;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#0c4a6e,#1e3a8a)!important;
  color:#e0f2fe!important;box-shadow:0 2px 20px rgba(14,165,233,0.3)!important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:26px!important;}

.stTextInput input,.stDateInput input{background:rgba(8,15,35,0.87)!important;
  border-color:rgba(56,189,248,0.22)!important;border-radius:10px!important;
  color:#e2e8f0!important;font-family:'Space Grotesk',sans-serif!important;}
.stTextInput input:focus{border-color:rgba(56,189,248,0.52)!important;
  box-shadow:0 0 0 3px rgba(56,189,248,0.1)!important;}
.stSelectbox div[data-baseweb="select"]>div,.stMultiSelect div[data-baseweb="select"]>div{
  background:rgba(8,15,35,0.87)!important;border-color:rgba(56,189,248,0.22)!important;
  border-radius:10px!important;color:#e2e8f0!important;}
.stMultiSelect span[data-baseweb="tag"]{background:rgba(14,165,233,0.18)!important;
  color:#38bdf8!important;border-radius:6px!important;}
label,.stSelectbox label,.stMultiSelect label,.stTextInput label,.stDateInput label{
  color:#94a3b8!important;font-size:0.76rem!important;font-weight:600!important;
  letter-spacing:.06em!important;text-transform:uppercase!important;}

.stButton>button{background:linear-gradient(135deg,#0c4a6e,#1e3a8a)!important;
  color:#e0f2fe!important;border:1px solid rgba(56,189,248,0.3)!important;
  border-radius:10px!important;font-weight:600!important;font-size:0.84rem!important;
  padding:10px 24px!important;transition:all .25s!important;
  font-family:'Space Grotesk',sans-serif!important;letter-spacing:.04em;}
.stButton>button:hover{background:linear-gradient(135deg,#1e3a8a,#1d4ed8)!important;
  border-color:rgba(56,189,248,0.62)!important;transform:translateY(-2px)!important;
  box-shadow:0 6px 24px rgba(14,165,233,0.26)!important;}
.stDownloadButton>button{background:rgba(34,197,94,0.1)!important;color:#4ade80!important;
  border:1px solid rgba(34,197,94,0.3)!important;border-radius:10px!important;font-weight:600!important;}

.stDataFrame{border-radius:14px!important;overflow:hidden!important;
  border:1px solid rgba(56,189,248,0.13)!important;}
[data-testid="stDataFrame"] iframe{background:#060d1f!important;}
.stDataFrame [data-testid="stDataFrameGlideDataEditor"]{background:#07111f!important;}
div[data-testid="stDataFrame"]>div{background:rgba(7,17,40,0.97)!important;
  border:1px solid rgba(56,189,248,0.15)!important;border-radius:14px!important;}
.stDataFrame canvas{background:#07111f!important;}
.glide-data-grid-container{background:#07111f!important;}
.stRadio label{color:#94a3b8!important;font-size:0.85rem!important;}
hr{border-color:rgba(56,189,248,0.08)!important;margin:22px 0!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:rgba(6,13,31,0.5);}
::-webkit-scrollbar-thumb{background:#1e3a8a;border-radius:3px;}
[data-testid="stDataFrame"]{
  background:rgba(6,13,31,0.96)!important;
  border:1px solid rgba(56,189,248,0.18)!important;
  border-radius:14px!important;
  overflow:hidden!important;}
[data-testid="stDataFrame"] > div {
  background:rgba(6,13,31,0.96)!important;
  border-radius:14px!important;}
[data-testid="stDataFrame"] div[role="grid"]{
  background:rgba(6,13,31,0.96)!important;}
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] [role="columnheader"]{
  background:rgba(12,26,58,0.98)!important;
  color:#38bdf8!important;
  font-weight:700!important;
  border-bottom:1px solid rgba(56,189,248,0.22)!important;}
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] [role="gridcell"]{
  background:rgba(6,13,31,0.96)!important;
  color:#cbd5e1!important;
  border-bottom:1px solid rgba(56,189,248,0.06)!important;}
[data-testid="stDataFrame"] tr:hover td{
  background:rgba(14,165,233,0.08)!important;}
[data-testid="stMetric"]{background:rgba(13,31,60,0.72)!important;
  border:1px solid rgba(56,189,248,0.13)!important;border-radius:14px!important;
  padding:14px!important;backdrop-filter:blur(8px);}
[data-testid="stMetricValue"]{font-family:'Bebas Neue',sans-serif!important;
  color:#38bdf8!important;letter-spacing:.05em!important;}
[data-testid="stMetricLabel"]{color:#64748b!important;font-size:.74rem!important;}
.stCaption{color:#475569!important;font-size:.72rem!important;}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except:
        return "R$ 0,00"

def plotly_dark(fig, height=None, margin_b=40):
    u = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,0.015)",
             font=dict(color="#94a3b8",family="Space Grotesk"),coloraxis_showscale=False,
             margin=dict(t=24,b=margin_b,l=8,r=12),
             xaxis=dict(tickfont=dict(color="#64748b",size=10),
                        gridcolor="rgba(255,255,255,0.04)",linecolor="rgba(255,255,255,0.06)"),
             yaxis=dict(tickfont=dict(color="#64748b",size=10),
                        gridcolor="rgba(255,255,255,0.04)",linecolor="rgba(255,255,255,0.06)"),
             legend=dict(bgcolor="rgba(8,15,35,0.9)",bordercolor="rgba(56,189,248,0.15)",
                         borderwidth=1,font=dict(color="#94a3b8",size=11)))
    if height: u["height"] = height
    fig.update_layout(**u)
    return fig

BLUE  = ["#0c4a6e","#0369a1","#0ea5e9","#7dd3fc","#bae6fd"]
RED   = ["#7f1d1d","#b91c1c","#ef4444","#fca5a5"]
GREEN = ["#14532d","#15803d","#22c55e","#86efac","#bbf7d0"]
MIXED = ["#0ea5e9","#22c55e","#f59e0b","#ef4444","#a855f7","#ec4899","#14b8a6","#f97316"]

SHEET_ID    = "1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI"
GSHEETS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}"
REENTREGAS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=8261-REENTREGAS%202026"

@st.cache_data(ttl=60)
def load_data(url):
    r = requests.get(url, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

# ── Carrega planilha devoluções ───────────────────────────────────────────────
with st.spinner("⏳ Carregando dados..."):
    try:
        df_raw = load_data(GSHEETS_URL)
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados de devoluções: {e}")
        st.stop()

# ── Carrega planilha reentregas ───────────────────────────────────────────────
df_reent_raw = None
reent_load_error = None
try:
    df_reent_raw = load_data(REENTREGAS_URL)
except Exception as e:
    reent_load_error = str(e)

# ── Normaliza colunas devoluções ──────────────────────────────────────────────
df_raw.columns = [str(c).strip().upper().replace(" ","_") for c in df_raw.columns]
actual_cols = list(df_raw.columns)

def get_col(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None

VALOR_COL     = get_col(df_raw, ["VLT","VLTOTAL","VL_TOTAL","VALOR_LIQUIDO","VALOR","TOTAL","VLF"]) or "VLT"
COL_PLACA     = get_col(df_raw, ["PLACA","PLACA_VEICULO","VEICULO"])
COL_MOTIVO    = get_col(df_raw, ["MOTIVO","MOTIVO_DEVOLUCAO","MOTIVO_DEV","CONF_MATRICULA"])
COL_CLIENTE   = get_col(df_raw, ["CLIENTE","NOMERCA","NOME_CLIENTE","RAZAO_SOCIAL"])
COL_VENDEDOR  = get_col(df_raw, ["NOMERCA","VENDEDOR","NOME_VENDEDOR"])
COL_DEVOLUCION= get_col(df_raw, ["NOMEFUNC","DEVOLUCIONISTA","FUNCIONARIO","NOME_FUNC"])
COL_MOTORISTA = get_col(df_raw, ["MOTORISTA","ENTREGADOR"])
COL_DESTINO   = get_col(df_raw, ["DESTINO","CIDADE","MUNICIPIO","PRACA","CODPRA"])
COL_NF_VENDA  = get_col(df_raw, ["NOTA_VENDA","NF_VENDA","NF_SAIDA","NOTA_SAIDA","NOTA_FISCAL","NUMERO"])
COL_NUMCAR    = get_col(df_raw, ["NUMCAR","NUM_CARREGAMENTO","CARREGAMENTO","NR_CARREGAMENTO"])
COL_CODCLI    = get_col(df_raw, ["CODCLI","COD_CLI","CLI","NUM_PEDIDO","PEDIDO"])
COL_DTSAIDA   = get_col(df_raw, ["DTSAIDA","DATA_DEVOLUCAO","DATA","DT_DEVOLUCAO","DATA_EMISSAO"])
COL_DTENTREGA = get_col(df_raw, ["DTENT","DTENTREGA","DATA_ENTREGA","DT_ENTREGA","DATAENTREGA","DATA_ENTREGA_REAL"])

if VALOR_COL not in df_raw.columns:
    df_raw[VALOR_COL] = 0.0

def parse_brl(s):
    s = str(s).replace("R$","").strip()
    if "," in s and "." in s:
        s = s.replace(".","").replace(",",".")
    elif "," in s:
        s = s.replace(",",".")
    return pd.to_numeric(s, errors="coerce")

df_raw[VALOR_COL] = df_raw[VALOR_COL].apply(parse_brl).fillna(0)
for col in df_raw.columns:
    if col != VALOR_COL:
        df_raw[col] = df_raw[col].fillna("").astype(str).str.strip()

if COL_DTENTREGA:
    df_raw["_DTENTREGA_DT"] = pd.to_datetime(df_raw[COL_DTENTREGA], dayfirst=True, errors="coerce")
    mask_nat = df_raw["_DTENTREGA_DT"].isna() & (df_raw[COL_DTENTREGA] != "")
    if mask_nat.any():
        alt = pd.to_datetime(df_raw.loc[mask_nat, COL_DTENTREGA], format="%Y-%m-%d", errors="coerce")
        df_raw.loc[mask_nat, "_DTENTREGA_DT"] = alt
else:
    df_raw["_DTENTREGA_DT"] = pd.NaT

# ── Normaliza colunas reentregas ──────────────────────────────────────────────
# Colunas reais da aba "8261-REENTREGAS 2026" (obtidas da planilha):
# NUMNOTA, DTFAT, SERIE, ESPECIE, DTSAIDA, VLTOT, GERTOT, PESO, NUMTRANS,
# VENDA, NUMCARANTERIOR, PLACAANT, COD MOT ANTERIOR, NOME MOT ANTERIOR,
# COD AJU ANTERIOR, NOME AJU ANTERIOR, NUMCARATUAL, PLACAATUAL,
# COD MOT ATUAL, NOME MOT ATUAL, COD AJU ATUAL, NOME AJU ATUAL,
# DTRANSF, CODMOTIVO, MOTIVOTRANSF, CODCLI, CLIENTE, BAIRROENT,
# CODPRACA, PRACA, ROTA, NUMPED, CODUSU, RNOME

REENT_COLS_MAP = {
    # Chave canônica  →  lista de variações possíveis (a planilha usa exatamente as primeiras)
    "NUMNOTA":            ["NUMNOTA"],
    "DTFAT":              ["DTFAT"],
    "SERIE":              ["SERIE"],
    "ESPECIE":            ["ESPECIE"],
    "DTSAIDA":            ["DTSAIDA"],
    "VLTOT":              ["VLTOT"],
    "GERTOT":             ["GERTOT"],
    "PESO":               ["PESO"],
    "NUMTRANS":           ["NUMTRANS"],
    "VENDA":              ["VENDA"],
    "NUMCARANTERIOR":     ["NUMCARANTERIOR"],
    "PLACAANT":           ["PLACAANT"],
    "COD_MOT_ANTERIOR":   ["COD MOT ANTERIOR","COD_MOT_ANTERIOR"],
    "NOME_MOT_ANTERIOR":  ["NOME MOT ANTERIOR","NOME_MOT_ANTERIOR"],
    "COD_AJU_ANTERIOR":   ["COD AJU ANTERIOR","COD_AJU_ANTERIOR"],
    "NOME_AJU_ANTERIOR":  ["NOME AJU ANTERIOR","NOME_AJU_ANTERIOR"],
    "NUMCARATUAL":        ["NUMCARATUAL"],
    "PLACAATUAL":         ["PLACAATUAL"],
    "COD_MOT_ATUAL":      ["COD MOT ATUAL","COD_MOT_ATUAL"],
    "NOME_MOT_ATUAL":     ["NOME MOT ATUAL","NOME_MOT_ATUAL"],
    "COD_AJU_ATUAL":      ["COD AJU ATUAL","COD_AJU_ATUAL"],
    "NOME_AJU_ATUAL":     ["NOME AJU ATUAL","NOME_AJU_ATUAL"],
    "DATATRANSF":         ["DTRANSF","DATATRANSF","DATA_TRANSF"],
    "CODMOTIVO":          ["CODMOTIVO"],
    "MOTIVOTRANSF":       ["MOTIVOTRANSF"],
    "CODCLI":             ["CODCLI"],
    "CLIENTE":            ["CLIENTE"],
    "BAIRROENT":          ["BAIRROENT"],
    "CODPRACA":           ["CODPRACA"],
    "PRACA":              ["PRACA"],
    "ROTA":               ["ROTA"],
    "NUMPED":             ["NUMPED"],
    "CODUSU":             ["CODUSU"],
    "NOME":               ["RNOME","NOME"],
}

df_reent = None
reent_cols = {}

if df_reent_raw is not None:
    # Normaliza: strip espaços nas bordas, uppercase, mas preserva espaços internos
    # para colunas como "COD MOT ANTERIOR"
    df_reent_raw.columns = [str(c).strip().upper() for c in df_reent_raw.columns]

    def get_col_reent(alternatives):
        """Busca coluna pelo nome exato (após strip+upper)."""
        for n in alternatives:
            n_norm = n.strip().upper()
            if n_norm in df_reent_raw.columns:
                return n_norm
        return None

    for canonical, alternatives in REENT_COLS_MAP.items():
        found = get_col_reent(alternatives)
        reent_cols[canonical] = found

    # Valor col para reentregas — coluna real é VLTOT
    REENT_VALOR_COL = get_col_reent(["VLTOT","VLTOTAL","VL_TOTAL","VALOR","TOTAL"])

    if REENT_VALOR_COL:
        df_reent_raw[REENT_VALOR_COL] = df_reent_raw[REENT_VALOR_COL].apply(parse_brl).fillna(0)
    else:
        df_reent_raw["_VALOR_REENT"] = 0.0
        REENT_VALOR_COL = "_VALOR_REENT"

    for col in df_reent_raw.columns:
        if col != REENT_VALOR_COL:
            df_reent_raw[col] = df_reent_raw[col].fillna("").astype(str).str.strip()

    # Parse data de transferência — coluna real é DTRANSF
    dt_col = reent_cols.get("DATATRANSF")
    if dt_col:
        df_reent_raw["_DATATRANSF_DT"] = pd.to_datetime(df_reent_raw[dt_col], dayfirst=True, errors="coerce")
        mask_nat2 = df_reent_raw["_DATATRANSF_DT"].isna() & (df_reent_raw[dt_col] != "")
        if mask_nat2.any():
            alt2 = pd.to_datetime(df_reent_raw.loc[mask_nat2, dt_col], format="%Y-%m-%d", errors="coerce")
            df_reent_raw.loc[mask_nat2, "_DATATRANSF_DT"] = alt2
    else:
        df_reent_raw["_DATATRANSF_DT"] = pd.NaT

    df_reent = df_reent_raw.copy()

# ── TOPBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bg-overlay">
  <div class="bg-img"></div>
  <div class="bg-tint"></div>
</div>
""", unsafe_allow_html=True)

import streamlit.components.v1 as components
components.html("""
<script>
(function removeBadge() {
  const selectors = [
    '[data-testid="stStatusWidget"]','[data-testid="stToolbar"]',
    'iframe[title="streamlit_cloud_info"]','.viewerBadge_container__1QSob',
    '.styles_viewerBadge_1yB5','div[class*="StatusWidget"]',
    'div[class*="viewerBadge"]','div[class*="streamlit-badge"]',
    '#stDecoration','a[href*="streamlit.io/cloud"]',
  ];
  function hide() {
    selectors.forEach(function(sel) {
      try {
        var els = window.parent.document.querySelectorAll(sel);
        els.forEach(function(el) { el.style.setProperty('display','none','important'); });
      } catch(e) {}
    });
    try {
      var header = window.parent.document.querySelector('[data-testid="stHeader"]');
      if (header) header.style.setProperty('display','none','important');
    } catch(e) {}
  }
  hide();
  var observer = new MutationObserver(hide);
  try { observer.observe(window.parent.document.body, { childList: true, subtree: true }); } catch(e) {}
})();
</script>
""", height=0)

st.markdown(f"""
<div class="topbar">
  <div class="topbar-inner">
    <div class="topbar-icon">📦</div>
    <div class="topbar-divider"></div>
    <div class="topbar-text">
      <p class="topbar-title">GESTÃO DE DEVOLUÇÕES DELLY'S</p>
      <p class="topbar-sub">Módulo de Análise e Controle Operacional</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FILTROS GLOBAIS (devoluções)
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="filter-bar"><div class="filter-bar-title">⚙️ FILTROS GLOBAIS — DEVOLUÇÕES</div>', unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns([3, 2, 2, 1], gap="medium")

usar_data = False
dt_sel = None

with fc1:
    datas_ok = df_raw["_DTENTREGA_DT"].dropna()
    col_label = COL_DTENTREGA if COL_DTENTREGA else "DTENT"
    if len(datas_ok) > 0:
        datas_unicas = sorted(datas_ok.dt.date.unique())
        opcoes_data = ["— Todas as datas —"] + [d.strftime("%d/%m/%Y") for d in datas_unicas]
        sel_data_str = st.selectbox(f"📅 Data de Entrega ({col_label})", opcoes_data, key="g_dtsel")
        if sel_data_str != "— Todas as datas —":
            dt_sel = datetime.strptime(sel_data_str, "%d/%m/%Y").date()
            usar_data = True
    else:
        st.caption(f"⚠️ Sem datas válidas na coluna {col_label}")

with fc2:
    if COL_DEVOLUCION:
        devs_opts = sorted([x for x in df_raw[COL_DEVOLUCION].unique() if x not in ("","N/D","nan","None")])
        sel_dev = st.multiselect("👷 Devolucionista (NOMEFUNC)", devs_opts, default=[], key="g_dev", placeholder="Todos")
    else:
        sel_dev = []
        st.caption("⚠️ NOMEFUNC não encontrado")

with fc3:
    if COL_MOTIVO:
        mot_opts = sorted([x for x in df_raw[COL_MOTIVO].unique() if x not in ("","N/D","nan","None")])
        sel_motivo = st.multiselect("❗ Motivo", mot_opts, default=[], key="g_mot", placeholder="Todos")
    else:
        sel_motivo = []

with fc4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Atualizar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── Aplica filtros devoluções ──────────────────────────────────────────────────
df = df_raw.copy()
if usar_data and dt_sel:
    df = df[df["_DTENTREGA_DT"].dt.date == dt_sel]
if sel_dev and COL_DEVOLUCION:
    df = df[df[COL_DEVOLUCION].isin(sel_dev)]
if sel_motivo and COL_MOTIVO:
    df = df[df[COL_MOTIVO].isin(sel_motivo)]

# ── KPIs devoluções ────────────────────────────────────────────────────────────
total_val      = df[VALOR_COL].sum()
total_notas    = len(df)
total_clientes = df[COL_CLIENTE].nunique() if COL_CLIENTE else 0
ticket_medio   = total_val / total_notas if total_notas > 0 else 0
total_placas   = df[COL_PLACA].nunique() if COL_PLACA else 0

filtros_info = []
if usar_data and dt_sel:
    filtros_info.append(f"📅 {dt_sel.strftime('%d/%m/%Y')}")
if sel_dev:
    filtros_info.append(f"👷 {', '.join(sel_dev[:2])}{'...' if len(sel_dev)>2 else ''}")
if sel_motivo:
    filtros_info.append(f"❗ {len(sel_motivo)} motivo(s)")
if filtros_info:
    st.info(f"🔎 Filtros: {' · '.join(filtros_info)} — *{total_notas} registros filtrados*")

# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
tab_dash, tab_reent, tab_reent_det, tab_campos, tab_dados = st.tabs([
    "📊  Dashboard",
    "🔄  Reentregas",
    "🔍  Detalhes das Reentregas",
    "🗂️  Campos",
    "📑  Dados Completos",
])

# ══════════════════════════════════════════════════════════════
# ABA 1 — DASHBOARD DEVOLUÇÕES
# ══════════════════════════════════════════════════════════════
with tab_dash:

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-icon">💰</div>
        <div class="kpi-label">Valor Total</div>
        <div class="kpi-value">{fmt_brl(total_val)}</div>
        <div class="kpi-sub">Total devolvido</div></div>
      <div class="kpi-card"><div class="kpi-icon">📄</div>
        <div class="kpi-label">Devoluções</div>
        <div class="kpi-value">{total_notas:,}</div>
        <div class="kpi-sub">Registros filtrados</div></div>
      <div class="kpi-card"><div class="kpi-icon">👤</div>
        <div class="kpi-label">Clientes</div>
        <div class="kpi-value">{total_clientes:,}</div>
        <div class="kpi-sub">Clientes únicos</div></div>
      <div class="kpi-card"><div class="kpi-icon">📊</div>
        <div class="kpi-label">Ticket Médio</div>
        <div class="kpi-value">{fmt_brl(ticket_medio)}</div>
        <div class="kpi-sub">Por devolução</div></div>
      <div class="kpi-card"><div class="kpi-icon">🚚</div>
        <div class="kpi-label">Placas</div>
        <div class="kpi-value">{total_placas:,}</div>
        <div class="kpi-sub">Veículos únicos</div></div>
    </div>
    """.replace(",","."), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🚚 Devoluções por Placa — Valor e Quantidade</h3></div>', unsafe_allow_html=True)

    if COL_PLACA:
        df_placa = (
            df[df[COL_PLACA].str.strip() != ""]
            .groupby(COL_PLACA)
            .agg(Valor=(VALOR_COL,"sum"), Qtd=(VALOR_COL,"count"))
            .reset_index()
            .sort_values("Valor", ascending=False)
        )

        if not df_placa.empty:
            n = len(df_placa)
            bar_colors = []
            for i in range(n):
                if i < 5:    bar_colors.append("#ef4444")
                elif i < 10: bar_colors.append("#f97316")
                else:        bar_colors.append("#0ea5e9")

            periodo = f"Data: {dt_sel.strftime('%d/%m/%Y')}" if usar_data and dt_sel else ""

            fig_placa = go.Figure()
            fig_placa.add_trace(go.Bar(
                x=df_placa[COL_PLACA], y=df_placa["Valor"],
                name="Soma Valor (R$)",
                marker=dict(color=bar_colors, opacity=0.88,
                            line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
                text=[fmt_brl(v) for v in df_placa["Valor"]],
                textposition="outside",
                textfont=dict(size=13, color="#ffffff", family="DM Mono", weight="bold"),
                hovertemplate="<b>%{x}</b><br>Valor: <b>%{text}</b><extra></extra>",
                yaxis="y1",
            ))
            fig_placa.add_trace(go.Scatter(
                x=df_placa[COL_PLACA], y=df_placa["Qtd"],
                name="Qtd. Devoluções",
                mode="lines+markers+text",
                line=dict(color="#f59e0b", width=2.5),
                marker=dict(color="#fde68a", size=10, line=dict(color="#f59e0b", width=2)),
                text=df_placa["Qtd"].astype(str),
                textposition="top center",
                textfont=dict(size=13, color="#ffffff", family="DM Mono", weight="bold"),
                hovertemplate="<b>%{x}</b><br>Qtd: <b>%{y}</b><extra></extra>",
                yaxis="y2",
            ))

            h = max(440, min(n * 36, 680))
            fig_placa.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.015)",
                font=dict(color="#94a3b8", family="Space Grotesk"),
                height=h, margin=dict(t=60, b=90, l=12, r=70),
                title=dict(text=f"<b>{periodo}</b>",
                           font=dict(size=17, color="#ffffff", family="Space Grotesk"),
                           x=0.5, xanchor="center"),
                bargap=0.28,
                xaxis=dict(tickfont=dict(color="#b0bec5", size=11, family="DM Mono"),
                           gridcolor="rgba(255,255,255,0.04)",
                           linecolor="rgba(255,255,255,0.06)", tickangle=-38),
                yaxis=dict(title=dict(text="Soma de Valor (R$)", font=dict(color="#64748b", size=11)),
                           tickfont=dict(color="#64748b", size=10),
                           gridcolor="rgba(255,255,255,0.05)",
                           linecolor="rgba(255,255,255,0.06)",
                           tickformat=",.0f", side="left"),
                yaxis2=dict(title=dict(text="Contagem de Devoluções", font=dict(color="#f59e0b", size=11)),
                            tickfont=dict(color="#f59e0b", size=10),
                            overlaying="y", side="right", showgrid=False),
                legend=dict(bgcolor="rgba(8,15,35,0.92)", bordercolor="rgba(56,189,248,0.2)",
                            borderwidth=1, font=dict(color="#94a3b8", size=11),
                            orientation="h", x=1.0, xanchor="right", y=-0.22),
            )
            st.plotly_chart(fig_placa, use_container_width=True)
            st.markdown("""
            <div style="display:flex;gap:22px;font-size:0.74rem;color:#64748b;margin-top:-8px;margin-bottom:18px;padding-left:4px;">
              <span>🔴 Top 5 — crítico</span><span>🟠 6–10 — atenção</span>
              <span>🔵 Demais placas</span><span>🟡 Linha = quantidade de devoluções</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Sem dados de placa para o filtro selecionado")
    else:
        st.warning("Coluna PLACA não encontrada na planilha")

    st.markdown("---")
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Valor de Devolução por Motivo</h3></div>', unsafe_allow_html=True)

    if COL_MOTIVO:
        df_motivo_val = (
            df[df[COL_MOTIVO].str.strip() != ""]
            .groupby(COL_MOTIVO)
            .agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
            .reset_index().sort_values("Valor", ascending=False)
        )
        if not df_motivo_val.empty:
            n_mot = len(df_motivo_val)
            bar_colors_mot = ["#ef4444" if i<3 else "#f97316" if i<6 else "#0ea5e9" for i in range(n_mot)]
            fig_mot = go.Figure()
            fig_mot.add_trace(go.Bar(
                x=df_motivo_val[COL_MOTIVO], y=df_motivo_val["Valor"],
                name="Valor Total (R$)",
                marker=dict(color=bar_colors_mot, opacity=0.9,
                            line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
                text=[fmt_brl(v) for v in df_motivo_val["Valor"]],
                textposition="outside",
                textfont=dict(size=13, color="#ffffff", family="DM Mono", weight="bold"),
                hovertemplate="<b>%{x}</b><br>Valor: <b>%{text}</b><extra></extra>",
                yaxis="y1",
            ))
            fig_mot.add_trace(go.Scatter(
                x=df_motivo_val[COL_MOTIVO], y=df_motivo_val["Qtd"],
                name="Qtd. Devoluções",
                mode="lines+markers+text",
                line=dict(color="#f59e0b", width=2.5),
                marker=dict(color="#fde68a", size=10, line=dict(color="#f59e0b", width=2)),
                text=df_motivo_val["Qtd"].astype(str),
                textposition="top center",
                textfont=dict(size=13, color="#ffffff", family="DM Mono", weight="bold"),
                hovertemplate="<b>%{x}</b><br>Qtd: <b>%{y}</b><extra></extra>",
                yaxis="y2",
            ))
            h_mot = max(440, min(n_mot * 60, 680))
            fig_mot.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.015)",
                font=dict(color="#94a3b8", family="Space Grotesk"),
                height=h_mot, margin=dict(t=40, b=110, l=12, r=70), bargap=0.32,
                xaxis=dict(tickfont=dict(color="#b0bec5", size=11, family="Space Grotesk"),
                           gridcolor="rgba(255,255,255,0.04)",
                           linecolor="rgba(255,255,255,0.06)", tickangle=-35, automargin=True),
                yaxis=dict(title=dict(text="Valor Total (R$)", font=dict(color="#64748b", size=11)),
                           tickfont=dict(color="#64748b", size=10),
                           gridcolor="rgba(255,255,255,0.05)",
                           linecolor="rgba(255,255,255,0.06)", tickformat=",.0f", side="left"),
                yaxis2=dict(title=dict(text="Qtd. Devoluções", font=dict(color="#f59e0b", size=11)),
                            tickfont=dict(color="#f59e0b", size=10),
                            overlaying="y", side="right", showgrid=False),
                legend=dict(bgcolor="rgba(8,15,35,0.92)", bordercolor="rgba(56,189,248,0.2)",
                            borderwidth=1, font=dict(color="#94a3b8", size=11),
                            orientation="h", x=1.0, xanchor="right", y=-0.22),
            )
            st.plotly_chart(fig_mot, use_container_width=True)
            st.markdown("""
            <div style="display:flex;gap:22px;font-size:0.74rem;color:#64748b;margin-top:-8px;margin-bottom:18px;padding-left:4px;">
              <span>🔴 Top 3 motivos — maior impacto financeiro</span>
              <span>🟠 4º–6º — atenção</span><span>🔵 Demais motivos</span>
            </div>""", unsafe_allow_html=True)

            with st.expander("📋 Ver tabela de motivos por valor"):
                df_mot_display = df_motivo_val.copy()
                df_mot_display["Valor (R$)"] = df_mot_display["Valor"].apply(fmt_brl)
                df_mot_display["% do Total"] = (
                    (df_mot_display["Valor"] / total_val * 100).round(1).astype(str) + "%"
                    if total_val > 0 else "0%"
                )
                df_mot_display = df_mot_display.rename(columns={COL_MOTIVO: "Motivo", "Qtd": "Qtd."})
                st.dataframe(df_mot_display[["Motivo", "Qtd.", "Valor (R$)", "% do Total"]],
                             use_container_width=True, hide_index=True)

    st.markdown("---")
    c1, c2, c3 = st.columns(3, gap="medium")

    def make_hbar(df_data, x_col, y_col, color_scale, height=420):
        fig = px.bar(df_data, x=x_col, y=y_col, orientation="h",
                     color=x_col, color_continuous_scale=color_scale,
                     text=[fmt_brl(v) for v in df_data[x_col]],
                     labels={y_col: "", x_col: "R$"})
        fig.update_traces(textposition="outside",
                          textfont=dict(size=11, color="#e2e8f0", family="DM Mono"),
                          cliponaxis=False, marker_line_width=0)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", family="Space Grotesk"), coloraxis_showscale=False,
            height=height, margin=dict(t=10, b=30, l=6, r=110),
            xaxis=dict(tickfont=dict(color="#475569", size=10),
                       gridcolor="rgba(255,255,255,0.04)",
                       linecolor="rgba(255,255,255,0.05)", tickformat=",.0f", zeroline=False),
            yaxis=dict(tickfont=dict(color="#cbd5e1", size=11, family="Space Grotesk"),
                       gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)", automargin=True))
        return fig

    with c1:
        if COL_MOTIVO:
            df_m = (df[df[COL_MOTIVO].str.strip()!=""]
                    .groupby(COL_MOTIVO).agg(Valor=(VALOR_COL,"sum"), Qtd=(VALOR_COL,"count"))
                    .reset_index().sort_values("Valor",ascending=True).tail(8))
            if not df_m.empty:
                st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ PRINCIPAIS MOTIVOS</h3></div>', unsafe_allow_html=True)
                st.plotly_chart(make_hbar(df_m, "Valor", COL_MOTIVO, RED, 420), use_container_width=True)
                top = df_m.iloc[-1]
                pct = top["Valor"]/total_val*100 if total_val>0 else 0
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{top[COL_MOTIVO]}</b> representa {pct:.1f}% ({fmt_brl(top["Valor"])})</p>', unsafe_allow_html=True)

    with c2:
        if COL_CLIENTE:
            df_cli = (df[df[COL_CLIENTE].str.strip()!=""]
                      .groupby(COL_CLIENTE).agg(Valor=(VALOR_COL,"sum"), Qtd=(VALOR_COL,"count"))
                      .reset_index().sort_values("Valor",ascending=True).tail(10))
            if not df_cli.empty:
                st.markdown('<div class="sec-header"><div class="bar"></div><h3>👤 TOP 10 CLIENTES</h3></div>', unsafe_allow_html=True)
                st.plotly_chart(make_hbar(df_cli, "Valor", COL_CLIENTE, MIXED, 420), use_container_width=True)
                top_c = df_cli.iloc[-1]
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{str(top_c[COL_CLIENTE])[:32]}</b> — {fmt_brl(top_c["Valor"])}</p>', unsafe_allow_html=True)

    with c3:
        if COL_VENDEDOR:
            df_v = (df[df[COL_VENDEDOR].str.strip()!=""]
                    .groupby(COL_VENDEDOR).agg(Valor=(VALOR_COL,"sum"), Qtd=(VALOR_COL,"count"))
                    .reset_index().sort_values("Valor",ascending=True).tail(10))
            if not df_v.empty:
                st.markdown('<div class="sec-header"><div class="bar"></div><h3>🧑‍💼 TOP 10 VENDEDORES</h3></div>', unsafe_allow_html=True)
                st.plotly_chart(make_hbar(df_v, "Valor", COL_VENDEDOR, BLUE, 420), use_container_width=True)
                top_v = df_v.iloc[-1]
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{str(top_v[COL_VENDEDOR])[:32]}</b> — {int(top_v["Qtd"])} devoluções</p>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    c4, c5 = st.columns([1,2], gap="large")
    with c4:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏙️ Por Destino</h3></div>', unsafe_allow_html=True)
        if COL_DESTINO:
            df_d = (df[df[COL_DESTINO].str.strip()!=""]
                    .groupby(COL_DESTINO).agg(Valor=(VALOR_COL,"sum"))
                    .reset_index().sort_values("Valor",ascending=False).head(10))
            if not df_d.empty:
                fig_d = px.pie(df_d, names=COL_DESTINO, values="Valor",
                               color_discrete_sequence=MIXED, hole=0.52)
                fig_d.update_traces(
                    textfont=dict(size=12, color="#e2e8f0"),
                    marker=dict(line=dict(color="rgba(4,9,20,0.8)",width=2)),
                    pull=[0.05]+[0]*(len(df_d)-1))
                st.plotly_chart(plotly_dark(fig_d,height=360), use_container_width=True)

    with c5:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>📊 Ranking de Motivos</h3></div>', unsafe_allow_html=True)
        if COL_MOTIVO:
            df_rk = (df.groupby(COL_MOTIVO)
                     .agg(Qtd=(VALOR_COL,"count"),Total=(VALOR_COL,"sum"))
                     .reset_index().sort_values("Total",ascending=False))
            df_rk["Valor Total"] = df_rk["Total"].apply(fmt_brl)
            df_rk["% Total"] = (df_rk["Total"]/total_val*100).round(1).astype(str)+"%" if total_val>0 else "0%"
            df_rk = df_rk.rename(columns={COL_MOTIVO:"Motivo"})
            rows_html = ""
            for i, row in df_rk[["Motivo","Qtd","Valor Total","% Total"]].iterrows():
                bg = "rgba(14,165,233,0.06)" if i % 2 == 0 else "rgba(0,0,0,0)"
                rows_html += f"""<tr style="background:{bg};">
                  <td style="padding:10px 14px;color:#cbd5e1;font-size:0.84rem;border-bottom:1px solid rgba(56,189,248,0.07);">{row['Motivo']}</td>
                  <td style="padding:10px 14px;color:#7dd3fc;font-size:0.84rem;text-align:center;border-bottom:1px solid rgba(56,189,248,0.07);">{row['Qtd']}</td>
                  <td style="padding:10px 14px;color:#4ade80;font-size:0.84rem;font-family:'DM Mono',monospace;border-bottom:1px solid rgba(56,189,248,0.07);">{row['Valor Total']}</td>
                  <td style="padding:10px 14px;color:#f59e0b;font-size:0.84rem;text-align:center;border-bottom:1px solid rgba(56,189,248,0.07);">{row['% Total']}</td>
                </tr>"""
            st.markdown(f"""
            <div style="background:rgba(6,13,31,0.92);border:1px solid rgba(56,189,248,0.15);
              border-radius:14px;overflow:hidden;max-height:360px;overflow-y:auto;">
              <table style="width:100%;border-collapse:collapse;">
                <thead><tr style="background:rgba(12,26,58,0.98);position:sticky;top:0;">
                  <th style="padding:12px 14px;color:#38bdf8;font-size:0.75rem;font-weight:700;letter-spacing:0.08em;text-align:left;text-transform:uppercase;border-bottom:1px solid rgba(56,189,248,0.2);">Motivo</th>
                  <th style="padding:12px 14px;color:#38bdf8;font-size:0.75rem;font-weight:700;letter-spacing:0.08em;text-align:center;border-bottom:1px solid rgba(56,189,248,0.2);">Qtd</th>
                  <th style="padding:12px 14px;color:#38bdf8;font-size:0.75rem;font-weight:700;letter-spacing:0.08em;border-bottom:1px solid rgba(56,189,248,0.2);">Valor Total</th>
                  <th style="padding:12px 14px;color:#38bdf8;font-size:0.75rem;font-weight:700;letter-spacing:0.08em;text-align:center;border-bottom:1px solid rgba(56,189,248,0.2);">% Total</th>
                </tr></thead>
                <tbody>{rows_html}</tbody>
              </table>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ABA 2 — DASHBOARD REENTREGAS
# ══════════════════════════════════════════════════════════════
with tab_reent:

    if reent_load_error:
        st.error(f"❌ Erro ao carregar aba de reentregas: {reent_load_error}")
        st.info("💡 Verifique se a aba '8261-REENTREGAS 2026' existe na planilha e está acessível.")
        st.stop()

    if df_reent is None or len(df_reent) == 0:
        st.warning("⚠️ Nenhum dado encontrado na aba de reentregas.")
        st.stop()

    # ── Filtro de data DATATRANSF ────────────────────────────────────────────
    st.markdown('<div class="filter-bar"><div class="filter-bar-title">⚙️ FILTROS — REENTREGAS</div>', unsafe_allow_html=True)
    rf1, rf2, rf3 = st.columns([3, 3, 1], gap="medium")

    usar_data_reent = False
    dt_reent_sel = None

    with rf1:
        datas_reent_ok = df_reent["_DATATRANSF_DT"].dropna()
        dt_col_reent = reent_cols.get("DATATRANSF")
        col_label_reent = dt_col_reent if dt_col_reent else "DATATRANSF"
        if len(datas_reent_ok) > 0:
            datas_reent_unicas = sorted(datas_reent_ok.dt.date.unique())
            opcoes_reent = ["— Todas as datas —"] + [d.strftime("%d/%m/%Y") for d in datas_reent_unicas]
            sel_reent_data_str = st.selectbox(f"📅 Data de Transferência ({col_label_reent})", opcoes_reent, key="r_dtsel")
            if sel_reent_data_str != "— Todas as datas —":
                dt_reent_sel = datetime.strptime(sel_reent_data_str, "%d/%m/%Y").date()
                usar_data_reent = True
        else:
            st.caption(f"⚠️ Sem datas válidas na coluna {col_label_reent}")

    with rf2:
        motivo_reent_col = reent_cols.get("MOTIVOTRANSF")
        if motivo_reent_col:
            mot_reent_opts = sorted([x for x in df_reent[motivo_reent_col].unique() if x not in ("","N/D","nan","None")])
            sel_mot_reent = st.multiselect("❗ Motivo de Transferência", mot_reent_opts, default=[], key="r_mot", placeholder="Todos")
        else:
            sel_mot_reent = []

    with rf3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Atualizar", use_container_width=True, key="btn_reent"):
            st.cache_data.clear()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Aplica filtros reentregas
    df_r = df_reent.copy()
    if usar_data_reent and dt_reent_sel:
        df_r = df_r[df_r["_DATATRANSF_DT"].dt.date == dt_reent_sel]
    if sel_mot_reent and motivo_reent_col:
        df_r = df_r[df_r[motivo_reent_col].isin(sel_mot_reent)]

    filtros_reent_info = []
    if usar_data_reent and dt_reent_sel:
        filtros_reent_info.append(f"📅 {dt_reent_sel.strftime('%d/%m/%Y')}")
    if sel_mot_reent:
        filtros_reent_info.append(f"❗ {len(sel_mot_reent)} motivo(s)")
    if filtros_reent_info:
        st.info(f"🔎 Filtros: {' · '.join(filtros_reent_info)} — *{len(df_r)} registros filtrados*")

    # KPIs reentregas
    total_reent         = len(df_r)
    total_reent_valor   = df_r[REENT_VALOR_COL].sum() if REENT_VALOR_COL in df_r.columns else 0
    placaant_col        = reent_cols.get("PLACAANT")
    placaatual_col      = reent_cols.get("PLACAATUAL")
    cliente_reent_col   = reent_cols.get("CLIENTE")
    praca_reent_col     = reent_cols.get("PRACA")
    motivo_reent_col2   = reent_cols.get("MOTIVOTRANSF")
    nome_reent_col      = reent_cols.get("NOME")

    total_placas_ant    = df_r[placaant_col].nunique() if placaant_col and placaant_col in df_r.columns else 0
    total_clientes_reent= df_r[cliente_reent_col].nunique() if cliente_reent_col and cliente_reent_col in df_r.columns else 0
    ticket_reent        = total_reent_valor / total_reent if total_reent > 0 and total_reent_valor > 0 else 0

    has_valor = total_reent_valor > 0

    if has_valor:
        st.markdown(f"""
        <div class="kpi-grid">
          <div class="kpi-card"><div class="kpi-icon">🔄</div>
            <div class="kpi-label">Total Reentregas</div>
            <div class="kpi-value-amber">{total_reent:,}</div>
            <div class="kpi-sub">Registros filtrados</div></div>
          <div class="kpi-card"><div class="kpi-icon">💰</div>
            <div class="kpi-label">Valor Total</div>
            <div class="kpi-value">{fmt_brl(total_reent_valor)}</div>
            <div class="kpi-sub">Total transferido</div></div>
          <div class="kpi-card"><div class="kpi-icon">👤</div>
            <div class="kpi-label">Clientes</div>
            <div class="kpi-value">{total_clientes_reent:,}</div>
            <div class="kpi-sub">Clientes únicos</div></div>
          <div class="kpi-card"><div class="kpi-icon">📊</div>
            <div class="kpi-label">Ticket Médio</div>
            <div class="kpi-value">{fmt_brl(ticket_reent)}</div>
            <div class="kpi-sub">Por reentrega</div></div>
          <div class="kpi-card"><div class="kpi-icon">🚚</div>
            <div class="kpi-label">Placas Origem</div>
            <div class="kpi-value">{total_placas_ant:,}</div>
            <div class="kpi-sub">Veículos anteriores</div></div>
        </div>
        """.replace(",","."), unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="kpi-grid-4">
          <div class="kpi-card"><div class="kpi-icon">🔄</div>
            <div class="kpi-label">Total Reentregas</div>
            <div class="kpi-value-amber">{total_reent:,}</div>
            <div class="kpi-sub">Registros filtrados</div></div>
          <div class="kpi-card"><div class="kpi-icon">👤</div>
            <div class="kpi-label">Clientes</div>
            <div class="kpi-value">{total_clientes_reent:,}</div>
            <div class="kpi-sub">Clientes únicos</div></div>
          <div class="kpi-card"><div class="kpi-icon">🚚</div>
            <div class="kpi-label">Placas Origem</div>
            <div class="kpi-value">{total_placas_ant:,}</div>
            <div class="kpi-sub">Veículos anteriores</div></div>
          <div class="kpi-card"><div class="kpi-icon">🗺️</div>
            <div class="kpi-label">Praças</div>
            <div class="kpi-value">{df_r[praca_reent_col].nunique() if praca_reent_col and praca_reent_col in df_r.columns else 0:,}</div>
            <div class="kpi-sub">Destinos únicos</div></div>
        </div>
        """.replace(",","."), unsafe_allow_html=True)

    st.markdown("---")

    # ── GRÁFICO 1: Reentregas por Placa Anterior ─────────────────────────────
    st.markdown('<div class="sec-header"><div class="bar-green" style="width:3px;height:24px;background:linear-gradient(180deg,#4ade80,#16a34a);border-radius:2px;box-shadow:0 0 10px rgba(74,222,128,0.5);"></div><h3>🚚 Reentregas por Placa Anterior — Quantidade</h3></div>', unsafe_allow_html=True)

    if placaant_col and placaant_col in df_r.columns:
        agg_dict = {"Qtd": (placaant_col, "count")}
        if has_valor:
            agg_col_val = REENT_VALOR_COL
            df_placa_r = (
                df_r[df_r[placaant_col].str.strip() != ""]
                .groupby(placaant_col)
                .agg(Qtd=(placaant_col,"count"), Valor=(agg_col_val,"sum"))
                .reset_index().sort_values("Qtd", ascending=False)
            )
        else:
            df_placa_r = (
                df_r[df_r[placaant_col].str.strip() != ""]
                .groupby(placaant_col)
                .agg(Qtd=(placaant_col,"count"))
                .reset_index().sort_values("Qtd", ascending=False)
            )

        if not df_placa_r.empty:
            n_r = len(df_placa_r)
            bar_colors_r = ["#ef4444" if i<3 else "#f97316" if i<6 else "#22c55e" for i in range(n_r)]
            periodo_r = f"Data: {dt_reent_sel.strftime('%d/%m/%Y')}" if usar_data_reent and dt_reent_sel else ""

            fig_placa_r = go.Figure()
            y_vals = df_placa_r["Valor"] if has_valor else df_placa_r["Qtd"]
            text_vals = [fmt_brl(v) for v in y_vals] if has_valor else [str(v) for v in y_vals]
            y_label = "Valor (R$)" if has_valor else "Qtd. Reentregas"

            fig_placa_r.add_trace(go.Bar(
                x=df_placa_r[placaant_col],
                y=y_vals,
                name=y_label,
                marker=dict(color=bar_colors_r, opacity=0.88,
                            line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
                text=text_vals,
                textposition="outside",
                textfont=dict(size=13, color="#ffffff", family="DM Mono", weight="bold"),
                hovertemplate="<b>%{x}</b><br>" + y_label + ": <b>%{text}</b><extra></extra>",
                yaxis="y1",
            ))

            # Linha amarela de quantidade
            fig_placa_r.add_trace(go.Scatter(
                x=df_placa_r[placaant_col],
                y=df_placa_r["Qtd"],
                name="Qtd. Reentregas",
                mode="lines+markers+text",
                line=dict(color="#f59e0b", width=2.5),
                marker=dict(color="#fde68a", size=10, line=dict(color="#f59e0b", width=2)),
                text=df_placa_r["Qtd"].astype(str),
                textposition="top center",
                textfont=dict(size=13, color="#ffffff", family="DM Mono", weight="bold"),
                hovertemplate="<b>%{x}</b><br>Qtd: <b>%{y}</b><extra></extra>",
                yaxis="y2",
            ))

            h_r = max(440, min(n_r * 36, 680))
            fig_placa_r.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.015)",
                font=dict(color="#94a3b8", family="Space Grotesk"),
                height=h_r, margin=dict(t=60, b=90, l=12, r=70),
                title=dict(text=f"<b>{periodo_r}</b>",
                           font=dict(size=17, color="#ffffff", family="Space Grotesk"),
                           x=0.5, xanchor="center"),
                bargap=0.28,
                xaxis=dict(tickfont=dict(color="#b0bec5", size=11, family="DM Mono"),
                           gridcolor="rgba(255,255,255,0.04)",
                           linecolor="rgba(255,255,255,0.06)", tickangle=-38),
                yaxis=dict(title=dict(text=y_label, font=dict(color="#64748b", size=11)),
                           tickfont=dict(color="#64748b", size=10),
                           gridcolor="rgba(255,255,255,0.05)",
                           linecolor="rgba(255,255,255,0.06)", tickformat=",.0f", side="left"),
                yaxis2=dict(title=dict(text="Contagem de Reentregas", font=dict(color="#f59e0b", size=11)),
                            tickfont=dict(color="#f59e0b", size=10),
                            overlaying="y", side="right", showgrid=False),
                legend=dict(bgcolor="rgba(8,15,35,0.92)", bordercolor="rgba(56,189,248,0.2)",
                            borderwidth=1, font=dict(color="#94a3b8", size=11),
                            orientation="h", x=1.0, xanchor="right", y=-0.22),
            )
            st.plotly_chart(fig_placa_r, use_container_width=True)
            st.markdown("""
            <div style="display:flex;gap:22px;font-size:0.74rem;color:#64748b;margin-top:-8px;margin-bottom:18px;padding-left:4px;">
              <span>🔴 Top 3 — crítico</span><span>🟠 4–6 — atenção</span>
              <span>🟢 Demais placas</span><span>🟡 Linha = quantidade de reentregas</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Sem dados de placa anterior para o filtro selecionado.")
    else:
        st.warning("Coluna PLACAANT não encontrada na planilha de reentregas.")

    st.markdown("---")

    # ── GRÁFICO 2: Motivos de Transferência ──────────────────────────────────
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Reentregas por Motivo de Transferência</h3></div>', unsafe_allow_html=True)

    if motivo_reent_col2 and motivo_reent_col2 in df_r.columns:
        if has_valor:
            df_mot_r = (
                df_r[df_r[motivo_reent_col2].str.strip() != ""]
                .groupby(motivo_reent_col2)
                .agg(Valor=(REENT_VALOR_COL,"sum"), Qtd=(motivo_reent_col2,"count"))
                .reset_index().sort_values("Valor", ascending=False)
            )
            y_col_mot = "Valor"
            text_mot = [fmt_brl(v) for v in df_mot_r["Valor"]]
            y_title_mot = "Valor Total (R$)"
        else:
            df_mot_r = (
                df_r[df_r[motivo_reent_col2].str.strip() != ""]
                .groupby(motivo_reent_col2)
                .agg(Qtd=(motivo_reent_col2,"count"))
                .reset_index().sort_values("Qtd", ascending=False)
            )
            df_mot_r["Valor"] = df_mot_r["Qtd"]
            y_col_mot = "Qtd"
            text_mot = [str(v) for v in df_mot_r["Qtd"]]
            y_title_mot = "Qtd. Reentregas"

        if not df_mot_r.empty:
            n_mot_r = len(df_mot_r)
            bc_mot_r = ["#ef4444" if i<3 else "#f97316" if i<6 else "#0ea5e9" for i in range(n_mot_r)]

            fig_mot_r = go.Figure()
            fig_mot_r.add_trace(go.Bar(
                x=df_mot_r[motivo_reent_col2], y=df_mot_r[y_col_mot],
                name=y_title_mot,
                marker=dict(color=bc_mot_r, opacity=0.9,
                            line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
                text=text_mot, textposition="outside",
                textfont=dict(size=13, color="#ffffff", family="DM Mono", weight="bold"),
                hovertemplate="<b>%{x}</b><br>" + y_title_mot + ": <b>%{text}</b><extra></extra>",
                yaxis="y1",
            ))
            fig_mot_r.add_trace(go.Scatter(
                x=df_mot_r[motivo_reent_col2], y=df_mot_r["Qtd"],
                name="Qtd. Reentregas",
                mode="lines+markers+text",
                line=dict(color="#f59e0b", width=2.5),
                marker=dict(color="#fde68a", size=10, line=dict(color="#f59e0b", width=2)),
                text=df_mot_r["Qtd"].astype(str),
                textposition="top center",
                textfont=dict(size=13, color="#ffffff", family="DM Mono", weight="bold"),
                hovertemplate="<b>%{x}</b><br>Qtd: <b>%{y}</b><extra></extra>",
                yaxis="y2",
            ))
            h_mot_r = max(440, min(n_mot_r * 60, 680))
            fig_mot_r.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.015)",
                font=dict(color="#94a3b8", family="Space Grotesk"),
                height=h_mot_r, margin=dict(t=40, b=110, l=12, r=70), bargap=0.32,
                xaxis=dict(tickfont=dict(color="#b0bec5", size=11, family="Space Grotesk"),
                           gridcolor="rgba(255,255,255,0.04)",
                           linecolor="rgba(255,255,255,0.06)", tickangle=-35, automargin=True),
                yaxis=dict(title=dict(text=y_title_mot, font=dict(color="#64748b", size=11)),
                           tickfont=dict(color="#64748b", size=10),
                           gridcolor="rgba(255,255,255,0.05)",
                           linecolor="rgba(255,255,255,0.06)", tickformat=",.0f", side="left"),
                yaxis2=dict(title=dict(text="Qtd. Reentregas", font=dict(color="#f59e0b", size=11)),
                            tickfont=dict(color="#f59e0b", size=10),
                            overlaying="y", side="right", showgrid=False),
                legend=dict(bgcolor="rgba(8,15,35,0.92)", bordercolor="rgba(56,189,248,0.2)",
                            borderwidth=1, font=dict(color="#94a3b8", size=11),
                            orientation="h", x=1.0, xanchor="right", y=-0.22),
            )
            st.plotly_chart(fig_mot_r, use_container_width=True)
            st.markdown("""
            <div style="display:flex;gap:22px;font-size:0.74rem;color:#64748b;margin-top:-8px;margin-bottom:18px;padding-left:4px;">
              <span>🔴 Top 3 motivos — maior volume</span>
              <span>🟠 4º–6º — atenção</span><span>🔵 Demais motivos</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Sem dados de motivo para o filtro selecionado.")
    else:
        st.warning("Coluna MOTIVOTRANSF não encontrada na planilha de reentregas.")

    st.markdown("---")

    # ── 3 gráficos laterais reentregas ───────────────────────────────────────
    cr1, cr2, cr3 = st.columns(3, gap="medium")

    def make_hbar_reent(df_data, x_col, y_col, color_scale, height=420):
        fig = px.bar(df_data, x=x_col, y=y_col, orientation="h",
                     color=x_col, color_continuous_scale=color_scale,
                     text=[str(v) for v in df_data[x_col]],
                     labels={y_col: "", x_col: "Qtd"})
        fig.update_traces(textposition="outside",
                          textfont=dict(size=11, color="#e2e8f0", family="DM Mono"),
                          cliponaxis=False, marker_line_width=0)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", family="Space Grotesk"), coloraxis_showscale=False,
            height=height, margin=dict(t=10, b=30, l=6, r=80),
            xaxis=dict(tickfont=dict(color="#475569", size=10),
                       gridcolor="rgba(255,255,255,0.04)",
                       linecolor="rgba(255,255,255,0.05)", zeroline=False),
            yaxis=dict(tickfont=dict(color="#cbd5e1", size=11, family="Space Grotesk"),
                       gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)", automargin=True))
        return fig

    with cr1:
        if motivo_reent_col2 and motivo_reent_col2 in df_r.columns:
            df_mr = (df_r[df_r[motivo_reent_col2].str.strip()!=""]
                     .groupby(motivo_reent_col2).agg(Qtd=(motivo_reent_col2,"count"))
                     .reset_index().sort_values("Qtd",ascending=True).tail(8))
            if not df_mr.empty:
                st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ PRINCIPAIS MOTIVOS</h3></div>', unsafe_allow_html=True)
                st.plotly_chart(make_hbar_reent(df_mr, "Qtd", motivo_reent_col2, RED, 420), use_container_width=True)
                top_mr = df_mr.iloc[-1]
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{top_mr[motivo_reent_col2]}</b> — {int(top_mr["Qtd"])} ocorrências</p>', unsafe_allow_html=True)

    with cr2:
        if cliente_reent_col and cliente_reent_col in df_r.columns:
            df_clir = (df_r[df_r[cliente_reent_col].str.strip()!=""]
                       .groupby(cliente_reent_col).agg(Qtd=(cliente_reent_col,"count"))
                       .reset_index().sort_values("Qtd",ascending=True).tail(10))
            if not df_clir.empty:
                st.markdown('<div class="sec-header"><div class="bar"></div><h3>👤 TOP 10 CLIENTES</h3></div>', unsafe_allow_html=True)
                st.plotly_chart(make_hbar_reent(df_clir, "Qtd", cliente_reent_col, MIXED, 420), use_container_width=True)
                top_cr = df_clir.iloc[-1]
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{str(top_cr[cliente_reent_col])[:32]}</b> — {int(top_cr["Qtd"])} reentregas</p>', unsafe_allow_html=True)

    with cr3:
        if nome_reent_col and nome_reent_col in df_r.columns:
            df_nomr = (df_r[df_r[nome_reent_col].str.strip()!=""]
                       .groupby(nome_reent_col).agg(Qtd=(nome_reent_col,"count"))
                       .reset_index().sort_values("Qtd",ascending=True).tail(10))
            if not df_nomr.empty:
                st.markdown('<div class="sec-header"><div class="bar"></div><h3>🧑‍💼 TOP 10 VENDEDORES</h3></div>', unsafe_allow_html=True)
                st.plotly_chart(make_hbar_reent(df_nomr, "Qtd", nome_reent_col, BLUE, 420), use_container_width=True)
                top_nr = df_nomr.iloc[-1]
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{str(top_nr[nome_reent_col])[:32]}</b> — {int(top_nr["Qtd"])} reentregas</p>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Praça (pizza) + Ranking motivos ─────────────────────────────────────
    cr4, cr5 = st.columns([1,2], gap="large")
    with cr4:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏙️ Por Praça</h3></div>', unsafe_allow_html=True)
        if praca_reent_col and praca_reent_col in df_r.columns:
            df_praca_r = (df_r[df_r[praca_reent_col].str.strip()!=""]
                          .groupby(praca_reent_col).agg(Qtd=(praca_reent_col,"count"))
                          .reset_index().sort_values("Qtd",ascending=False).head(10))
            if not df_praca_r.empty:
                fig_pr = px.pie(df_praca_r, names=praca_reent_col, values="Qtd",
                                color_discrete_sequence=MIXED, hole=0.52)
                fig_pr.update_traces(
                    textfont=dict(size=12, color="#e2e8f0"),
                    marker=dict(line=dict(color="rgba(4,9,20,0.8)",width=2)),
                    pull=[0.05]+[0]*(len(df_praca_r)-1))
                st.plotly_chart(plotly_dark(fig_pr, height=360), use_container_width=True)

    with cr5:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>📊 Ranking de Motivos de Transferência</h3></div>', unsafe_allow_html=True)
        if motivo_reent_col2 and motivo_reent_col2 in df_r.columns:
            df_rkr = (df_r.groupby(motivo_reent_col2)
                      .agg(Qtd=(motivo_reent_col2,"count"))
                      .reset_index().sort_values("Qtd",ascending=False))
            total_r = df_rkr["Qtd"].sum()
            df_rkr["% Total"] = (df_rkr["Qtd"]/total_r*100).round(1).astype(str)+"%" if total_r>0 else "0%"

            rows_html_r = ""
            for i, row in df_rkr.iterrows():
                bg = "rgba(74,222,128,0.05)" if i % 2 == 0 else "rgba(0,0,0,0)"
                rows_html_r += f"""<tr style="background:{bg};">
                  <td style="padding:10px 14px;color:#cbd5e1;font-size:0.84rem;border-bottom:1px solid rgba(74,222,128,0.07);">{row[motivo_reent_col2]}</td>
                  <td style="padding:10px 14px;color:#4ade80;font-size:0.84rem;text-align:center;border-bottom:1px solid rgba(74,222,128,0.07);">{row['Qtd']}</td>
                  <td style="padding:10px 14px;color:#f59e0b;font-size:0.84rem;text-align:center;border-bottom:1px solid rgba(74,222,128,0.07);
