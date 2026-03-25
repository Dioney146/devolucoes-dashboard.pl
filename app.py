import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
from datetime import datetime, date

st.set_page_config(
    page_title="Devoluções Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,.stApp{font-family:'Space Grotesk',sans-serif;color:#e2e8f0;background:#060d1f;}
/* Background image via fixed div injected below */
.bg-overlay{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;}
.bg-img{position:absolute;inset:0;width:100%;height:100%;
  background-image:url('https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1920&q=80');
  background-size:cover;background-position:center center;
  filter:blur(6px) brightness(0.13) saturate(0.4);transform:scale(1.06);}
.bg-tint{position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(4,9,20,0.93) 0%,rgba(6,14,35,0.88) 50%,rgba(4,12,28,0.95) 100%);}
/* Make streamlit containers transparent so bg shows through */
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stToolbar"]{background:transparent!important;}
[data-testid="stAppViewContainer"]>section{background:transparent!important;}
.main .block-container{position:relative;z-index:1;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}

.topbar{background:linear-gradient(90deg,rgba(8,15,35,0.98),rgba(10,20,45,0.98));
  border-bottom:1px solid rgba(56,189,248,0.22);padding:16px 36px;
  display:flex;align-items:center;justify-content:space-between;
  margin:-6rem -1rem 0;position:sticky;top:0;z-index:999;
  backdrop-filter:blur(20px);box-shadow:0 4px 40px rgba(0,0,0,0.6);}
