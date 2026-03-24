import streamlit as st
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
    font-family: 'Space Grotesk', sans-serif;
    color: #e2e8f0;
}

/* ── Background com imagem desfocada ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: url('https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1920&q=80');
    background-size: cover;
    background-position: center;
    filter: blur(8px) brightness(0.18) saturate(0.6);
    z-index: -2;
    transform: scale(1.05);
}

.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(4,9,20,0.92) 0%, rgba(6,14,35,0.88) 50%, rgba(4,12,28,0.95) 100%);
    z-index: -1;
}

/* ── Hide default branding ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top nav bar ── */
.topbar {
    background: linear-gradient(90deg, rgba(10,18,40,0.95) 0%, rgba(12,22,48,0.95) 100%);
    border-bottom: 1px solid rgba(56,189,248,0.2);
    padding: 16px 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -6rem -1rem 2.5rem;
    position: sticky;
    top: 0;
    z-index: 999;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.5);
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}
.topbar-brand .icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    box-shadow: 0 0 20px rgba(14,165,233,0.4);
}
.topbar-brand h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 400 !important;
    color: #f0f9ff !important;
    letter-spacing: 0.1em;
    margin: 0 !important;
}
.topbar-brand span {
    font-size: 0.7rem;
    color: #475569;
    display: block;
    font-weight: 400;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 18px;
}
.live-badge {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.35);
    border-radius: 50px;
    padding: 6px 16px;
    font-size: 0.73rem;
    color: #4ade80;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #4ade80;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
    box-shadow: 0 0 8px #4ade80;
}
@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px #4ade80; }
    50% { opacity: 0.5; box-shadow: 0 0 3px #4ade80; }
}
.topbar-time { 
    font-family: 'DM Mono', monospace;
    font-size: 0.73rem; 
    color: #475569;
    letter-spacing: 0.05em;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.kpi-card {
    background: linear-gradient(135deg, rgba(13,31,60,0.85) 0%, rgba(15,36,68,0.85) 100%);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 18px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
    backdrop-filter: blur(10px);
}
.kpi-card:hover {
    border-color: rgba(56,189,248,0.45);
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(14,165,233,0.15);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 100px; height: 100px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56,189,248,0.08), transparent 70%);
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.4), transparent);
}
.kpi-icon { font-size: 1.5rem; margin-bottom: 12px; }
.kpi-label { 
    font-size: 0.68rem; 
    color: #64748b; 
    font-weight: 600; 
    letter-spacing: 0.08em; 
    text-transform: uppercase; 
    margin-bottom: 8px; 
}
.kpi-value { 
    font-family: 'Bebas Neue', sans-serif; 
    font-size: 1.7rem; 
    font-weight: 400; 
    color: #38bdf8; 
    line-height: 1;
    letter-spacing: 0.02em;
}
.kpi-sub { font-size: 0.68rem; color: #475569; margin-top: 8px; }

/* ── Section headers ── */
.sec-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}
.sec-header .bar { 
    width: 3px; height: 24px; 
    background: linear-gradient(180deg, #38bdf8, #2563eb); 
    border-radius: 2px; 
    box-shadow: 0 0 10px rgba(56,189,248,0.5);
}
.sec-header h3 { 
    font-family: 'Bebas Neue', sans-serif; 
    font-size: 1.1rem; 
    font-weight: 400; 
    color: #e2e8f0; 
    margin: 0;
    letter-spacing: 0.08em;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10,18,40,0.8) !important;
    border-radius: 16px !important;
    padding: 6px !important;
    gap: 4px !important;
    border: 1px solid rgba(56,189,248,0.15) !important;
    margin-bottom: 8px;
    backdrop-filter: blur(10px);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 12px !important;
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 24px !important;
    transition: all 0.25s !important;
    border: none !important;
    letter-spacing: 0.03em;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0c4a6e, #1e3a8a) !important;
    color: #e0f2fe !important;
    box-shadow: 0 2px 20px rgba(14,165,233,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 28px !important; }

/* ── Charts card wrapper ── */
.chart-card {
    background: rgba(13,31,60,0.7);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 22px;
    backdrop-filter: blur(10px);
}

/* ── Search cards ── */
.result-card {
    background: linear-gradient(135deg, rgba(13,31,60,0.85), rgba(15,36,68,0.85));
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 16px;
    padding: 18px 24px;
    margin-bottom: 12px;
    transition: border-color 0.2s, transform 0.2s;
    backdrop-filter: blur(8px);
}
.result-card:hover {
    border-color: rgba(56,189,248,0.4);
    transform: translateX(4px);
    box-shadow: 0 4px 20px rgba(14,165,233,0.1);
}
.rc-client { font-size: 1rem; font-weight: 700; color: #38bdf8; margin-bottom: 8px; }
.rc-row { font-size: 0.8rem; color: #94a3b8; margin-top: 4px; display: flex; flex-wrap: wrap; gap: 16px; }
.rc-row span { display: flex; align-items: center; gap: 5px; }
.rc-val { 
    font-family: 'Bebas Neue', sans-serif; 
    font-size: 1.4rem; 
    font-weight: 400; 
    color: #4ade80;
    letter-spacing: 0.05em;
}
.rc-badge {
    display: inline-block;
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.7rem;
    font-weight: 600;
}

/* ── Inputs ── */
.stTextInput input {
    background: rgba(10,18,40,0.8) !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput input:focus { 
    border-color: rgba(56,189,248,0.5) !important; 
    box-shadow: 0 0 0 3px rgba(56,189,248,0.1) !important; 
}
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(10,18,40,0.8) !important;
    border-color: rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stMultiSelect div[data-baseweb="select"] > div {
    background: rgba(10,18,40,0.8) !important;
    border-color: rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: rgba(14,165,233,0.2) !important;
    color: #38bdf8 !important;
    border-radius: 6px !important;
}
label, .stSelectbox label, .stMultiSelect label, .stTextInput label {
    color: #94a3b8 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0c4a6e, #1e3a8a) !important;
    color: #e0f2fe !important;
    border: 1px solid rgba(56,189,248,0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 24px !important;
    transition: all 0.25s !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.04em;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e3a8a, #1d4ed8) !important;
    border-color: rgba(56,189,248,0.6) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(14,165,233,0.25) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(34,197,94,0.1) !important;
    color: #4ade80 !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid rgba(56,189,248,0.12) !important;
}

/* ── Radio ── */
.stRadio label { color: #94a3b8 !important; font-size: 0.85rem !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #94a3b8 !important; }

/* ── Divider ── */
hr { border-color: rgba(56,189,248,0.08) !important; margin: 24px 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(6,13,31,0.5); }
::-webkit-scrollbar-thumb { background: #1e3a8a; border-radius: 3px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(10,18,40,0.95) !important;
    border-right: 1px solid rgba(56,189,248,0.1) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(13,31,60,0.7) !important;
    border: 1px solid rgba(56,189,248,0.12) !important;
    border-radius: 14px !important;
    padding: 16px !important;
    backdrop-filter: blur(8px);
}
[data-testid="stMetricValue"] { 
    font-family: 'Bebas Neue', sans-serif !important; 
    color: #38bdf8 !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.75rem !important; }

/* ── Caption ── */
.stCaption { color: #475569 !important; font-size: 0.73rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def plotly_layout(fig, margin_b=50):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#94a3b8", family="Space Grotesk"),
        coloraxis_showscale=False,
        margin=dict(t=20, b=margin_b, l=10, r=10),
        xaxis=dict(
            tickfont=dict(color="#64748b", size=10),
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.06)",
        ),
        yaxis=dict(
            tickfont=dict(color="#64748b", size=10),
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.06)",
        ),
        legend=dict(
            bgcolor="rgba(10,18,40,0.9)",
            bordercolor="rgba(56,189,248,0.15)",
            borderwidth=1,
            font=dict(color="#94a3b8", size=11),
        ),
    )
    return fig

BLUE  = ["#0c4a6e", "#0369a1", "#0ea5e9", "#7dd3fc"]
RED   = ["#7f1d1d", "#b91c1c", "#ef4444", "#fca5a5"]
GREEN = ["#14532d", "#15803d", "#22c55e", "#86efac"]
MIXED = ["#0ea5e9", "#22c55e", "#f59e0b", "#ef4444", "#a855f7", "#ec4899", "#14b8a6", "#f97316"]

# ── Google Sheets URL ─────────────────────────────────────────────────────────
SHEET_ID = "1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI"
GSHEETS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}"

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_data(url: str) -> pd.DataFrame:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, timeout=30, headers=headers)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        st.stop()

with st.spinner("⏳ Carregando dados da planilha..."):
    df_raw = load_data(GSHEETS_URL)

# ── Normalize columns — mantém nomes originais da planilha ───────────────────
df_raw.columns = [str(c).strip().upper().replace(" ", "_") for c in df_raw.columns]
actual_cols = list(df_raw.columns)

# Mapeia colunas financeiras para padronizar apenas o que é necessário
# Preservamos os nomes originais e apenas normalizamos o valor e a data

# Detecta coluna de valor (VLT ou similares)
VALOR_COL = None
for c in ["VLT", "VALOR_LIQUIDO", "VALOR", "TOTAL", "VL_TOTAL", "VLF", "VL_DEVOLUCAO"]:
    if c in df_raw.columns:
        VALOR_COL = c
        break
if VALOR_COL is None:
    # Tenta encontrar qualquer coluna numérica com 'valor' ou 'vl'
    for c in df_raw.columns:
        if any(k in c for k in ["VALOR", "VL", "VLT"]):
            VALOR_COL = c
            break
if VALOR_COL is None:
    df_raw["VLT"] = 0.0
    VALOR_COL = "VLT"

# Detecta coluna de data
DATA_COL = None
for c in ["DTSAIDA", "DATA_DEVOLUCAO", "DATA", "DT_DEVOLUCAO", "DATA_DEV", "DATA_EMISSAO", "DTENTREGA"]:
    if c in df_raw.columns:
        DATA_COL = c
        break

# Parse numeric value
def parse_brl(s):
    s = str(s).replace("R$", "").strip()
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    return pd.to_numeric(s, errors="coerce")

df_raw[VALOR_COL] = df_raw[VALOR_COL].apply(parse_brl).fillna(0)

# Preenche NaN com string vazia para colunas de texto
for col in df_raw.columns:
    if col != VALOR_COL:
        df_raw[col] = df_raw[col].fillna("").astype(str).str.strip()

# Parse date
if DATA_COL:
    df_raw["_DATA_DT"] = pd.to_datetime(df_raw[DATA_COL], dayfirst=True, errors="coerce")
else:
    df_raw["_DATA_DT"] = pd.NaT

# Detecta outras colunas específicas usadas nas análises
def get_col(names):
    for n in names:
        if n in df_raw.columns:
            return n
    return None

COL_PLACA      = get_col(["PLACA", "PLACA_VEICULO", "VEICULO"])
COL_MOTIVO     = get_col(["MOTIVO", "MOTIVO_DEVOLUCAO", "MOTIVO_DEV"])
COL_CLIENTE    = get_col(["CLIENTE", "NOMERCA", "NOME_CLIENTE", "RAZAO_SOCIAL"])
COL_VENDEDOR   = get_col(["NOMERCA", "VENDEDOR", "NOMEFUNC_VEND", "REPR_VENDAS"])
COL_DEVOLUCION = get_col(["NOMEFUNC", "DEVOLUCIONISTA", "FUNCIONARIO"])
COL_MOTORISTA  = get_col(["MOTORISTA", "ENTREGADOR"])
COL_SUPERVISOR = get_col(["SUPERVISOR", "AM", "GERENTE"])
COL_DESTINO    = get_col(["DESTINO", "CIDADE", "MUNICIPIO", "PRACA", "CODPRA"])
COL_NF_VENDA   = get_col(["NOTA_VENDA", "NF_VENDA", "NF_SAIDA", "NOTA_SAIDA"])
COL_NUMCAR     = get_col(["NUMCAR", "NUM_CARREGAMENTO", "CARREGAMENTO", "NR_CARREGAMENTO"])
COL_CODCLI     = get_col(["CODCLI", "COD_CLI", "CLI", "NUM_PEDIDO", "PEDIDO"])
COL_DTSAIDA    = get_col(["DTSAIDA", "DATA_DEVOLUCAO", "DATA", "DT_DEVOLUCAO"])
COL_DTENTREGA  = get_col(["DTENTREGA", "DATA_ENTREGA", "DT_ENTREGA"])

# ── Computed KPIs ─────────────────────────────────────────────────────────────
df = df_raw.copy()
total_val      = df[VALOR_COL].sum()
total_notas    = len(df)
total_clientes = df[COL_CLIENTE].nunique() if COL_CLIENTE else 0
ticket_medio   = total_val / total_notas if total_notas > 0 else 0
total_veiculos = df[COL_PLACA].nunique() if COL_PLACA else 0

# ── TOPBAR ────────────────────────────────────────────────────────────────────
now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand">
        <div class="icon">📦</div>
        <div>
            <h1>DEVOLUÇÕES</h1>
            <span>Sistema de Análise e Controle</span>
        </div>
    </div>
    <div class="topbar-right">
        <div class="live-badge"><span class="live-dot"></span>Ao Vivo</div>
        <div class="topbar-time">🕐 {now_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab_dash, tab_campos, tab_dados = st.tabs([
    "📊  Dashboard",
    "🗂️  Campos",
    "📑  Dados Completos",
])

# ════════════════════════════════════════════════════════
# ABA 1 — DASHBOARD
# ════════════════════════════════════════════════════════
with tab_dash:
    # KPI Row
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Valor Total</div>
            <div class="kpi-value">{fmt_brl(total_val)}</div>
            <div class="kpi-sub">Total devolvido</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">📄</div>
            <div class="kpi-label">Devoluções</div>
            <div class="kpi-value">{str(total_notas).replace(",", ".")}</div>
            <div class="kpi-sub">Registros totais</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">👤</div>
            <div class="kpi-label">Clientes</div>
            <div class="kpi-value">{str(total_clientes).replace(",", ".")}</div>
            <div class="kpi-sub">Clientes únicos</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Ticket Médio</div>
            <div class="kpi-value">{fmt_brl(ticket_medio)}</div>
            <div class="kpi-sub">Por devolução</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">🚚</div>
            <div class="kpi-label">Veículos</div>
            <div class="kpi-value">{str(total_veiculos).replace(",", ".")}</div>
            <div class="kpi-sub">Placas únicas</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── GRÁFICO PRINCIPAL: Devoluções por Placa ────────────────────────────
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🚚 Devoluções por Placa — Ranking Geral</h3></div>', unsafe_allow_html=True)

    if COL_PLACA:
        df_placa_all = (
            df[df[COL_PLACA].str.strip() != ""]
            .groupby(COL_PLACA, as_index=False)[VALOR_COL]
            .agg(Valor=VALOR_COL, Qtd=(VALOR_COL, "count"))
            .rename(columns={VALOR_COL: "Valor", "Qtd": "Qtd"})
        )
        # Fix: use agg properly
df_placa_all = (
    df[df[COL_PLACA].str.strip() != ""]
    .groupby(COL_PLACA, as_index=False)[VALOR_COL]
    .agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
    .rename(columns={VALOR_COL: "Valor", "Qtd": "Qtd"})
)
        )

        if not df_placa_all.empty:
            # Colorir as top 5 mais críticas diferente
            colors = ["#ef4444" if i >= len(df_placa_all) - 5 else "#0ea5e9"
                      for i in range(len(df_placa_all))]

            fig_placa = go.Figure(go.Bar(
                x=df_placa_all["Valor"],
                y=df_placa_all[COL_PLACA],
                orientation="h",
                marker=dict(
                    color=colors,
                    line=dict(color="rgba(255,255,255,0.05)", width=0.5),
                ),
                text=[fmt_brl(v) for v in df_placa_all["Valor"]],
                textposition="outside",
                textfont=dict(size=9, color="#94a3b8"),
                hovertemplate="<b>%{y}</b><br>Valor: %{text}<br>Qtd: " +
                              df_placa_all["Qtd"].astype(str) + "<extra></extra>",
            ))
            fig_placa.update_layout(height=max(400, len(df_placa_all) * 22))
            st.plotly_chart(plotly_layout(fig_placa, margin_b=30), use_container_width=True)
        else:
            st.info("Sem dados de placa")
    else:
        st.warning("Coluna PLACA não encontrada na planilha")

    st.markdown("---")

    # ── 3 GRÁFICOS NARRATIVOS ─────────────────────────────────────────────
    c1, c2, c3 = st.columns(3, gap="large")

    # Gráfico 1: Devoluções por Motivo
    with c1:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Top Motivos de Devolução</h3></div>', unsafe_allow_html=True)
        if COL_MOTIVO:
            df_m = (
                df[df[COL_MOTIVO].str.strip() != ""]
                .groupby(COL_MOTIVO)
                .agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                .reset_index()
                .sort_values("Valor", ascending=True)
                .tail(8)
            )
            if not df_m.empty:
                fig_m = px.bar(
                    df_m, x="Valor", y=COL_MOTIVO, orientation="h",
                    color="Valor", color_continuous_scale=RED,
                    text=[fmt_brl(v) for v in df_m["Valor"]],
                    labels={COL_MOTIVO: "", "Valor": "R$"},
                )
                fig_m.update_traces(textposition="outside", textfont_size=8, cliponaxis=False)
                fig_m.update_layout(height=360)
                st.plotly_chart(plotly_layout(fig_m), use_container_width=True)

                # Narrativa
                top_motivo = df_m.iloc[-1][COL_MOTIVO]
                top_val = df_m.iloc[-1]["Valor"]
                pct = (top_val / total_val * 100) if total_val > 0 else 0
                st.caption(f"📌 *{top_motivo}* representa {pct:.1f}% do total devolvido ({fmt_brl(top_val)})")
            else:
                st.info("Sem dados de motivo")
        else:
            st.warning("Coluna MOTIVO não detectada")

    # Gráfico 2: Top Clientes
    with c2:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>👤 Top 10 Clientes — Maior Devolução</h3></div>', unsafe_allow_html=True)
        if COL_CLIENTE:
            df_cli = (
                df[df[COL_CLIENTE].str.strip() != ""]
                .groupby(COL_CLIENTE)
                .agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                .reset_index()
                .sort_values("Valor", ascending=True)
                .tail(10)
            )
            if not df_cli.empty:
                fig_cli = px.bar(
                    df_cli, x="Valor", y=COL_CLIENTE, orientation="h",
                    color="Valor", color_continuous_scale=MIXED,
                    text=[fmt_brl(v) for v in df_cli["Valor"]],
                    labels={COL_CLIENTE: "", "Valor": "R$"},
                )
                fig_cli.update_traces(textposition="outside", textfont_size=8, cliponaxis=False)
                fig_cli.update_layout(height=360)
                st.plotly_chart(plotly_layout(fig_cli), use_container_width=True)

                top_cli = df_cli.iloc[-1][COL_CLIENTE]
                top_val_cli = df_cli.iloc[-1]["Valor"]
                st.caption(f"📌 *{top_cli[:30]}* é o cliente com maior volume de devolução: {fmt_brl(top_val_cli)}")
            else:
                st.info("Sem dados de clientes")
        else:
            st.warning("Coluna CLIENTE não detectada")

    # Gráfico 3: Top Vendedores (NOMERCA)
    with c3:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🧑‍💼 Top 10 Vendedores por Devolução</h3></div>', unsafe_allow_html=True)
        if COL_VENDEDOR:
            df_vend = (
                df[df[COL_VENDEDOR].str.strip() != ""]
                .groupby(COL_VENDEDOR)
                .agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                .reset_index()
                .sort_values("Valor", ascending=True)
                .tail(10)
            )
            if not df_vend.empty:
                fig_vend = px.bar(
                    df_vend, x="Valor", y=COL_VENDEDOR, orientation="h",
                    color="Valor", color_continuous_scale=BLUE,
                    text=[fmt_brl(v) for v in df_vend["Valor"]],
                    labels={COL_VENDEDOR: "", "Valor": "R$"},
                )
                fig_vend.update_traces(textposition="outside", textfont_size=8, cliponaxis=False)
                fig_vend.update_layout(height=360)
                st.plotly_chart(plotly_layout(fig_vend), use_container_width=True)

                top_vend = df_vend.iloc[-1][COL_VENDEDOR]
                top_qtd_vend = int(df_vend.iloc[-1]["Qtd"])
                st.caption(f"📌 *{top_vend[:30]}* acumula {top_qtd_vend} devoluções no período")
            else:
                st.info("Sem dados de vendedores")
        else:
            st.warning("Coluna NOMERCA/VENDEDOR não detectada")

    # ── Linha divisória + Motivos tabela ──────────────────────────────────
    st.markdown("---")
    c4, c5 = st.columns([1, 2], gap="large")

    with c4:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏙️ Devoluções por Destino</h3></div>', unsafe_allow_html=True)
        if COL_DESTINO:
            df_dest = (
                df[df[COL_DESTINO].str.strip() != ""]
                .groupby(COL_DESTINO)
                .agg(Valor=(VALOR_COL, "sum"))
                .reset_index()
                .sort_values("Valor", ascending=False)
                .head(10)
            )
            if not df_dest.empty:
                fig_dest = px.pie(df_dest, names=COL_DESTINO, values="Valor",
                                  color_discrete_sequence=MIXED, hole=0.5)
                fig_dest.update_traces(
                    textfont_size=10,
                    marker=dict(line=dict(color="rgba(6,13,31,0.8)", width=2)),
                    pull=[0.04] + [0] * (len(df_dest) - 1),
                )
                fig_dest.update_layout(height=320)
                st.plotly_chart(plotly_layout(fig_dest), use_container_width=True)
            else:
                st.info("Sem dados de destino")
        else:
            st.warning("Coluna DESTINO não detectada")

    with c5:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>📊 Ranking de Motivos — Tabela Detalhada</h3></div>', unsafe_allow_html=True)
        if COL_MOTIVO:
            df_rank = (
                df.groupby(COL_MOTIVO)
                .agg(Qtd=(VALOR_COL, "count"), Total=(VALOR_COL, "sum"))
                .reset_index()
                .sort_values("Total", ascending=False)
            )
            df_rank["Valor Total"] = df_rank["Total"].apply(fmt_brl)
            df_rank["% do Total"] = (df_rank["Total"] / total_val * 100).round(1).astype(str) + "%" if total_val > 0 else "0%"
            df_rank = df_rank.rename(columns={COL_MOTIVO: "Motivo"})
            st.dataframe(
                df_rank[["Motivo", "Qtd", "Valor Total", "% do Total"]],
                use_container_width=True, hide_index=True, height=320,
            )
        else:
            st.warning("Coluna MOTIVO não detectada")

# ════════════════════════════════════════════════════════
# ABA 2 — CAMPOS (tabela detalhada + pesquisa)
# ════════════════════════════════════════════════════════
with tab_campos:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🗂️ Campos da Planilha — Visualização e Pesquisa</h3></div>', unsafe_allow_html=True)

    # Barra de pesquisa
    st.markdown("#### 🔎 Pesquisar")
    sr1, sr2, sr3, sr4 = st.columns(4, gap="medium")
    with sr1:
        s_cliente_c = st.text_input("👤 Cliente", placeholder="Nome do cliente", key="sc_cliente")
    with sr2:
        s_nota_c = st.text_input("📄 Nota Fiscal", placeholder="Nº da nota de venda", key="sc_nota")
    with sr3:
        s_pedido_c = st.text_input("📦 Pedido / Cód. Cliente", placeholder="Código ou pedido", key="sc_pedido")
    with sr4:
        s_placa_c = st.text_input("🚚 Placa", placeholder="Placa do veículo", key="sc_placa")

    # Monta lista de colunas para exibir — usa as colunas reais da planilha
    CAMPOS_DESEJADOS = [
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

    # Filtra apenas colunas que existem no df
    cols_existentes = [(orig, alias) for orig, alias in CAMPOS_DESEJADOS if orig is not None]

    df_campos = df[[orig for orig, _ in cols_existentes]].copy()
    df_campos.columns = [alias for _, alias in cols_existentes]

    # Aplica pesquisa
    filtros_ativos = []

    if s_cliente_c.strip() and "Cliente" in df_campos.columns:
        df_campos = df_campos[df_campos["Cliente"].str.contains(s_cliente_c.strip(), case=False, na=False)]
        filtros_ativos.append(f"Cliente: {s_cliente_c}")

    if s_nota_c.strip() and "Nota Fiscal" in df_campos.columns:
        df_campos = df_campos[df_campos["Nota Fiscal"].str.contains(s_nota_c.strip(), case=False, na=False)]
        filtros_ativos.append(f"Nota: {s_nota_c}")

    if s_pedido_c.strip() and "Cód. Cliente" in df_campos.columns:
        df_campos = df_campos[df_campos["Cód. Cliente"].str.contains(s_pedido_c.strip(), case=False, na=False)]
        filtros_ativos.append(f"Pedido: {s_pedido_c}")

    if s_placa_c.strip() and "Placa" in df_campos.columns:
        df_campos = df_campos[df_campos["Placa"].str.contains(s_placa_c.strip(), case=False, na=False)]
        filtros_ativos.append(f"Placa: {s_placa_c}")

    st.markdown("---")

    if filtros_ativos:
        st.info(f"🔍 *{len(df_campos)} resultado(s)* | Filtros ativos: {' · '.join(filtros_ativos)}")
    else:
        st.caption(f"Exibindo todos os {len(df_campos):,} registros. Use os campos acima para filtrar.")

    if len(df_campos) == 0:
        st.warning("⚠️ Nenhum registro encontrado.")
    else:
        st.dataframe(
            df_campos,
            use_container_width=True,
            height=560,
            hide_index=True,
        )

    if len(df_campos) > 0:
        st.markdown("---")
        csv_campos = df_campos.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button(
            "⬇️ Exportar tabela (.csv)",
            data=csv_campos,
            file_name=f"campos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

# ════════════════════════════════════════════════════════
# ABA 3 — DADOS COMPLETOS
# ════════════════════════════════════════════════════════
with tab_dados:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>📑 Detalhamento Completo das Devoluções</h3></div>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3, gap="medium")
    with d1:
        # Usa colunas disponíveis para ordenação
        sort_options = [VALOR_COL]
        if COL_DTSAIDA: sort_options.append(COL_DTSAIDA)
        if COL_CLIENTE: sort_options.append(COL_CLIENTE)
        if COL_MOTIVO: sort_options.append(COL_MOTIVO)
        if COL_PLACA: sort_options.append(COL_PLACA)

        sort_labels = {
            VALOR_COL: "💰 Valor",
            COL_DTSAIDA: "📅 Data Saída",
            COL_CLIENTE: "👤 Cliente",
            COL_MOTIVO: "❗ Motivo",
            COL_PLACA: "🚚 Placa",
        }
        sort_col = st.selectbox("Ordenar por", sort_options,
                                format_func=lambda x: sort_labels.get(x, x))
    with d2:
        sort_asc = st.radio("Direção", ["↑ Crescente", "↓ Decrescente"], horizontal=True) == "↑ Crescente"
    with d3:
        n_rows = st.selectbox("Máximo de linhas", [50, 100, 250, 500, 1000, "Todos"])

    df_sorted = df.sort_values(sort_col, ascending=sort_asc)
    if n_rows != "Todos":
        df_sorted = df_sorted.head(int(n_rows))

    # Exibe todas as colunas originais da planilha (exceto colunas internas)
    display_cols = [c for c in actual_cols if not c.startswith("_")]
    df_disp = df_sorted[display_cols].copy()

    st.dataframe(df_disp, use_container_width=True, height=520, hide_index=True)
    st.caption(f"Exibindo {len(df_disp):,} de {len(df):,} registros · Total bruto: {len(df_raw):,}")

    st.markdown("---")
    e1, e2 = st.columns(2, gap="medium")
    with e1:
        csv_all = df[display_cols].to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar todos (.csv)", data=csv_all,
            file_name=f"devolucoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)
    with e2:
        if st.button("🔄 Atualizar Dados", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    with st.expander("🔍 Diagnóstico: colunas detectadas na planilha"):
        st.write(f"*Colunas originais ({len(actual_cols)}):* {actual_cols}")
        st.write(f"*Coluna de valor detectada:* {VALOR_COL}")
        st.write(f"*Coluna de data detectada:* {DATA_COL}")
        st.write(f"*Registros com Valor > 0:* {(df_raw[VALOR_COL] > 0).sum()}")
        st.write(f"*Registros com data válida:* {df_raw['_DATA_DT'].notna().sum()}")
        st.markdown("*Amostra (5 linhas originais):*")
        st.dataframe(df_raw[actual_cols].head(5), use_container_width=True)
