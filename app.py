# ── COLUMN FIXES APPLIED based on real spreadsheet:
# ABA DEVOLUÇÕES (8456- DEVOLUCAO 2026):
#   VLTOTAL, DTENT (filter), DTENTREGA (delivery), NOTA_VENDA, NOTA_DEVOLUCAO,
#   NUMCAR, PLACA, DESTINO, MOTIVO, CODCLI, CLIENTE, MOTORISTA, NOMERCA,
#   NOMEFUNC, SUPERVISOR, TIPO_MERCADO, DTSAIDA, PRACA, NOME_CIDADE
# ABA REENTREGAS (8261 - REENTREGAS 2026):
#   VLTOTGER, DTRANSF, NUMTRANSVENDA, CODUSUR, TOTPESO, PLACAANT, PLACAATUAL,
#   MOTIVOTRANSF, CODMOTIVO, CLIENTE, NUMNOTA, NUMPED, PRACA, NOME (vendedor)

import streamlit as st
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
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,.stApp{font-family:'Space Grotesk',sans-serif;color:#e2e8f0;background:#060d1f;}
.bg-overlay{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;}
.bg-img{position:absolute;inset:0;width:100%;height:100%;
  background-image:url('https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1920&q=80');
  background-size:cover;background-position:center center;
  filter:blur(3px) brightness(0.38) saturate(0.6);transform:scale(1.06);}
.bg-tint{position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(4,9,20,0.70) 0%,rgba(6,14,35,0.62) 50%,rgba(4,12,28,0.72) 100%);}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stToolbar"]{background:transparent!important;}
[data-testid="stAppViewContainer"]>section{background:transparent!important;}
.main .block-container{position:relative;z-index:1;}
#MainMenu,footer,header{visibility:hidden!important;display:none!important;}
.stDeployButton{display:none!important;}
[data-testid="stStatusWidget"]{display:none!important;}
[data-testid="stToolbar"]{display:none!important;}
[data-testid="stHeader"]{display:none!important;}
[data-testid="stDecoration"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}

.topbar{
  background:linear-gradient(100deg,rgba(4,10,26,0.98),rgba(7,18,44,0.98),rgba(5,14,34,0.98));
  border-bottom:1px solid rgba(56,189,248,0.18);
  padding:0 48px;height:88px;
  display:flex;align-items:center;
  margin:-6rem -1rem 0;position:sticky;top:0;z-index:999;
  backdrop-filter:blur(28px);box-shadow:0 2px 60px rgba(0,0,0,0.75);}