.topbar-brand{display:flex;align-items:center;gap:14px;}
.topbar-brand .icon{width:42px;height:42px;background:linear-gradient(135deg,#0ea5e9,#2563eb);
  border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;
  box-shadow:0 0 20px rgba(14,165,233,0.4);}
.topbar-brand h1{font-family:'Bebas Neue',sans-serif!important;font-size:1.65rem!important;
  font-weight:400!important;color:#f0f9ff!important;letter-spacing:0.12em;margin:0!important;}
.topbar-brand span{font-size:0.68rem;color:#475569;display:block;font-weight:400;
  letter-spacing:0.1em;text-transform:uppercase;}
.topbar-right{display:flex;align-items:center;gap:18px;}
.live-badge{background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.35);
  border-radius:50px;padding:6px 16px;font-size:0.72rem;color:#4ade80;font-weight:600;
  letter-spacing:0.06em;text-transform:uppercase;}
.live-dot{display:inline-block;width:7px;height:7px;background:#4ade80;border-radius:50%;
  margin-right:6px;animation:pulse 2s infinite;box-shadow:0 0 8px #4ade80;}
@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 8px #4ade80;}50%{opacity:0.4;box-shadow:0 0 3px #4ade80;}}
.topbar-time{font-family:'DM Mono',monospace;font-size:0.72rem;color:#475569;letter-spacing:0.06em;}

.filter-bar{background:linear-gradient(135deg,rgba(10,18,42,0.93),rgba(12,22,50,0.93));
  border:1px solid rgba(56,189,248,0.2);border-radius:18px;padding:20px 28px 16px;
  margin:20px 0 20px;backdrop-filter:blur(14px);box-shadow:0 4px 30px rgba(0,0,0,0.35);}
.filter-bar-title{font-family:'Bebas Neue',sans-serif;font-size:0.92rem;color:#7dd3fc;
  letter-spacing:0.14em;margin-bottom:14px;display:flex;align-items:center;gap:8px;}

.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:28px;}
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
.kpi-sub{font-size:0.67rem;color:#475569;margin-top:7px;}

.sec-header{display:flex;align-items:center;gap:12px;margin-bottom:16px;}
.sec-header .bar{width:3px;height:24px;background:linear-gradient(180deg,#38bdf8,#2563eb);
  border-radius:2px;box-shadow:0 0 10px rgba(56,189,248,0.5);}
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
.stRadio label{color:#94a3b8!important;font-size:0.85rem!important;}
hr{border-color:rgba(56,189,248,0.08)!important;margin:22px 0!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:rgba(6,13,31,0.5);}
::-webkit-scrollbar-thumb{background:#1e3a8a;border-radius:3px;}
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
MIXED = ["#0ea5e9","#22c55e","#f59e0b","#ef4444","#a855f7","#ec4899","#14b8a6","#f97316"]

# ── Carrega planilha ──────────────────────────────────────────────────────────
SHEET_ID    = "1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI"
GSHEETS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}"

@st.cache_data(ttl=60)
def load_data(url):
    r = requests.get(url, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

with st.spinner("⏳ Carregando dados..."):
    try:
        df_raw = load_data(GSHEETS_URL)
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        st.stop()

# ── Normaliza colunas ─────────────────────────────────────────────────────────
df_raw.columns = [str(c).strip().upper().replace(" ","_") for c in df_raw.columns]
actual_cols = list(df_raw.columns)

def get_col(names):
    for n in names:
        if n in df_raw.columns:
            return n
    return None

VALOR_COL     = get_col(["VLT","VLTOTAL","VL_TOTAL","VALOR_LIQUIDO","VALOR","TOTAL","VLF"]) or "VLT"
COL_PLACA     = get_col(["PLACA","PLACA_VEICULO","VEICULO"])
COL_MOTIVO    = get_col(["MOTIVO","MOTIVO_DEVOLUCAO","MOTIVO_DEV","CONF_MATRICULA"])
COL_CLIENTE   = get_col(["CLIENTE","NOMERCA","NOME_CLIENTE","RAZAO_SOCIAL"])
COL_VENDEDOR  = get_col(["NOMERCA","VENDEDOR","NOME_VENDEDOR"])
COL_DEVOLUCION= get_col(["NOMEFUNC","DEVOLUCIONISTA","FUNCIONARIO","NOME_FUNC"])
COL_MOTORISTA = get_col(["MOTORISTA","ENTREGADOR"])
COL_DESTINO   = get_col(["DESTINO","CIDADE","MUNICIPIO","PRACA","CODPRA"])
COL_NF_VENDA  = get_col(["NOTA_VENDA","NF_VENDA","NF_SAIDA","NOTA_SAIDA","NOTA_FISCAL","NUMERO"])
COL_NUMCAR    = get_col(["NUMCAR","NUM_CARREGAMENTO","CARREGAMENTO","NR_CARREGAMENTO"])
COL_CODCLI    = get_col(["CODCLI","COD_CLI","CLI","NUM_PEDIDO","PEDIDO"])
COL_DTSAIDA   = get_col(["DTSAIDA","DATA_DEVOLUCAO","DATA","DT_DEVOLUCAO","DATA_EMISSAO"])
COL_DTENTREGA = get_col(["DTENTREGA","DATA_ENTREGA","DT_ENTREGA","DATAENTREGA"])

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
else:
    df_raw["_DTENTREGA_DT"] = pd.NaT

# ── TOPBAR ────────────────────────────────────────────────────────────────────
# Inject background overlay div — works reliably in Streamlit
st.markdown("""
<div class="bg-overlay">
  <div class="bg-img"></div>
  <div class="bg-tint"></div>
</div>
""", unsafe_allow_html=True)

now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">
    <div class="icon">📦</div>
    <div><h1>DEVOLUÇÕES</h1><span>Sistema de Análise e Controle</span></div>
  </div>
  <div class="topbar-right">
    <div class="live-badge"><span class="live-dot"></span>Ao Vivo</div>
    <div class="topbar-time">🕐 {now_str}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FILTROS GLOBAIS
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="filter-bar"><div class="filter-bar-title">⚙️ FILTROS GLOBAIS</div>', unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns([3, 2, 2, 1], gap="medium")

usar_data = False
dt_sel = None

with fc1:
    datas_ok = df_raw["_DTENTREGA_DT"].dropna()
    if len(datas_ok) > 0:
        datas_unicas = sorted(datas_ok.dt.date.unique())
        opcoes_data = ["— Todas as datas —"] + [d.strftime("%d/%m/%Y") for d in datas_unicas]
        sel_data_str = st.selectbox("📅 Data de Entrega (DTENT)", opcoes_data, key="g_dtsel")
        if sel_data_str != "— Todas as datas —":
            dt_sel = datetime.strptime(sel_data_str, "%d/%m/%Y").date()
            usar_data = True
    else:
        st.caption("⚠️ Sem datas DTENT válidas na planilha")

with fc2:
    if COL_DEVOLUCION:
        devs_opts = sorted([x for x in df_raw[COL_DEVOLUCION].unique() if x not in ("","N/D","nan","None")])
        sel_dev = st.multiselect("👷 Devolucionista (NOMEFUNC)", devs_opts, default=[], key="g_dev",
                                 placeholder="Todos")
    else:
        sel_dev = []
        st.caption("⚠️ NOMEFUNC não encontrado")

with fc3:
    if COL_MOTIVO:
        mot_opts = sorted([x for x in df_raw[COL_MOTIVO].unique() if x not in ("","N/D","nan","None")])
        sel_motivo = st.multiselect("❗ Motivo", mot_opts, default=[], key="g_mot",
                                    placeholder="Todos")
    else:
        sel_motivo = []

with fc4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Atualizar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── Aplica filtros ─────────────────────────────────────────────────────────────
df = df_raw.copy()

if usar_data and dt_sel:
    mask = df["_DTENTREGA_DT"].dt.date == dt_sel
    df = df[mask]

if sel_dev and COL_DEVOLUCION:
    df = df[df[COL_DEVOLUCION].isin(sel_dev)]

if sel_motivo and COL_MOTIVO:
    df = df[df[COL_MOTIVO].isin(sel_motivo)]

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_val      = df[VALOR_COL].sum()
total_notas    = len(df)
total_clientes = df[COL_CLIENTE].nunique() if COL_CLIENTE else 0
ticket_medio   = total_val / total_notas if total_notas > 0 else 0
total_placas   = df[COL_PLACA].nunique() if COL_PLACA else 0

# Info de filtros ativos
filtros_info = []
if usar_data and dt_sel:
    filtros_info.append(f"📅 {dt_sel.strftime('%d/%m/%Y')}")
if sel_dev:
    filtros_info.append(f"👷 {', '.join(sel_dev[:2])}{'...' if len(sel_dev)>2 else ''}")
if sel_motivo:
    filtros_info.append(f"❗ {len(sel_motivo)} motivo(s)")
if filtros_info:
    st.info(f"🔎 Filtros: {' · '.join(filtros_info)} — **{total_notas} registros filtrados**")

# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
tab_dash, tab_campos, tab_dados = st.tabs([
    "📊  Dashboard",
    "🗂️  Campos",
    "📑  Dados Completos",
])

# ══════════════════════════════════════════════════════════════
# ABA 1 — DASHBOARD
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

    # ── GRÁFICO PRINCIPAL: Barras (valor) + Linha (quantidade) ────────────────
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
            # Cores: top 5 vermelho, 6-10 laranja, resto azul
            bar_colors = []
            for i in range(n):
                if i < 5:      bar_colors.append("#ef4444")
                elif i < 10:   bar_colors.append("#f97316")
                else:          bar_colors.append("#0ea5e9")

            periodo = ""
            if usar_data and dt_sel:
                periodo = f"Data: {dt_sel.strftime('%d/%m/%Y')}"

            fig_placa = go.Figure()

            fig_placa.add_trace(go.Bar(
                x=df_placa[COL_PLACA],
                y=df_placa["Valor"],
                name="Soma Valor (R$)",
                marker=dict(color=bar_colors, opacity=0.88,
                            line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
                text=[fmt_brl(v) for v in df_placa["Valor"]],
                textposition="outside",
                textfont=dict(size=9, color="#94a3b8", family="DM Mono"),
                hovertemplate="<b>%{x}</b><br>Valor: <b>%{text}</b><extra></extra>",
                yaxis="y1",
            ))

            fig_placa.add_trace(go.Scatter(
                x=df_placa[COL_PLACA],
                y=df_placa["Qtd"],
                name="Qtd. Devoluções",
                mode="lines+markers+text",
                line=dict(color="#f59e0b", width=2.5),
                marker=dict(color="#fde68a", size=10,
                            line=dict(color="#f59e0b", width=2)),
                text=df_placa["Qtd"].astype(str),
                textposition="top center",
                textfont=dict(size=10, color="#fde68a", family="DM Mono"),
                hovertemplate="<b>%{x}</b><br>Qtd: <b>%{y}</b><extra></extra>",
                yaxis="y2",
            ))

            h = max(440, min(n * 36, 680))
            fig_placa.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.015)",
                font=dict(color="#94a3b8", family="Space Grotesk"),
                height=h,
                margin=dict(t=50, b=90, l=12, r=70),
                title=dict(text=f"<b>{periodo}</b>",
                           font=dict(size=13, color="#64748b"), x=0.5, xanchor="center"),
                bargap=0.28,
                xaxis=dict(tickfont=dict(color="#b0bec5", size=11, family="DM Mono"),
                           gridcolor="rgba(255,255,255,0.04)",
                           linecolor="rgba(255,255,255,0.06)",
                           tickangle=-38),
                yaxis=dict(
                    title=dict(text="Soma de Valor (R$)", font=dict(color="#64748b", size=11)),
                    tickfont=dict(color="#64748b", size=10),
                    gridcolor="rgba(255,255,255,0.05)",
                    linecolor="rgba(255,255,255,0.06)",
                    tickformat=",.0f", side="left",
                ),
                yaxis2=dict(
                    title=dict(text="Contagem de Devoluções", font=dict(color="#f59e0b", size=11)),
                    tickfont=dict(color="#f59e0b", size=10),
                    overlaying="y", side="right", showgrid=False,
                ),
                legend=dict(bgcolor="rgba(8,15,35,0.92)",
                            bordercolor="rgba(56,189,248,0.2)", borderwidth=1,
                            font=dict(color="#94a3b8", size=11),
                            orientation="h", x=0.5, xanchor="center", y=1.06),
            )

            st.plotly_chart(fig_placa, use_container_width=True)

            st.markdown("""
            <div style="display:flex;gap:22px;font-size:0.74rem;color:#64748b;margin-top:-8px;margin-bottom:18px;padding-left:4px;">
              <span>🔴 Top 5 — crítico</span>
              <span>🟠 6–10 — atenção</span>
              <span>🔵 Demais placas</span>
              <span>🟡 Linha = quantidade de devoluções</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Sem dados de placa para o filtro selecionado")
    else:
        st.warning("Coluna PLACA não encontrada na planilha")

    # ── GRÁFICO: Motivo por Placa ────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Motivo de Devolução por Placa</h3></div>', unsafe_allow_html=True)

    if COL_PLACA and COL_MOTIVO:
        df_pm = (
            df[(df[COL_PLACA].str.strip() != "") & (df[COL_MOTIVO].str.strip() != "")]
            .groupby([COL_PLACA, COL_MOTIVO])
            .agg(Qtd=(VALOR_COL, "count"), Valor=(VALOR_COL, "sum"))
            .reset_index()
        )
        if not df_pm.empty:
            # Pega top motivo por placa para label
            top_motivos = df_pm.loc[df_pm.groupby(COL_PLACA)["Qtd"].idxmax()][[COL_PLACA, COL_MOTIVO, "Qtd", "Valor"]].copy()
            
            # Ordena pelas mesmas placas do grafico principal
            if not df_placa.empty:
                placa_order = df_placa[COL_PLACA].tolist()
                top_motivos[COL_PLACA] = pd.Categorical(top_motivos[COL_PLACA], categories=placa_order, ordered=True)
                top_motivos = top_motivos.sort_values(COL_PLACA)

            # Gráfico stacked bar — todas as combinações placa x motivo
            df_pm_sorted = df_pm.copy()
            if not df_placa.empty:
                df_pm_sorted[COL_PLACA] = pd.Categorical(df_pm_sorted[COL_PLACA], categories=placa_order, ordered=True)
                df_pm_sorted = df_pm_sorted.sort_values(COL_PLACA)

            fig_pm = px.bar(
                df_pm_sorted,
                x=COL_PLACA,
                y="Qtd",
                color=COL_MOTIVO,
                color_discrete_sequence=MIXED,
                barmode="stack",
                text="Qtd",
                labels={COL_PLACA: "Placa", "Qtd": "Qtd. Devoluções", COL_MOTIVO: "Motivo"},
                custom_data=[COL_MOTIVO, "Valor"],
            )
            fig_pm.update_traces(
                textposition="inside",
                textfont_size=9,
                hovertemplate="<b>%{x}</b><br>Motivo: %{customdata[0]}<br>Qtd: %{y}<extra></extra>",
            )
            h_pm = max(420, min(len(df_pm_sorted[COL_PLACA].unique()) * 34, 680))
            fig_pm.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.015)",
                font=dict(color="#94a3b8", family="Space Grotesk"),
                height=h_pm,
                margin=dict(t=30, b=90, l=12, r=12),
                bargap=0.28,
                xaxis=dict(tickfont=dict(color="#b0bec5", size=11, family="DM Mono"),
                           gridcolor="rgba(255,255,255,0.04)",
                           linecolor="rgba(255,255,255,0.06)",
                           tickangle=-38),
                yaxis=dict(tickfont=dict(color="#64748b", size=10),
                           gridcolor="rgba(255,255,255,0.05)"),
                legend=dict(bgcolor="rgba(8,15,35,0.92)",
                            bordercolor="rgba(56,189,248,0.18)", borderwidth=1,
                            font=dict(color="#94a3b8", size=10),
                            title_text="Motivo",
                            orientation="v"),
            )
            st.plotly_chart(fig_pm, use_container_width=True)
        else:
            st.info("Sem dados suficientes para combinar Placa × Motivo")
    else:
        st.warning("Colunas PLACA e/ou MOTIVO não encontradas")

    st.markdown("---")

    # ── 3 GRÁFICOS NARRATIVOS ────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Top Motivos</h3></div>', unsafe_allow_html=True)
        if COL_MOTIVO:
            df_m = (
                df[df[COL_MOTIVO].str.strip()!=""]
                .groupby(COL_MOTIVO)
                .agg(Valor=(VALOR_COL,"sum"), Qtd=(VALOR_COL,"count"))
                .reset_index().sort_values("Valor",ascending=True).tail(8)
            )
            if not df_m.empty:
                fig_m = px.bar(df_m, x="Valor", y=COL_MOTIVO, orientation="h",
                               color="Valor", color_continuous_scale=RED,
                               text=[fmt_brl(v) for v in df_m["Valor"]],
                               labels={COL_MOTIVO:"","Valor":"R$"})
                fig_m.update_traces(textposition="outside",textfont_size=8,cliponaxis=False)
                st.plotly_chart(plotly_dark(fig_m,height=360), use_container_width=True)
                top = df_m.iloc[-1]
                pct = top["Valor"]/total_val*100 if total_val>0 else 0
                st.caption(f"📌 **{top[COL_MOTIVO]}** representa {pct:.1f}% ({fmt_brl(top['Valor'])})")

    with c2:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>👤 Top 10 Clientes</h3></div>', unsafe_allow_html=True)
        if COL_CLIENTE:
            df_cli = (
                df[df[COL_CLIENTE].str.strip()!=""]
                .groupby(COL_CLIENTE)
                .agg(Valor=(VALOR_COL,"sum"), Qtd=(VALOR_COL,"count"))
                .reset_index().sort_values("Valor",ascending=True).tail(10)
            )
            if not df_cli.empty:
                fig_c = px.bar(df_cli, x="Valor", y=COL_CLIENTE, orientation="h",
                               color="Valor", color_continuous_scale=MIXED,
                               text=[fmt_brl(v) for v in df_cli["Valor"]],
                               labels={COL_CLIENTE:"","Valor":"R$"})
                fig_c.update_traces(textposition="outside",textfont_size=8,cliponaxis=False)
                st.plotly_chart(plotly_dark(fig_c,height=360), use_container_width=True)
                top_c = df_cli.iloc[-1]
                st.caption(f"📌 **{str(top_c[COL_CLIENTE])[:28]}** — {fmt_brl(top_c['Valor'])}")

    with c3:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🧑‍💼 Top 10 Vendedores</h3></div>', unsafe_allow_html=True)
        if COL_VENDEDOR:
            df_v = (
                df[df[COL_VENDEDOR].str.strip()!=""]
                .groupby(COL_VENDEDOR)
                .agg(Valor=(VALOR_COL,"sum"), Qtd=(VALOR_COL,"count"))
                .reset_index().sort_values("Valor",ascending=True).tail(10)
            )
            if not df_v.empty:
                fig_v = px.bar(df_v, x="Valor", y=COL_VENDEDOR, orientation="h",
                               color="Valor", color_continuous_scale=BLUE,
                               text=[fmt_brl(v) for v in df_v["Valor"]],
                               labels={COL_VENDEDOR:"","Valor":"R$"})
                fig_v.update_traces(textposition="outside",textfont_size=8,cliponaxis=False)
                st.plotly_chart(plotly_dark(fig_v,height=360), use_container_width=True)
                top_v = df_v.iloc[-1]
                st.caption(f"📌 **{str(top_v[COL_VENDEDOR])[:28]}** — {int(top_v['Qtd'])} devoluções")

    st.markdown("---")
    c4, c5 = st.columns([1,2], gap="large")

    with c4:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏙️ Por Destino</h3></div>', unsafe_allow_html=True)
        if COL_DESTINO:
            df_d = (
                df[df[COL_DESTINO].str.strip()!=""]
                .groupby(COL_DESTINO)
                .agg(Valor=(VALOR_COL,"sum"))
                .reset_index().sort_values("Valor",ascending=False).head(10)
            )
            if not df_d.empty:
                fig_d = px.pie(df_d, names=COL_DESTINO, values="Valor",
                               color_discrete_sequence=MIXED, hole=0.52)
                fig_d.update_traces(textfont_size=10,
                    marker=dict(line=dict(color="rgba(4,9,20,0.8)",width=2)),
                    pull=[0.05]+[0]*(len(df_d)-1))
                st.plotly_chart(plotly_dark(fig_d,height=320), use_container_width=True)

    with c5:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>📊 Ranking de Motivos</h3></div>', unsafe_allow_html=True)
        if COL_MOTIVO:
            df_rk = (
                df.groupby(COL_MOTIVO)
                .agg(Qtd=(VALOR_COL,"count"),Total=(VALOR_COL,"sum"))
                .reset_index().sort_values("Total",ascending=False)
            )
            df_rk["Valor Total"] = df_rk["Total"].apply(fmt_brl)
            df_rk["% Total"] = (df_rk["Total"]/total_val*100).round(1).astype(str)+"%" if total_val>0 else "0%"
            df_rk = df_rk.rename(columns={COL_MOTIVO:"Motivo"})
            st.dataframe(df_rk[["Motivo","Qtd","Valor Total","% Total"]],
                         use_container_width=True, hide_index=True, height=320)

# ══════════════════════════════════════════════════════════════
# ABA 2 — CAMPOS
# ══════════════════════════════════════════════════════════════
with tab_campos:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🗂️ Campos da Planilha — Pesquisa Detalhada</h3></div>', unsafe_allow_html=True)

    sr1, sr2, sr3, sr4 = st.columns(4, gap="medium")
    with sr1:
        s_cli = st.text_input("👤 Cliente", placeholder="Nome", key="sc_cli")
    with sr2:
        s_nf  = st.text_input("📄 Nota Fiscal", placeholder="Nº da nota", key="sc_nf")
    with sr3:
        s_ped = st.text_input("📦 Pedido / Cód. Cliente", placeholder="Código", key="sc_ped")
    with sr4:
        s_placa2 = st.text_input("🚚 Placa", placeholder="Ex: PHY6J84", key="sc_placa")

    CAMPOS = [
        (COL_DTSAIDA,    "Data Saída"),
        (COL_DTENTREGA,  "Data Entrega"),
        (COL_NF_VENDA,   "Nota Fiscal"),
        (COL_NUMCAR,     "Carregamento"),
        (COL_PLACA,      "Placa"),
        (COL_DESTINO,    "Destino"),
        (COL_MOTIVO,     "Motivo"),
        (COL_CODCLI,     "Cód. Cliente"),
        (COL_CLIENTE,    "Cliente"),
        (COL_MOTORISTA,  "Motorista"),
        (COL_VENDEDOR,   "Vendedor"),
        (COL_DEVOLUCION, "Devolucionista"),
    ]
    cols_ok = [(o,a) for o,a in CAMPOS if o is not None]
    df_campos = df[[o for o,_ in cols_ok]].copy()
    df_campos.columns = [a for _,a in cols_ok]

    if s_cli.strip() and "Cliente" in df_campos.columns:
        df_campos = df_campos[df_campos["Cliente"].str.contains(s_cli.strip(), case=False, na=False)]
    if s_nf.strip() and "Nota Fiscal" in df_campos.columns:
        df_campos = df_campos[df_campos["Nota Fiscal"].str.contains(s_nf.strip(), case=False, na=False)]
    if s_ped.strip() and "Cód. Cliente" in df_campos.columns:
        df_campos = df_campos[df_campos["Cód. Cliente"].str.contains(s_ped.strip(), case=False, na=False)]
    if s_placa2.strip() and "Placa" in df_campos.columns:
        df_campos = df_campos[df_campos["Placa"].str.contains(s_placa2.strip(), case=False, na=False)]

    st.markdown("---")
    st.caption(f"Exibindo {len(df_campos):,} registros (filtros globais + pesquisa acima)".replace(",","."))

    if len(df_campos) == 0:
        st.warning("⚠️ Nenhum registro encontrado.")
    else:
        st.dataframe(df_campos, use_container_width=True, height=560, hide_index=True)
        csv_c = df_campos.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar (.csv)", data=csv_c,
            file_name=f"campos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")

# ══════════════════════════════════════════════════════════════
# ABA 3 — DADOS COMPLETOS
# ══════════════════════════════════════════════════════════════
with tab_dados:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>📑 Detalhamento Completo</h3></div>', unsafe_allow_html=True)

    display_cols = [c for c in actual_cols if not c.startswith("_")]
    d1, d2, d3 = st.columns(3, gap="medium")

    sort_opts = [VALOR_COL] + [c for c in [COL_DTSAIDA,COL_DTENTREGA,COL_CLIENTE,COL_MOTIVO,COL_PLACA] if c]
    with d1:
        sort_col = st.selectbox("Ordenar por", sort_opts)
    with d2:
        sort_asc = st.radio("Direção", ["↑ Crescente","↓ Decrescente"], horizontal=True) == "↑ Crescente"
    with d3:
        n_rows = st.selectbox("Máximo de linhas", [50,100,250,500,1000,"Todos"])

    df_sorted = df.sort_values(sort_col, ascending=sort_asc)
    if n_rows != "Todos":
        df_sorted = df_sorted.head(int(n_rows))

    st.dataframe(df_sorted[display_cols], use_container_width=True, height=520, hide_index=True)
    st.caption(f"Exibindo {len(df_sorted):,} de {len(df):,} registros".replace(",","."))

    st.markdown("---")
    e1, e2 = st.columns(2)
    with e1:
        csv_all = df[display_cols].to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar filtrados (.csv)", data=csv_all,
            file_name=f"devolucoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)
    with e2:
        if st.button("🔄 Atualizar Dados", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    with st.expander("🔍 Diagnóstico — colunas detectadas"):
        st.write(f"**Colunas ({len(actual_cols)}):** `{actual_cols}`")
        st.write(f"Valor=`{VALOR_COL}` | Placa=`{COL_PLACA}` | Motivo=`{COL_MOTIVO}`")
        st.write(f"Cliente=`{COL_CLIENTE}` | Devolucionista=`{COL_DEVOLUCION}`")
        st.write(f"DataSaída=`{COL_DTSAIDA}` | DataEntrega=`{COL_DTENTREGA}`")
        st.write(f"Registros com valor > 0: {(df_raw[VALOR_COL]>0).sum()}")
        st.dataframe(df_raw[display_cols].head(5), use_container_width=True)