.topbar-inner{display:flex;align-items:center;gap:24px;width:100%;}
.topbar-icon{width:52px;height:52px;background:linear-gradient(135deg,#0284c7,#1d4ed8);
  border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:24px;
  box-shadow:0 0 0 1px rgba(56,189,248,0.25),0 0 24px rgba(14,165,233,0.4);}
.topbar-divider{width:1px;height:48px;
  background:linear-gradient(180deg,transparent,rgba(56,189,248,0.3),transparent);margin:0 4px;}
.topbar-text{display:flex;flex-direction:column;justify-content:center;gap:4px;}
.topbar-title{font-family:'Bebas Neue',sans-serif!important;font-size:2.15rem!important;
  font-weight:400!important;color:#f8fafc!important;letter-spacing:0.18em;line-height:1;margin:0!important;
  text-shadow:0 0 32px rgba(56,189,248,0.28);}
.topbar-sub{font-family:'Space Grotesk',sans-serif;font-size:0.64rem;color:#334e6e;
  font-weight:600;letter-spacing:0.22em;text-transform:uppercase;margin:0;}

.filter-bar{background:linear-gradient(135deg,rgba(10,18,42,0.93),rgba(12,22,50,0.93));
  border:1px solid rgba(56,189,248,0.2);border-radius:18px;padding:20px 28px 16px;
  margin:20px 0 20px;backdrop-filter:blur(14px);box-shadow:0 4px 30px rgba(0,0,0,0.35);}
.filter-bar-title{font-family:'Bebas Neue',sans-serif;font-size:0.92rem;color:#7dd3fc;
  letter-spacing:0.14em;margin-bottom:14px;}

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
.kpi-value{font-family:'Bebas Neue',sans-serif;font-size:1.65rem;color:#38bdf8;line-height:1;}
.kpi-value-green{font-family:'Bebas Neue',sans-serif;font-size:1.65rem;color:#4ade80;line-height:1;}
.kpi-value-amber{font-family:'Bebas Neue',sans-serif;font-size:1.65rem;color:#f59e0b;line-height:1;}
.kpi-sub{font-size:0.67rem;color:#475569;margin-top:7px;}

.sec-header{display:flex;align-items:center;gap:12px;margin-bottom:16px;}
.sec-header .bar{width:3px;height:24px;background:linear-gradient(180deg,#38bdf8,#2563eb);
  border-radius:2px;box-shadow:0 0 10px rgba(56,189,248,0.5);}
.sec-header h3{font-family:'Bebas Neue',sans-serif;font-size:1.05rem;color:#e2e8f0;margin:0;letter-spacing:0.1em;}

.stTabs [data-baseweb="tab-list"]{background:rgba(8,15,35,0.87)!important;
  border-radius:16px!important;padding:5px!important;gap:4px!important;
  border:1px solid rgba(56,189,248,0.17)!important;margin-bottom:6px;backdrop-filter:blur(10px);}
.stTabs [data-baseweb="tab"]{background:transparent!important;border-radius:12px!important;
  color:#64748b!important;font-weight:600!important;font-size:0.84rem!important;
  padding:10px 24px!important;transition:all .25s!important;border:none!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#0c4a6e,#1e3a8a)!important;
  color:#e0f2fe!important;box-shadow:0 2px 20px rgba(14,165,233,0.3)!important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:26px!important;}

.stTextInput input,.stDateInput input{background:rgba(8,15,35,0.87)!important;
  border-color:rgba(56,189,248,0.22)!important;border-radius:10px!important;
  color:#e2e8f0!important;font-family:'Space Grotesk',sans-serif!important;}
.stSelectbox div[data-baseweb="select"]>div,.stMultiSelect div[data-baseweb="select"]>div{
  background:rgba(8,15,35,0.87)!important;border-color:rgba(56,189,248,0.22)!important;
  border-radius:10px!important;color:#e2e8f0!important;}
.stMultiSelect span[data-baseweb="tag"]{background:rgba(14,165,233,0.18)!important;
  color:#38bdf8!important;border-radius:6px!important;}
label,.stSelectbox label,.stMultiSelect label,.stTextInput label{
  color:#94a3b8!important;font-size:0.76rem!important;font-weight:600!important;
  letter-spacing:.06em!important;text-transform:uppercase!important;}
.stButton>button{background:linear-gradient(135deg,#0c4a6e,#1e3a8a)!important;
  color:#e0f2fe!important;border:1px solid rgba(56,189,248,0.3)!important;
  border-radius:10px!important;font-weight:600!important;font-size:0.84rem!important;
  padding:10px 24px!important;transition:all .25s!important;}
.stButton>button:hover{background:linear-gradient(135deg,#1e3a8a,#1d4ed8)!important;
  border-color:rgba(56,189,248,0.62)!important;transform:translateY(-2px)!important;}
.stDownloadButton>button{background:rgba(34,197,94,0.1)!important;color:#4ade80!important;
  border:1px solid rgba(34,197,94,0.3)!important;border-radius:10px!important;font-weight:600!important;}
hr{border-color:rgba(56,189,248,0.08)!important;margin:22px 0!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:rgba(6,13,31,0.5);}
::-webkit-scrollbar-thumb{background:#1e3a8a;border-radius:3px;}
.stCaption{color:#475569!important;font-size:.72rem!important;}
</style>
""", unsafe_allow_html=True)

def fmt_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except:
        return "R$ 0,00"

def plotly_dark(fig, height=None, margin_b=40):
    u = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,0.32)",
             font=dict(color="#c8d8e8",family="Space Grotesk"),coloraxis_showscale=False,
             margin=dict(t=24,b=margin_b,l=8,r=12),
             xaxis=dict(tickfont=dict(color="#d0dce8",size=14,family="Space Grotesk"),
                        gridcolor="rgba(255,255,255,0.10)",linecolor="rgba(255,255,255,0.12)"),
             yaxis=dict(tickfont=dict(color="#94a3b8",size=13),
                        gridcolor="rgba(255,255,255,0.10)",linecolor="rgba(255,255,255,0.12)"),
             legend=dict(bgcolor="rgba(8,15,35,0.9)",bordercolor="rgba(56,189,248,0.15)",
                         borderwidth=1,font=dict(color="#c8d8e8",size=12)))
    if height: u["height"] = height
    fig.update_layout(**u)
    return fig

BLUE  = ["#0c4a6e","#0369a1","#0ea5e9","#7dd3fc","#bae6fd"]
RED   = ["#7f1d1d","#b91c1c","#ef4444","#fca5a5"]
GREEN = ["#14532d","#15803d","#22c55e","#86efac","#bbf7d0"]
MIXED = ["#0ea5e9","#22c55e","#f59e0b","#ef4444","#a855f7","#ec4899","#14b8a6","#f97316"]

# ── Google Sheets ─────────────────────────────────────────────────────────────
SHEET_ID       = "1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI"
GSHEETS_URL    = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}"
REENTREGAS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=8261+-+REENTREGAS+2026"

@st.cache_data(ttl=60)
def load_data(url):
    r = requests.get(url, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

def parse_brl(s):
    s = str(s).replace("R$","").strip()
    if "," in s and "." in s:
        s = s.replace(".","").replace(",",".")
    elif "," in s:
        s = s.replace(",",".")
    return pd.to_numeric(s, errors="coerce")

# ── Carrega devoluções ────────────────────────────────────────────────────────
with st.spinner("⏳ Carregando dados..."):
    try:
        df_raw = load_data(GSHEETS_URL)
    except Exception as e:
        st.error(f"❌ Erro ao carregar devoluções: {e}")
        st.stop()

# ── Carrega reentregas ────────────────────────────────────────────────────────
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

VALOR_COL     = get_col(df_raw, ["VLTOTAL","VLT","VL_TOTAL","VALOR_LIQUIDO","VALOR","TOTAL"]) or "VLTOTAL"
COL_PLACA     = get_col(df_raw, ["PLACA"])
COL_MOTIVO    = get_col(df_raw, ["MOTIVO","MOTIVO_DEVOLUCAO","MOTIVO_DEV"])
COL_CLIENTE   = get_col(df_raw, ["CLIENTE","NOME_CLIENTE","RAZAO_SOCIAL"])
COL_VENDEDOR  = get_col(df_raw, ["NOMERCA","VENDEDOR","NOME_VENDEDOR"])
COL_DEVOLUCION= get_col(df_raw, ["NOMEFUNC","DEVOLUCIONISTA","FUNCIONARIO"])
COL_MOTORISTA = get_col(df_raw, ["MOTORISTA","ENTREGADOR"])
COL_DESTINO   = get_col(df_raw, ["DESTINO","NOME_CIDADE","CIDADE","MUNICIPIO"])
COL_NF_VENDA  = get_col(df_raw, ["NOTA_VENDA","NF_VENDA","NF_SAIDA","NOTA_SAIDA","NOTA_FISCAL"])
COL_NOTA_DEV  = get_col(df_raw, ["NOTA_DEVOLUCAO","NF_DEVOLUCAO"])
COL_NUMCAR    = get_col(df_raw, ["NUMCAR","NUM_CARREGAMENTO","CARREGAMENTO"])
COL_CODCLI    = get_col(df_raw, ["CODCLI","COD_CLI","CLI"])
COL_SUPERVISOR= get_col(df_raw, ["SUPERVISOR","AM","GERENTE"])
COL_PRACA     = get_col(df_raw, ["PRACA"])
COL_TIPO_MERC = get_col(df_raw, ["TIPO_MERCADO","CANAL","SEGMENTO"])
COL_DTSAIDA   = get_col(df_raw, ["DTSAIDA","DATA_DEVOLUCAO","DATA","DT_DEVOLUCAO"])
COL_DTENTREGA = get_col(df_raw, ["DTENT","DTENTREGA","DATA_ENTREGA","DT_ENTREGA"])

if VALOR_COL not in df_raw.columns:
    df_raw[VALOR_COL] = 0.0

df_raw[VALOR_COL] = df_raw[VALOR_COL].apply(parse_brl).fillna(0)
for col in df_raw.columns:
    if col != VALOR_COL:
        df_raw[col] = df_raw[col].fillna("").astype(str).str.strip()

if COL_DTENTREGA:
    df_raw["_DTENTREGA_DT"] = pd.to_datetime(df_raw[COL_DTENTREGA], dayfirst=True, errors="coerce")
    mask_nat = df_raw["_DTENTREGA_DT"].isna() & (df_raw[COL_DTENTREGA] != "")
    if mask_nat.any():
        df_raw.loc[mask_nat,"_DTENTREGA_DT"] = pd.to_datetime(
            df_raw.loc[mask_nat, COL_DTENTREGA], format="%Y-%m-%d", errors="coerce")
else:
    df_raw["_DTENTREGA_DT"] = pd.NaT

# ── Normaliza colunas reentregas ──────────────────────────────────────────────
REENT_COLS_MAP = {
    "NUMNOTA":           ["NUMNOTA"],
    "DTFAT":             ["DTFAT"],
    "SERIE":             ["SERIE"],
    "ESPECIE":           ["ESPECIE"],
    "DTSAIDA":           ["DTSAIDA"],
    "VLTOTGER":          ["VLTOTGER","VLTOT","VLTOTAL"],
    "TOTPESO":           ["TOTPESO","PESO"],
    "NUMTRANSVENDA":     ["NUMTRANSVENDA","NUMTRANS","VENDA"],
    "NUMCARANTERIOR":    ["NUMCARANTERIOR"],
    "PLACAANT":          ["PLACAANT"],
    "COD_MOT_ANTERIOR":  ["COD MOT ANTERIOR","COD_MOT_ANTERIOR"],
    "NOME_MOT_ANTERIOR": ["NOME MOT ANTERIOR","NOME_MOT_ANTERIOR"],
    "COD_AJU_ANTERIOR":  ["COD AJU ANTERIOR","COD_AJU_ANTERIOR"],
    "NOME_AJU_ANTERIOR": ["NOME AJU ANTERIOR","NOME_AJU_ANTERIOR"],
    "NUMCARATUAL":       ["NUMCARATUAL"],
    "PLACAATUAL":        ["PLACAATUAL"],
    "COD_MOT_ATUAL":     ["COD MOT ATUAL","COD_MOT_ATUAL"],
    "NOME_MOT_ATUAL":    ["NOME MOT ATUAL","NOME_MOT_ATUAL"],
    "COD_AJU_ATUAL":     ["COD AJU ATUAL","COD_AJU_ATUAL"],
    "NOME_AJU_ATUAL":    ["NOME AJU ATUAL","NOME_AJU_ATUAL"],
    "DATATRANSF":        ["DTRANSF","DATATRANSF","DATA_TRANSF"],
    "CODMOTIVO":         ["CODMOTIVO"],
    "MOTIVOTRANSF":      ["MOTIVOTRANSF"],
    "CODCLI":            ["CODCLI"],
    "CLIENTE":           ["CLIENTE"],
    "BAIRROENT":         ["BAIRROENT"],
    "CODPRACA":          ["CODPRACA"],
    "PRACA":             ["PRACA"],
    "ROTA":              ["ROTA"],
    "NUMPED":            ["NUMPED"],
    "CODUSU":            ["CODUSUR","CODUSU"],
    "NOME":              ["NOME","RNOME"],
}

df_reent = None
reent_cols = {}
REENT_VALOR_COL = "_VALOR_REENT"

if df_reent_raw is not None:
    df_reent_raw.columns = [str(c).strip().upper() for c in df_reent_raw.columns]

    def get_col_reent(alts):
        for n in alts:
            if n.strip().upper() in df_reent_raw.columns:
                return n.strip().upper()
        return None

    for canonical, alts in REENT_COLS_MAP.items():
        reent_cols[canonical] = get_col_reent(alts)

    rv = get_col_reent(["VLTOTGER","VLTOT","VLTOTAL","VALOR","TOTAL"])
    if rv:
        REENT_VALOR_COL = rv
        df_reent_raw[rv] = df_reent_raw[rv].apply(parse_brl).fillna(0)
    else:
        df_reent_raw["_VALOR_REENT"] = 0.0

    for col in df_reent_raw.columns:
        if col != REENT_VALOR_COL:
            df_reent_raw[col] = df_reent_raw[col].fillna("").astype(str).str.strip()

    dt_col_r = reent_cols.get("DATATRANSF")
    if dt_col_r:
        df_reent_raw["_DATATRANSF_DT"] = pd.to_datetime(df_reent_raw[dt_col_r], dayfirst=True, errors="coerce")
        m2 = df_reent_raw["_DATATRANSF_DT"].isna() & (df_reent_raw[dt_col_r] != "")
        if m2.any():
            df_reent_raw.loc[m2,"_DATATRANSF_DT"] = pd.to_datetime(
                df_reent_raw.loc[m2, dt_col_r], format="%Y-%m-%d", errors="coerce")
    else:
        df_reent_raw["_DATATRANSF_DT"] = pd.NaT

    df_reent = df_reent_raw.copy()

# ── Background + Topbar ───────────────────────────────────────────────────────
st.markdown("""
<div class="bg-overlay">
  <div class="bg-img"></div>
  <div class="bg-tint"></div>
</div>
""", unsafe_allow_html=True)

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

# ── Filtros globais (devoluções) ──────────────────────────────────────────────
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
        sel_data_str = st.selectbox(f"📅 Filtrar por {col_label}", opcoes_data, key="g_dtsel")
        if sel_data_str != "— Todas as datas —":
            dt_sel = datetime.strptime(sel_data_str, "%d/%m/%Y").date()
            usar_data = True
    else:
        st.caption(f"⚠️ Sem datas válidas em {col_label}")

with fc2:
    if COL_DEVOLUCION:
        devs_opts = sorted([x for x in df_raw[COL_DEVOLUCION].unique() if x not in ("","N/D","nan","None")])
        sel_dev = st.multiselect("👷 NOMEFUNC (Devolucionista)", devs_opts, default=[], key="g_dev", placeholder="Todos")
    else:
        sel_dev = []

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

# ── Aplica filtros ────────────────────────────────────────────────────────────
df = df_raw.copy()
if usar_data and dt_sel:
    df = df[df["_DTENTREGA_DT"].dt.date == dt_sel]
if sel_dev and COL_DEVOLUCION:
    df = df[df[COL_DEVOLUCION].isin(sel_dev)]
if sel_motivo and COL_MOTIVO:
    df = df[df[COL_MOTIVO].isin(sel_motivo)]

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
    st.info(f"🔎 Filtros: {' · '.join(filtros_info)} — **{total_notas} registros filtrados**")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_dash, tab_reent, tab_reent_det, tab_campos, tab_dados = st.tabs([
    "📊  Dashboard",
    "🔄  Reentregas",
    "🔍  Detalhes Reentregas",
    "🗂️  Campos",
    "📑  Dados Completos",
])

# ────────────────────────────────────────────────────────────────────────────
# ABA 1 — DASHBOARD
# ────────────────────────────────────────────────────────────────────────────
with tab_dash:
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-icon">💰</div><div class="kpi-label">Valor Total (VLTOTAL)</div>
        <div class="kpi-value">{fmt_brl(total_val)}</div><div class="kpi-sub">Total devolvido</div></div>
      <div class="kpi-card"><div class="kpi-icon">📄</div><div class="kpi-label">Devoluções</div>
        <div class="kpi-value">{total_notas}</div><div class="kpi-sub">Registros filtrados</div></div>
      <div class="kpi-card"><div class="kpi-icon">👤</div><div class="kpi-label">Clientes</div>
        <div class="kpi-value">{total_clientes}</div><div class="kpi-sub">Clientes únicos</div></div>
      <div class="kpi-card"><div class="kpi-icon">📊</div><div class="kpi-label">Ticket Médio</div>
        <div class="kpi-value">{fmt_brl(ticket_medio)}</div><div class="kpi-sub">Por devolução</div></div>
      <div class="kpi-card"><div class="kpi-icon">🚚</div><div class="kpi-label">Placas</div>
        <div class="kpi-value">{total_placas}</div><div class="kpi-sub">Veículos únicos</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── FUNÇÃO COMBO CHART ATUALIZADA ─────────────────────────────────────────
    def make_combo_chart(df_data, x_col, val_col, qtd_col, title, periodo="", bar_colors=None):
        n = len(df_data)
        if bar_colors is None:
            bar_colors = ["#ef4444" if i<5 else "#f97316" if i<10 else "#0ea5e9" for i in range(n)]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_data[x_col], y=df_data[val_col], name="Valor (R$)",
            marker=dict(color=bar_colors, opacity=0.88, line=dict(color="rgba(255,255,255,0.06)",width=0.5)),
            text=[fmt_brl(v) for v in df_data[val_col]],
            # ── FONTE MAIOR E NEGRITO nos rótulos das barras
            textposition="outside",
            textfont=dict(size=16, color="#ffffff", family="DM Mono"),
            hovertemplate="<b>%{x}</b><br>Valor: <b>%{text}</b><extra></extra>", yaxis="y1",
        ))
        fig.add_trace(go.Scatter(
            x=df_data[x_col], y=df_data[qtd_col], name="Qtd.",
            # ── mode com +text para exibir o valor acima do ponto
            mode="lines+markers+text",
            text=[f"<b>{v}</b>" for v in df_data[qtd_col]],
            textposition="top center",
            textfont=dict(color="#fde68a", size=15, family="DM Mono"),
            line=dict(color="#f59e0b", width=2.5),
            marker=dict(color="#fde68a", size=10, line=dict(color="#f59e0b", width=2), symbol="circle"),
            hovertemplate="<b>%{x}</b><br>Qtd: <b>%{y}</b><extra></extra>", yaxis="y2",
        ))
        h = max(440, min(n*36, 680))
        max_qtd = df_data[qtd_col].max() if len(df_data) > 0 else 1
        fig.update_layout(
            # ── FUNDO MAIS CLARO no gráfico
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.32)",
            font=dict(color="#c8d8e8", family="Space Grotesk"),
            height=h, margin=dict(t=60, b=90, l=12, r=70),
            title=dict(
                text=f"<b>{periodo}</b>",
                font=dict(size=17, color="#ffffff"),
                x=0.5, xanchor="center"
            ),
            bargap=0.28,
            # ── EIXO X: fonte maior e grid mais visível
            xaxis=dict(
                tickfont=dict(color="#d0dce8", size=14, family="DM Mono"),
                gridcolor="rgba(255,255,255,0.10)",
                linecolor="rgba(255,255,255,0.14)",
                tickangle=-38
            ),
            # ── EIXO Y1: fonte maior e grid mais visível
            yaxis=dict(
                title=dict(text="Valor (R$)", font=dict(color="#94a3b8", size=14)),
                tickfont=dict(color="#94a3b8", size=13),
                gridcolor="rgba(255,255,255,0.10)",
                tickformat=",.0f", side="left"
            ),
            # ── EIXO Y2: range reduzido para elevar a linha de quantidade
            yaxis2=dict(
                title=dict(text="Quantidade", font=dict(color="#f59e0b", size=14)),
                tickfont=dict(color="#f59e0b", size=13),
                overlaying="y", side="right", showgrid=False,
                # range menor = linha fica mais alta na área do gráfico
                range=[0, max_qtd * 2.0],
            ),
            legend=dict(
                bgcolor="rgba(8,15,35,0.92)",
                bordercolor="rgba(56,189,248,0.2)",
                borderwidth=1,
                font=dict(color="#c8d8e8", size=14),
                orientation="h", x=1.0, xanchor="right", y=-0.22
            ),
        )
        return fig

    # Gráfico principal: PLACA
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🚚 Devoluções por PLACA — Valor e Quantidade</h3></div>', unsafe_allow_html=True)
    if COL_PLACA:
        df_placa = (df[df[COL_PLACA].str.strip()!=""]
                    .groupby(COL_PLACA).agg(Valor=(VALOR_COL,"sum"),Qtd=(VALOR_COL,"count"))
                    .reset_index().sort_values("Valor",ascending=False))
        if not df_placa.empty:
            n = len(df_placa)
            bc = ["#ef4444" if i<5 else "#f97316" if i<10 else "#0ea5e9" for i in range(n)]
            periodo = f"Data {COL_DTENTREGA}: {dt_sel.strftime('%d/%m/%Y')}" if usar_data and dt_sel else "Todos os períodos"
            st.plotly_chart(make_combo_chart(df_placa,COL_PLACA,"Valor","Qtd","",periodo,bc), use_container_width=True)
            st.markdown('<div style="display:flex;gap:22px;font-size:0.74rem;color:#64748b;margin-top:-8px;margin-bottom:18px;padding-left:4px;"><span>🔴 Top 5 — crítico</span><span>🟠 6–10 — atenção</span><span>🔵 Demais</span><span>🟡 Linha = quantidade</span></div>', unsafe_allow_html=True)
        else:
            st.info("Sem dados de PLACA para o filtro selecionado")
    else:
        st.warning("Coluna PLACA não encontrada")

    st.markdown("---")

    # Gráfico MOTIVO
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Valor por MOTIVO de Devolução</h3></div>', unsafe_allow_html=True)
    if COL_MOTIVO:
        df_mot_v = (df[df[COL_MOTIVO].str.strip()!=""]
                    .groupby(COL_MOTIVO).agg(Valor=(VALOR_COL,"sum"),Qtd=(VALOR_COL,"count"))
                    .reset_index().sort_values("Valor",ascending=False))
        if not df_mot_v.empty:
            n_m = len(df_mot_v)
            bc_m = ["#ef4444" if i<3 else "#f97316" if i<6 else "#0ea5e9" for i in range(n_m)]
            fig_mv = make_combo_chart(df_mot_v, COL_MOTIVO, "Valor", "Qtd", "", "", bc_m)
            fig_mv.update_layout(height=max(440,min(n_m*60,680)), margin=dict(t=40,b=110,l=12,r=70))
            fig_mv.update_xaxes(tickangle=-35, automargin=True)
            st.plotly_chart(fig_mv, use_container_width=True)
            st.markdown('<div style="display:flex;gap:22px;font-size:0.74rem;color:#64748b;margin-top:-8px;margin-bottom:18px;padding-left:4px;"><span>🔴 Top 3 — maior impacto</span><span>🟠 4–6 — atenção</span><span>🔵 Demais</span></div>', unsafe_allow_html=True)
            with st.expander("📋 Tabela de motivos"):
                df_mt = df_mot_v.copy()
                df_mt["Valor (R$)"] = df_mt["Valor"].apply(fmt_brl)
                df_mt["% Total"] = (df_mt["Valor"]/total_val*100).round(1).astype(str)+"%" if total_val>0 else "0%"
                df_mt = df_mt.rename(columns={COL_MOTIVO:"Motivo","Qtd":"Qtd."})
                st.dataframe(df_mt[["Motivo","Qtd.","Valor (R$)","% Total"]], use_container_width=True, hide_index=True)

    st.markdown("---")

    def make_hbar(df_data, x_col, y_col, color_scale, height=420):
        fig = px.bar(df_data,x=x_col,y=y_col,orientation="h",
                     color=x_col,color_continuous_scale=color_scale,
                     text=[fmt_brl(v) for v in df_data[x_col]],
                     labels={y_col:"",x_col:"R$"})
        fig.update_traces(
            textposition="outside",
            textfont=dict(size=14, color="#e2e8f0", family="DM Mono"),
            cliponaxis=False, marker_line_width=0
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.30)",
            font=dict(color="#c8d8e8", family="Space Grotesk"),
            coloraxis_showscale=False,
            height=height, margin=dict(t=10,b=30,l=6,r=110),
            xaxis=dict(
                tickfont=dict(color="#94a3b8", size=13),
                gridcolor="rgba(255,255,255,0.09)", tickformat=",.0f", zeroline=False
            ),
            yaxis=dict(
                tickfont=dict(color="#dde6f0", size=14, family="Space Grotesk"),
                gridcolor="rgba(0,0,0,0)", automargin=True
            )
        )
        return fig

    c1,c2,c3 = st.columns(3,gap="medium")
    with c1:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ TOP MOTIVOS</h3></div>', unsafe_allow_html=True)
        if COL_MOTIVO:
            df_m2 = (df[df[COL_MOTIVO].str.strip()!=""]
                     .groupby(COL_MOTIVO).agg(Valor=(VALOR_COL,"sum"),Qtd=(VALOR_COL,"count"))
                     .reset_index().sort_values("Valor",ascending=True).tail(8))
            if not df_m2.empty:
                st.plotly_chart(make_hbar(df_m2,"Valor",COL_MOTIVO,RED,420),use_container_width=True)
                top=df_m2.iloc[-1]
                pct=top["Valor"]/total_val*100 if total_val>0 else 0
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{top[COL_MOTIVO]}</b> — {pct:.1f}% ({fmt_brl(top["Valor"])})</p>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>👤 TOP 10 CLIENTES</h3></div>', unsafe_allow_html=True)
        if COL_CLIENTE:
            df_cl = (df[df[COL_CLIENTE].str.strip()!=""]
                     .groupby(COL_CLIENTE).agg(Valor=(VALOR_COL,"sum"),Qtd=(VALOR_COL,"count"))
                     .reset_index().sort_values("Valor",ascending=True).tail(10))
            if not df_cl.empty:
                st.plotly_chart(make_hbar(df_cl,"Valor",COL_CLIENTE,MIXED,420),use_container_width=True)
                top_c=df_cl.iloc[-1]
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{str(top_c[COL_CLIENTE])[:30]}</b> — {fmt_brl(top_c["Valor"])}</p>',unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🧑‍💼 TOP 10 NOMERCA (Vendedor)</h3></div>', unsafe_allow_html=True)
        if COL_VENDEDOR:
            df_vv = (df[df[COL_VENDEDOR].str.strip()!=""]
                     .groupby(COL_VENDEDOR).agg(Valor=(VALOR_COL,"sum"),Qtd=(VALOR_COL,"count"))
                     .reset_index().sort_values("Valor",ascending=True).tail(10))
            if not df_vv.empty:
                st.plotly_chart(make_hbar(df_vv,"Valor",COL_VENDEDOR,BLUE,420),use_container_width=True)
                top_v=df_vv.iloc[-1]
                st.markdown(f'<p style="font-size:0.75rem;color:#64748b;padding:0 4px 12px;">📌 <b style="color:#94a3b8">{str(top_v[COL_VENDEDOR])[:30]}</b> — {int(top_v["Qtd"])} devoluções</p>',unsafe_allow_html=True)

    st.markdown("---")
    c4,c5 = st.columns([1,2],gap="large")
    with c4:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏙️ Por DESTINO</h3></div>', unsafe_allow_html=True)
        if COL_DESTINO:
            df_dd = (df[df[COL_DESTINO].str.strip()!=""]
                     .groupby(COL_DESTINO).agg(Valor=(VALOR_COL,"sum"))
                     .reset_index().sort_values("Valor",ascending=False).head(10))
            if not df_dd.empty:
                fig_dd = px.pie(df_dd,names=COL_DESTINO,values="Valor",color_discrete_sequence=MIXED,hole=0.52)
                fig_dd.update_traces(textfont=dict(size=13,color="#ffffff"),
                    marker=dict(line=dict(color="rgba(4,9,20,0.8)",width=2)),pull=[0.05]+[0]*(len(df_dd)-1))
                st.plotly_chart(plotly_dark(fig_dd,height=360),use_container_width=True)
    with c5:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>📊 Ranking de Motivos</h3></div>', unsafe_allow_html=True)
        if COL_MOTIVO:
            df_rk = (df.groupby(COL_MOTIVO).agg(Qtd=(VALOR_COL,"count"),Total=(VALOR_COL,"sum"))
                     .reset_index().sort_values("Total",ascending=False))
            df_rk["Valor Total"] = df_rk["Total"].apply(fmt_brl)
            df_rk["% Total"] = (df_rk["Total"]/total_val*100).round(1).astype(str)+"%" if total_val>0 else "0%"
            rows_h=""
            for i,row in df_rk.rename(columns={COL_MOTIVO:"Motivo"}).iterrows():
                bg="rgba(14,165,233,0.06)" if i%2==0 else "rgba(0,0,0,0)"
                rows_h+=f'<tr style="background:{bg};"><td style="padding:10px 14px;color:#dde6f0;font-size:0.84rem;font-weight:600;border-bottom:1px solid rgba(56,189,248,0.07);">{row["Motivo"]}</td><td style="padding:10px 14px;color:#7dd3fc;text-align:center;font-size:0.84rem;font-weight:700;border-bottom:1px solid rgba(56,189,248,0.07);">{row["Qtd"]}</td><td style="padding:10px 14px;color:#4ade80;font-size:0.84rem;font-weight:600;font-family:monospace;border-bottom:1px solid rgba(56,189,248,0.07);">{row["Valor Total"]}</td><td style="padding:10px 14px;color:#f59e0b;text-align:center;font-size:0.84rem;font-weight:700;border-bottom:1px solid rgba(56,189,248,0.07);">{row["% Total"]}</td></tr>'
            st.markdown(f'<div style="background:rgba(6,13,31,0.92);border:1px solid rgba(56,189,248,0.15);border-radius:14px;overflow:hidden;max-height:360px;overflow-y:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr style="background:rgba(12,26,58,0.98);"><th style="padding:12px 14px;color:#38bdf8;font-size:0.75rem;font-weight:700;letter-spacing:0.08em;text-align:left;text-transform:uppercase;border-bottom:1px solid rgba(56,189,248,0.2);">Motivo</th><th style="padding:12px 14px;color:#38bdf8;font-size:0.75rem;font-weight:700;text-align:center;border-bottom:1px solid rgba(56,189,248,0.2);">Qtd</th><th style="padding:12px 14px;color:#38bdf8;font-size:0.75rem;font-weight:700;border-bottom:1px solid rgba(56,189,248,0.2);">Valor Total</th><th style="padding:12px 14px;color:#38bdf8;font-size:0.75rem;font-weight:700;text-align:center;border-bottom:1px solid rgba(56,189,248,0.2);">%</th></tr></thead><tbody>{rows_h}</tbody></table></div>', unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# ABA 2 — REENTREGAS
# ────────────────────────────────────────────────────────────────────────────
with tab_reent:
    if reent_load_error:
        st.error(f"❌ Erro ao carregar reentregas: {reent_load_error}")
        st.info("💡 Verifique se a aba '8261 - REENTREGAS 2026' está publicada no Google Sheets.")
    elif df_reent is None or len(df_reent) == 0:
        st.warning("⚠️ Nenhum dado encontrado na aba de reentregas.")
    else:
        st.markdown('<div class="filter-bar"><div class="filter-bar-title">⚙️ FILTROS — REENTREGAS</div>', unsafe_allow_html=True)
        rf1,rf2,rf3 = st.columns([3,3,1],gap="medium")
        usar_data_reent = False
        dt_reent_sel = None

        with rf1:
            datas_reent_ok = df_reent["_DATATRANSF_DT"].dropna()
            dt_col_reent = reent_cols.get("DATATRANSF")
            col_label_reent = dt_col_reent if dt_col_reent else "DTRANSF"
            if len(datas_reent_ok) > 0:
                datas_reent_unicas = sorted(datas_reent_ok.dt.date.unique())
                opcoes_reent = ["— Todas as datas —"] + [d.strftime("%d/%m/%Y") for d in datas_reent_unicas]
                sel_reent_str = st.selectbox(f"📅 Filtrar por {col_label_reent}", opcoes_reent, key="r_dtsel")
                if sel_reent_str != "— Todas as datas —":
                    dt_reent_sel = datetime.strptime(sel_reent_str, "%d/%m/%Y").date()
                    usar_data_reent = True
            else:
                st.caption("⚠️ Sem datas DTRANSF válidas")

        with rf2:
            motivo_reent_col = reent_cols.get("MOTIVOTRANSF")
            if motivo_reent_col:
                mot_reent_opts = sorted([x for x in df_reent[motivo_reent_col].unique() if x not in ("","N/D","nan","None")])
                sel_mot_reent = st.multiselect("❗ MOTIVOTRANSF", mot_reent_opts, default=[], key="r_mot", placeholder="Todos")
            else:
                sel_mot_reent = []

        with rf3:
            st.markdown("<br>",unsafe_allow_html=True)
            if st.button("🔄 Atualizar",use_container_width=True,key="btn_reent"):
                st.cache_data.clear()
                st.rerun()

        st.markdown('</div>',unsafe_allow_html=True)

        df_r = df_reent.copy()
        if usar_data_reent and dt_reent_sel:
            df_r = df_r[df_r["_DATATRANSF_DT"].dt.date == dt_reent_sel]
        if sel_mot_reent and motivo_reent_col:
            df_r = df_r[df_r[motivo_reent_col].isin(sel_mot_reent)]

        if usar_data_reent and dt_reent_sel:
            st.info(f"🔎 Filtro: 📅 {dt_reent_sel.strftime('%d/%m/%Y')} — **{len(df_r)} registros**")

        # KPIs
        total_reent       = len(df_r)
        total_reent_valor = df_r[REENT_VALOR_COL].sum() if REENT_VALOR_COL in df_r.columns else 0
        placaant_col      = reent_cols.get("PLACAANT")
        cliente_r_col     = reent_cols.get("CLIENTE")
        praca_r_col       = reent_cols.get("PRACA")
        nome_r_col        = reent_cols.get("NOME")
        motivo_r_col2     = reent_cols.get("MOTIVOTRANSF")
        total_placas_r    = df_r[placaant_col].nunique() if placaant_col and placaant_col in df_r.columns else 0
        total_cli_r       = df_r[cliente_r_col].nunique() if cliente_r_col and cliente_r_col in df_r.columns else 0
        ticket_r          = total_reent_valor/total_reent if total_reent>0 and total_reent_valor>0 else 0

        if total_reent_valor > 0:
            st.markdown(f"""<div class="kpi-grid">
              <div class="kpi-card"><div class="kpi-icon">🔄</div><div class="kpi-label">Total Reentregas</div>
                <div class="kpi-value-amber">{total_reent}</div><div class="kpi-sub">Registros</div></div>
              <div class="kpi-card"><div class="kpi-icon">💰</div><div class="kpi-label">Valor Total (VLTOTGER)</div>
                <div class="kpi-value">{fmt_brl(total_reent_valor)}</div><div class="kpi-sub">Total</div></div>
              <div class="kpi-card"><div class="kpi-icon">👤</div><div class="kpi-label">Clientes</div>
                <div class="kpi-value">{total_cli_r}</div><div class="kpi-sub">Únicos</div></div>
              <div class="kpi-card"><div class="kpi-icon">📊</div><div class="kpi-label">Ticket Médio</div>
                <div class="kpi-value">{fmt_brl(ticket_r)}</div><div class="kpi-sub">Por reentrega</div></div>
              <div class="kpi-card"><div class="kpi-icon">🚚</div><div class="kpi-label">Placas Anteriores</div>
                <div class="kpi-value">{total_placas_r}</div><div class="kpi-sub">PLACAANT</div></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="kpi-grid-4">
              <div class="kpi-card"><div class="kpi-icon">🔄</div><div class="kpi-label">Total Reentregas</div>
                <div class="kpi-value-amber">{total_reent}</div></div>
              <div class="kpi-card"><div class="kpi-icon">👤</div><div class="kpi-label">Clientes</div>
                <div class="kpi-value">{total_cli_r}</div></div>
              <div class="kpi-card"><div class="kpi-icon">🚚</div><div class="kpi-label">Placas Anteriores</div>
                <div class="kpi-value">{total_placas_r}</div></div>
              <div class="kpi-card"><div class="kpi-icon">🗺️</div><div class="kpi-label">Praças</div>
                <div class="kpi-value">{df_r[praca_r_col].nunique() if praca_r_col and praca_r_col in df_r.columns else 0}</div></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # ── FUNÇÃO COMBO REENTREGAS ATUALIZADA ───────────────────────────────
        def make_combo_reent(df_data, x_col, y_col, qtd_col, bar_colors=None):
            n = len(df_data)
            if bar_colors is None:
                bar_colors = ["#ef4444" if i<3 else "#f97316" if i<6 else "#22c55e" for i in range(n)]
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_data[x_col], y=df_data[y_col], name="Qtd.",
                marker=dict(color=bar_colors,opacity=0.88,line=dict(color="rgba(255,255,255,0.06)",width=0.5)),
                text=[f"<b>{v}</b>" for v in df_data[y_col]],
                textposition="outside",
                textfont=dict(size=16, color="#ffffff", family="DM Mono"),
                hovertemplate="<b>%{x}</b><br>Qtd: <b>%{y}</b><extra></extra>", yaxis="y1",
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.32)",
                font=dict(color="#c8d8e8", family="Space Grotesk"),
                height=max(440,min(n*36,680)),
                margin=dict(t=40,b=90,l=12,r=40),
                bargap=0.28,
                xaxis=dict(
                    tickfont=dict(color="#d0dce8", size=14, family="DM Mono"),
                    gridcolor="rgba(255,255,255,0.10)",
                    tickangle=-38
                ),
                yaxis=dict(
                    title=dict(text="Quantidade", font=dict(color="#94a3b8", size=14)),
                    tickfont=dict(color="#94a3b8", size=13),
                    gridcolor="rgba(255,255,255,0.10)"
                ),
                legend=dict(
                    bgcolor="rgba(8,15,35,0.92)",
                    bordercolor="rgba(56,189,248,0.2)",
                    borderwidth=1,
                    font=dict(color="#c8d8e8", size=14),
                    orientation="h", x=1.0, xanchor="right", y=-0.22
                ),
            )
            return fig

        # PLACAANT
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🚚 Reentregas por PLACAANT — Quantidade</h3></div>', unsafe_allow_html=True)
        if placaant_col and placaant_col in df_r.columns:
            df_pr = (df_r[df_r[placaant_col].str.strip()!=""]
                     .groupby(placaant_col).agg(Qtd=(placaant_col,"count"))
                     .reset_index().sort_values("Qtd",ascending=False))
            if not df_pr.empty:
                n_p=len(df_pr)
                bc_p=["#ef4444" if i<3 else "#f97316" if i<6 else "#22c55e" for i in range(n_p)]
                st.plotly_chart(make_combo_reent(df_pr,placaant_col,"Qtd","Qtd",bc_p),use_container_width=True)
                st.markdown('<div style="display:flex;gap:22px;font-size:0.74rem;color:#64748b;margin-top:-8px;margin-bottom:18px;padding-left:4px;"><span>🔴 Top 3 — crítico</span><span>🟠 4–6 — atenção</span><span>🟢 Demais</span></div>',unsafe_allow_html=True)

        st.markdown("---")

        # MOTIVOTRANSF
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Reentregas por MOTIVOTRANSF</h3></div>', unsafe_allow_html=True)
        if motivo_r_col2 and motivo_r_col2 in df_r.columns:
            df_mr = (df_r[df_r[motivo_r_col2].str.strip()!=""]
                     .groupby(motivo_r_col2).agg(Qtd=(motivo_r_col2,"count"))
                     .reset_index().sort_values("Qtd",ascending=False))
            if not df_mr.empty:
                n_mr=len(df_mr)
                bc_mr=["#ef4444" if i<3 else "#f97316" if i<6 else "#0ea5e9" for i in range(n_mr)]
                fig_mr=make_combo_reent(df_mr,motivo_r_col2,"Qtd","Qtd",bc_mr)
                fig_mr.update_layout(height=max(440,min(n_mr*60,680)),margin=dict(t=40,b=110,l=12,r=40))
                fig_mr.update_xaxes(tickangle=-35,automargin=True)
                st.plotly_chart(fig_mr,use_container_width=True)

        st.markdown("---")

        def make_hbar_reent(df_data, x_col, y_col, color_scale, height=420):
            fig=px.bar(df_data,x=x_col,y=y_col,orientation="h",
                       color=x_col,color_continuous_scale=color_scale,
                       text=[f"<b>{v}</b>" for v in df_data[x_col]],
                       labels={y_col:"",x_col:"Qtd"})
            fig.update_traces(
                textposition="outside",
                textfont=dict(size=14, color="#e2e8f0", family="DM Mono"),
                cliponaxis=False, marker_line_width=0
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.30)",
                font=dict(color="#c8d8e8", family="Space Grotesk"),
                coloraxis_showscale=False,
                height=height, margin=dict(t=10,b=30,l=6,r=80),
                xaxis=dict(
                    tickfont=dict(color="#94a3b8", size=13),
                    gridcolor="rgba(255,255,255,0.09)", zeroline=False
                ),
                yaxis=dict(
                    tickfont=dict(color="#dde6f0", size=14, family="Space Grotesk"),
                    gridcolor="rgba(0,0,0,0)", automargin=True
                )
            )
            return fig

        cr1,cr2,cr3=st.columns(3,gap="medium")
        with cr1:
            if motivo_r_col2 and motivo_r_col2 in df_r.columns:
                df_mr2=(df_r[df_r[motivo_r_col2].str.strip()!=""]
                        .groupby(motivo_r_col2).agg(Qtd=(motivo_r_col2,"count"))
                        .reset_index().sort_values("Qtd",ascending=True).tail(8))
                if not df_mr2.empty:
                    st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ PRINCIPAIS MOTIVOS</h3></div>',unsafe_allow_html=True)
                    st.plotly_chart(make_hbar_reent(df_mr2,"Qtd",motivo_r_col2,RED,420),use_container_width=True)
        with cr2:
            if cliente_r_col and cliente_r_col in df_r.columns:
                df_clr=(df_r[df_r[cliente_r_col].str.strip()!=""]
                        .groupby(cliente_r_col).agg(Qtd=(cliente_r_col,"count"))
                        .reset_index().sort_values("Qtd",ascending=True).tail(10))
                if not df_clr.empty:
                    st.markdown('<div class="sec-header"><div class="bar"></div><h3>👤 TOP 10 CLIENTES</h3></div>',unsafe_allow_html=True)
                    st.plotly_chart(make_hbar_reent(df_clr,"Qtd",cliente_r_col,MIXED,420),use_container_width=True)
        with cr3:
            if nome_r_col and nome_r_col in df_r.columns:
                df_nomr=(df_r[df_r[nome_r_col].str.strip()!=""]
                         .groupby(nome_r_col).agg(Qtd=(nome_r_col,"count"))
                         .reset_index().sort_values("Qtd",ascending=True).tail(10))
                if not df_nomr.empty:
                    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🧑‍💼 TOP VENDEDORES (NOME)</h3></div>',unsafe_allow_html=True)
                    st.plotly_chart(make_hbar_reent(df_nomr,"Qtd",nome_r_col,BLUE,420),use_container_width=True)

        st.markdown("---")
        cr4,cr5=st.columns([1,2],gap="large")
        with cr4:
            if praca_r_col and praca_r_col in df_r.columns:
                st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏙️ Por PRACA</h3></div>',unsafe_allow_html=True)
                df_praca_r=(df_r[df_r[praca_r_col].str.strip()!=""]
                            .groupby(praca_r_col).agg(Qtd=(praca_r_col,"count"))
                            .reset_index().sort_values("Qtd",ascending=False).head(10))
                if not df_praca_r.empty:
                    fig_pr=px.pie(df_praca_r,names=praca_r_col,values="Qtd",
                                  color_discrete_sequence=MIXED,hole=0.52)
                    fig_pr.update_traces(textfont=dict(size=13,color="#ffffff"),
                        marker=dict(line=dict(color="rgba(4,9,20,0.8)",width=2)),pull=[0.05]+[0]*(len(df_praca_r)-1))
                    st.plotly_chart(plotly_dark(fig_pr,height=360),use_container_width=True)
        with cr5:
            if motivo_r_col2 and motivo_r_col2 in df_r.columns:
                st.markdown('<div class="sec-header"><div class="bar"></div><h3>📊 Ranking MOTIVOTRANSF</h3></div>',unsafe_allow_html=True)
                df_rkr=(df_r.groupby(motivo_r_col2).agg(Qtd=(motivo_r_col2,"count"))
                        .reset_index().sort_values("Qtd",ascending=False))
                tot_r=df_rkr["Qtd"].sum()
                df_rkr["%"]=( df_rkr["Qtd"]/tot_r*100).round(1).astype(str)+"%" if tot_r>0 else "0%"
                rows_hr=""
                for i,row in df_rkr.iterrows():
                    bg="rgba(74,222,128,0.05)" if i%2==0 else "rgba(0,0,0,0)"
                    rows_hr+=f'<tr style="background:{bg};"><td style="padding:10px 14px;color:#dde6f0;font-size:0.84rem;font-weight:600;border-bottom:1px solid rgba(74,222,128,0.07);">{row[motivo_r_col2]}</td><td style="padding:10px 14px;color:#4ade80;text-align:center;font-size:0.84rem;font-weight:700;border-bottom:1px solid rgba(74,222,128,0.07);">{row["Qtd"]}</td><td style="padding:10px 14px;color:#f59e0b;text-align:center;font-size:0.84rem;font-weight:700;border-bottom:1px solid rgba(74,222,128,0.07);">{row["%"]}</td></tr>'
                st.markdown(f'<div style="background:rgba(6,13,31,0.92);border:1px solid rgba(74,222,128,0.15);border-radius:14px;overflow:hidden;max-height:360px;overflow-y:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr style="background:rgba(12,26,58,0.98);"><th style="padding:12px 14px;color:#4ade80;font-size:0.75rem;font-weight:700;text-align:left;text-transform:uppercase;border-bottom:1px solid rgba(74,222,128,0.2);">Motivo</th><th style="padding:12px 14px;color:#4ade80;font-size:0.75rem;font-weight:700;text-align:center;border-bottom:1px solid rgba(74,222,128,0.2);">Qtd</th><th style="padding:12px 14px;color:#4ade80;font-size:0.75rem;font-weight:700;text-align:center;border-bottom:1px solid rgba(74,222,128,0.2);">%</th></tr></thead><tbody>{rows_hr}</tbody></table></div>',unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# ABA 3 — DETALHES REENTREGAS
# ────────────────────────────────────────────────────────────────────────────
with tab_reent_det:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🔍 Campos das Reentregas — Pesquisa</h3></div>', unsafe_allow_html=True)
    if df_reent is None or len(df_reent)==0:
        st.warning("⚠️ Nenhum dado de reentregas disponível.")
    else:
        det_f1,det_f2=st.columns([3,1],gap="medium")
        usar_data_det=False; dt_det_sel=None
        with det_f1:
            datas_det_ok=df_reent["_DATATRANSF_DT"].dropna()
            dt_col_det=reent_cols.get("DATATRANSF"); col_label_det=dt_col_det if dt_col_det else "DTRANSF"
            if len(datas_det_ok)>0:
                datas_det_unicas=sorted(datas_det_ok.dt.date.unique())
                opcoes_det=["— Todas as datas —"]+[d.strftime("%d/%m/%Y") for d in datas_det_unicas]
                sel_det_str=st.selectbox(f"📅 {col_label_det}",opcoes_det,key="det_dtsel")
                if sel_det_str!="— Todas as datas —":
                    dt_det_sel=datetime.strptime(sel_det_str,"%d/%m/%Y").date(); usar_data_det=True
        with det_f2:
            st.markdown("<br>",unsafe_allow_html=True)
            if st.button("🔄 Atualizar",use_container_width=True,key="btn_det"):
                st.cache_data.clear(); st.rerun()

        df_det_base=df_reent.copy()
        if usar_data_det and dt_det_sel:
            df_det_base=df_det_base[df_det_base["_DATATRANSF_DT"].dt.date==dt_det_sel]
            st.info(f"📅 {dt_det_sel.strftime('%d/%m/%Y')} — {len(df_det_base)} registros")

        ds1,ds2,ds3,ds4=st.columns(4,gap="medium")
        with ds1: s_cli_r=st.text_input("👤 Cliente",placeholder="Nome",key="det_cli")
        with ds2: s_nf_r=st.text_input("📄 Nota (NUMNOTA)",placeholder="Nº",key="det_nf")
        with ds3: s_ped_r=st.text_input("📦 Pedido (NUMPED)",placeholder="Nº",key="det_ped")
        with ds4: s_placa_r=st.text_input("🚚 Placa",placeholder="PLACAANT ou PLACAATUAL",key="det_placa")

        REENT_DISPLAY=[
            ("DATATRANSF","DTRANSF"),("NUMPED","NUMPED"),("NUMNOTA","NUMNOTA"),
            ("DTFAT","DTFAT"),("DTSAIDA","DTSAIDA"),("CLIENTE","CLIENTE"),("CODCLI","CODCLI"),
            ("BAIRROENT","BAIRROENT"),("CODPRACA","CODPRACA"),("PRACA","PRACA"),("ROTA","ROTA"),
            ("NUMCARANTERIOR","CAR.ANT"),("PLACAANT","PLACAANT"),
            ("NOME_MOT_ANTERIOR","MOT.ANT"),("NOME_AJU_ANTERIOR","AJU.ANT"),
            ("NUMCARATUAL","CAR.ATUAL"),("PLACAATUAL","PLACAATUAL"),
            ("NOME_MOT_ATUAL","MOT.ATUAL"),("NOME_AJU_ATUAL","AJU.ATUAL"),
            ("CODMOTIVO","COD.MOTIVO"),("MOTIVOTRANSF","MOTIVO"),
            ("VLTOTGER","VLTOTGER"),("TOTPESO","PESO"),("NOME","VENDEDOR"),("CODUSU","CODUSU"),
        ]
        cols_det_ok=[(reent_cols.get(k),label) for k,label in REENT_DISPLAY if reent_cols.get(k) is not None]
        df_det=df_det_base[[o for o,_ in cols_det_ok]].copy()
        df_det.columns=[label for _,label in cols_det_ok]

        if s_cli_r.strip() and "CLIENTE" in df_det.columns: df_det=df_det[df_det["CLIENTE"].str.contains(s_cli_r.strip(),case=False,na=False)]
        if s_nf_r.strip() and "NUMNOTA" in df_det.columns: df_det=df_det[df_det["NUMNOTA"].str.contains(s_nf_r.strip(),case=False,na=False)]
        if s_ped_r.strip() and "NUMPED" in df_det.columns: df_det=df_det[df_det["NUMPED"].str.contains(s_ped_r.strip(),case=False,na=False)]
        if s_placa_r.strip():
            mask_p=pd.Series([False]*len(df_det),index=df_det.index)
            for cp in ["PLACAANT","PLACAATUAL"]:
                if cp in df_det.columns: mask_p=mask_p|df_det[cp].str.contains(s_placa_r.strip(),case=False,na=False)
            df_det=df_det[mask_p]

        st.markdown("---")
        st.caption(f"Exibindo {len(df_det):,} registros".replace(",","."))
        if len(df_det)==0:
            st.warning("⚠️ Nenhum registro encontrado.")
        else:
            heads="".join([f'<th style="padding:11px 13px;color:#4ade80;font-size:0.74rem;font-weight:700;text-align:left;text-transform:uppercase;white-space:nowrap;border-bottom:1px solid rgba(74,222,128,0.22);background:rgba(10,26,48,0.99);">{c}</th>' for c in df_det.columns])
            rws=""
            for idx,(_,row) in enumerate(df_det.head(500).iterrows()):
                bg="rgba(74,222,128,0.04)" if idx%2==0 else "rgba(0,0,0,0)"
                cells="".join([f'<td style="padding:9px 13px;color:#dde6f0;font-size:0.83rem;font-weight:500;border-bottom:1px solid rgba(74,222,128,0.05);white-space:nowrap;">{val}</td>' for val in row.values])
                rws+=f'<tr style="background:{bg};">{cells}</tr>'
            st.markdown(f'<div style="background:rgba(5,11,28,0.94);border:1px solid rgba(74,222,128,0.16);border-radius:14px;overflow:hidden;max-height:560px;overflow-y:auto;overflow-x:auto;"><table style="width:100%;border-collapse:collapse;min-width:1100px;"><thead><tr>{heads}</tr></thead><tbody>{rws}</tbody></table></div>',unsafe_allow_html=True)
            csv_det=df_det.to_csv(index=False,sep=";",decimal=",").encode("utf-8-sig")
            st.markdown("<div style='margin-top:12px;'></div>",unsafe_allow_html=True)
            st.download_button("⬇️ Exportar (.csv)",data=csv_det,
                file_name=f"reentregas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",mime="text/csv")


# ────────────────────────────────────────────────────────────────────────────
# ABA 4 — CAMPOS (devoluções)
# ────────────────────────────────────────────────────────────────────────────
with tab_campos:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🗂️ Campos — Devoluções</h3></div>', unsafe_allow_html=True)
    sr1,sr2,sr3,sr4=st.columns(4,gap="medium")
    with sr1: s_cli=st.text_input("👤 CLIENTE",placeholder="Nome",key="sc_cli")
    with sr2: s_nf=st.text_input("📄 NOTA_VENDA",placeholder="Nº",key="sc_nf")
    with sr3: s_ped=st.text_input("📦 CODCLI",placeholder="Código",key="sc_ped")
    with sr4: s_placa2=st.text_input("🚚 PLACA",placeholder="Ex: NPB1J08",key="sc_placa")

    CAMPOS=[
        (COL_DTENTREGA,  "DTENT"),
        (COL_DTSAIDA,    "DTSAIDA"),
        (COL_NF_VENDA,   "NOTA_VENDA"),
        (COL_NOTA_DEV,   "NOTA_DEVOLUCAO"),
        (COL_NUMCAR,     "NUMCAR"),
        (COL_PLACA,      "PLACA"),
        (COL_DESTINO,    "DESTINO"),
        (COL_MOTIVO,     "MOTIVO"),
        (COL_CODCLI,     "CODCLI"),
        (COL_CLIENTE,    "CLIENTE"),
        (COL_MOTORISTA,  "MOTORISTA"),
        (COL_VENDEDOR,   "NOMERCA"),
        (COL_DEVOLUCION, "NOMEFUNC"),
        (COL_SUPERVISOR, "SUPERVISOR"),
        (COL_TIPO_MERC,  "TIPO_MERCADO"),
    ]
    cols_ok=[(o,a) for o,a in CAMPOS if o is not None]
    df_campos=df[[o for o,_ in cols_ok]].copy()
    df_campos.columns=[a for _,a in cols_ok]

    if s_cli.strip() and "CLIENTE" in df_campos.columns: df_campos=df_campos[df_campos["CLIENTE"].str.contains(s_cli.strip(),case=False,na=False)]
    if s_nf.strip() and "NOTA_VENDA" in df_campos.columns: df_campos=df_campos[df_campos["NOTA_VENDA"].str.contains(s_nf.strip(),case=False,na=False)]
    if s_ped.strip() and "CODCLI" in df_campos.columns: df_campos=df_campos[df_campos["CODCLI"].str.contains(s_ped.strip(),case=False,na=False)]
    if s_placa2.strip() and "PLACA" in df_campos.columns: df_campos=df_campos[df_campos["PLACA"].str.contains(s_placa2.strip(),case=False,na=False)]

    if usar_data and dt_sel:
        st.info(f"📅 Filtro ativo: {dt_sel.strftime('%d/%m/%Y')} ({COL_DTENTREGA})")

    st.markdown("---")
    st.caption(f"Exibindo {len(df_campos):,} registros".replace(",","."))

    if len(df_campos)==0:
        st.warning("⚠️ Nenhum registro encontrado.")
    else:
        heads_c="".join([f'<th style="padding:11px 13px;color:#38bdf8;font-size:0.74rem;font-weight:700;text-align:left;text-transform:uppercase;white-space:nowrap;border-bottom:1px solid rgba(56,189,248,0.22);background:rgba(12,26,58,0.99);">{c}</th>' for c in df_campos.columns])
        rows_hc=""
        for idx,(_,row) in enumerate(df_campos.head(500).iterrows()):
            bg="rgba(14,165,233,0.05)" if idx%2==0 else "rgba(0,0,0,0)"
            cells="".join([f'<td style="padding:9px 13px;color:#dde6f0;font-size:0.83rem;font-weight:500;border-bottom:1px solid rgba(56,189,248,0.06);white-space:nowrap;">{val}</td>' for val in row.values])
            rows_hc+=f'<tr style="background:{bg};">{cells}</tr>'
        st.markdown(f'<div style="background:rgba(5,11,28,0.94);border:1px solid rgba(56,189,248,0.16);border-radius:14px;overflow:hidden;max-height:560px;overflow-y:auto;overflow-x:auto;"><table style="width:100%;border-collapse:collapse;min-width:900px;"><thead><tr>{heads_c}</tr></thead><tbody>{rows_hc}</tbody></table></div>',unsafe_allow_html=True)
        if len(df_campos)>500: st.caption(f"⚠️ Exibindo primeiros 500 de {len(df_campos)}.")
        csv_c=df_campos.to_csv(index=False,sep=";",decimal=",").encode("utf-8-sig")
        st.markdown("<div style='margin-top:12px;'></div>",unsafe_allow_html=True)
        st.download_button("⬇️ Exportar (.csv)",data=csv_c,
            file_name=f"campos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",mime="text/csv")


# ────────────────────────────────────────────────────────────────────────────
# ABA 5 — DADOS COMPLETOS
# ────────────────────────────────────────────────────────────────────────────
with tab_dados:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>📑 Dados Completos</h3></div>', unsafe_allow_html=True)

    display_cols=[c for c in actual_cols if not c.startswith("_")]
    d1,d2,d3=st.columns(3,gap="medium")
    sort_opts=[VALOR_COL]+[c for c in [COL_DTSAIDA,COL_DTENTREGA,COL_CLIENTE,COL_MOTIVO,COL_PLACA] if c]
    with d1: sort_col=st.selectbox("Ordenar por",sort_opts)
    with d2: sort_asc=st.radio("Direção",["↑ Crescente","↓ Decrescente"],horizontal=True)=="↑ Crescente"
    with d3: n_rows=st.selectbox("Máximo de linhas",[50,100,250,500,1000,"Todos"])

    df_sorted=df.sort_values(sort_col,ascending=sort_asc)
    if n_rows!="Todos": df_sorted=df_sorted.head(int(n_rows))
    disp=df_sorted[display_cols]

    heads_d="".join([f'<th style="padding:11px 13px;color:#38bdf8;font-size:0.74rem;font-weight:700;text-align:left;text-transform:uppercase;white-space:nowrap;border-bottom:1px solid rgba(56,189,248,0.22);background:rgba(12,26,58,0.99);">{c}</th>' for c in disp.columns])
    rows_hd=""
    for idx,(_,row) in enumerate(disp.head(500).iterrows()):
        bg="rgba(14,165,233,0.05)" if idx%2==0 else "rgba(0,0,0,0)"
        cells="".join([f'<td style="padding:9px 13px;color:#dde6f0;font-size:0.83rem;font-weight:500;border-bottom:1px solid rgba(56,189,248,0.06);white-space:nowrap;">{val}</td>' for val in row.values])
        rows_hd+=f'<tr style="background:{bg};">{cells}</tr>'
    st.markdown(f'<div style="background:rgba(5,11,28,0.94);border:1px solid rgba(56,189,248,0.16);border-radius:14px;overflow:hidden;max-height:520px;overflow-y:auto;overflow-x:auto;"><table style="width:100%;border-collapse:collapse;min-width:900px;"><thead><tr>{heads_d}</tr></thead><tbody>{rows_hd}</tbody></table></div>',unsafe_allow_html=True)
    st.caption(f"Exibindo {len(disp.head(500)):,} de {len(df):,} registros".replace(",","."))

    st.markdown("---")
    e1,e2=st.columns(2)
    with e1:
        csv_all=df[display_cols].to_csv(index=False,sep=";",decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar filtrados (.csv)",data=csv_all,
            file_name=f"devolucoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",mime="text/csv",use_container_width=True)
    with e2:
        if st.button("🔄 Atualizar Dados",use_container_width=True):
            st.cache_data.clear(); st.rerun()

    with st.expander("🔍 Diagnóstico — colunas detectadas"):
        st.write(f"**Colunas devoluções ({len(actual_cols)}):** `{actual_cols}`")
        st.write(f"Valor=`{VALOR_COL}` | Placa=`{COL_PLACA}` | Motivo=`{COL_MOTIVO}`")
        st.write(f"Cliente=`{COL_CLIENTE}` | Devolucionista=`{COL_DEVOLUCION}`")
        st.write(f"DataEntrada(DTENT)=`{COL_DTENTREGA}` | DataSaída=`{COL_DTSAIDA}`")
        st.write(f"Supervisor=`{COL_SUPERVISOR}` | Destino=`{COL_DESTINO}` | Nota Dev=`{COL_NOTA_DEV}`")
        st.write(f"Registros com valor > 0: {(df_raw[VALOR_COL]>0).sum()}")
        if df_reent is not None:
            st.write(f"**Colunas reentregas:** `{list(df_reent_raw.columns)}`")
            st.write(f"Valor reent=`{REENT_VALOR_COL}` | PLACAANT=`{reent_cols.get('PLACAANT')}` | MOTIVOTRANSF=`{reent_cols.get('MOTIVOTRANSF')}`")
