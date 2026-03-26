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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #060d1f !important;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

/* ── Hide default branding ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top nav bar ── */
.topbar {
    background: linear-gradient(90deg, #0a1628 0%, #0d1f3c 100%);
    border-bottom: 1px solid rgba(56,189,248,0.15);
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -6rem -1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 999;
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.topbar-brand .icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #0ea5e9, #3b82f6);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.topbar-brand h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    color: #f0f9ff !important;
    letter-spacing: -0.01em;
    margin: 0 !important;
}
.topbar-brand span {
    font-size: 0.72rem;
    color: #64748b;
    display: block;
    font-weight: 400;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 16px;
}
.live-badge {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 50px;
    padding: 5px 14px;
    font-size: 0.75rem;
    color: #4ade80;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #4ade80;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.topbar-time { font-size: 0.75rem; color: #475569; }

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}
.kpi-card {
    background: linear-gradient(135deg, #0d1f3c 0%, #0f2444 100%);
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, transform 0.25s;
}
.kpi-card:hover {
    border-color: rgba(56,189,248,0.35);
    transform: translateY(-3px);
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56,189,248,0.08), transparent 70%);
}
.kpi-icon { font-size: 1.4rem; margin-bottom: 10px; }
.kpi-label { font-size: 0.72rem; color: #64748b; font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 6px; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800; color: #38bdf8; line-height: 1; }
.kpi-sub { font-size: 0.7rem; color: #475569; margin-top: 6px; }

/* ── Section headers ── */
.sec-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}
.sec-header .bar { width: 4px; height: 22px; background: linear-gradient(180deg, #38bdf8, #3b82f6); border-radius: 2px; }
.sec-header h3 { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; color: #e2e8f0; margin: 0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0a1628 !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1px solid rgba(56,189,248,0.12) !important;
    margin-bottom: 8px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 22px !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0c4a6e, #1e40af) !important;
    color: #e0f2fe !important;
    box-shadow: 0 2px 16px rgba(14,165,233,0.25) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }

/* ── Charts container ── */
.chart-card {
    background: linear-gradient(135deg, #0d1f3c, #0f2444);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

/* ── Filters panel ── */
.filter-panel {
    background: linear-gradient(135deg, #0a1628, #0d1f3c);
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
}
.filter-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: #e0f2fe;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Search cards ── */
.result-card {
    background: linear-gradient(135deg, #0d1f3c, #0f2444);
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    transition: border-color 0.2s, transform 0.2s;
}
.result-card:hover {
    border-color: rgba(56,189,248,0.4);
    transform: translateX(4px);
}
.rc-client { font-size: 1rem; font-weight: 700; color: #38bdf8; margin-bottom: 8px; }
.rc-row { font-size: 0.8rem; color: #94a3b8; margin-top: 4px; display: flex; flex-wrap: wrap; gap: 16px; }
.rc-row span { display: flex; align-items: center; gap: 5px; }
.rc-val { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 800; color: #4ade80; }
.rc-badge {
    display: inline-block;
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.72rem;
    font-weight: 600;
}

/* ── Inputs ── */
.stTextInput input {
    background: #0a1628 !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}
.stTextInput input:focus { border-color: rgba(56,189,248,0.5) !important; box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important; }
.stSelectbox div[data-baseweb="select"] > div {
    background: #0a1628 !important;
    border-color: rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stMultiSelect div[data-baseweb="select"] > div {
    background: #0a1628 !important;
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
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0c4a6e, #1e40af) !important;
    color: #e0f2fe !important;
    border: 1px solid rgba(56,189,248,0.25) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e40af, #1d4ed8) !important;
    border-color: rgba(56,189,248,0.5) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.2) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(34,197,94,0.12) !important;
    color: #4ade80 !important;
    border: 1px solid rgba(34,197,94,0.25) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(56,189,248,0.12) !important;
}

/* ── Radio ── */
.stRadio label { color: #94a3b8 !important; font-size: 0.85rem !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #94a3b8 !important; }

/* ── Divider ── */
hr { border-color: rgba(56,189,248,0.08) !important; margin: 20px 0 !important; }

/* ── Info ── */
.stAlert { border-radius: 10px !important; }

/* ── Caption ── */
.stCaption { color: #475569 !important; font-size: 0.75rem !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #0a1628 !important;
    border-radius: 10px !important;
    color: #38bdf8 !important;
    font-weight: 600 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #060d1f; }
::-webkit-scrollbar-thumb { background: #1e40af; border-radius: 3px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0a1628 !important;
    border-right: 1px solid rgba(56,189,248,0.1) !important;
}
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
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
        font=dict(color="#94a3b8", family="Inter"),
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
            bgcolor="rgba(10,22,40,0.9)",
            bordercolor="rgba(56,189,248,0.15)",
            borderwidth=1,
            font=dict(color="#94a3b8", size=11),
        ),
    )
    return fig

BLUE  = ["#0c4a6e", "#0369a1", "#0ea5e9", "#7dd3fc"]
RED   = ["#7f1d1d", "#b91c1c", "#ef4444", "#fca5a5"]
GREEN = ["#14532d", "#15803d", "#22c55e", "#86efac"]
MIXED = ["#0ea5e9", "#22c55e", "#f59e0b", "#ef4444", "#a855f7", "#ec4899"]

# ── Google Sheets URL ─────────────────────────────────────────────────────────
SHEET_ID = "1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI"
# Try to get the first visible sheet as CSV
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

# ── Normalize columns ─────────────────────────────────────────────────────────
df_raw.columns = [str(c).strip().upper().replace(" ", "_") for c in df_raw.columns]

# Show actual columns for debugging (will be used below)
actual_cols = list(df_raw.columns)

# Flexible column mapping — covers both the screenshot columns and common aliases
col_aliases = {
    # Financial value columns - map VLT (valor total devolução) or similar
    "VALOR_LIQUIDO": [
        "VLT", "VALOR_LIQUIDO", "VALOR", "TOTAL", "VL_TOTAL",
        "VALOR_LIQ", "VLF", "VL_DEVOLUCAO", "VALOR_DEVOLUCAO",
        "VALOR_VENDA", "VLVENDA", "VL_VENDA",
    ],
    "DATA_DEVOLUCAO": [
        "DATA_DEVOLUCAO", "DATA", "DT_DEVOLUCAO", "DATA_DEV",
        "DATA_EMISSAO", "EMISSAO", "DT_EMISSAO",
    ],
    "NOME_CLIENTE": [
        "NOMERCA", "NOME_CLIENTE", "CLIENTE", "NOME_CLIENTE",
        "RAZAO_SOCIAL", "NOME", "NOMERC",
    ],
    "PLACA": [
        "PLACA", "PLACA_VEICULO", "VEICULO", "CODPRA", "PRACA",
    ],
    "MOTIVO_DEVOLUCAO": [
        "MOTIVO_DEVOLUCAO", "MOTIVO", "MOTIVO_DEV", "CONF_MATRICULA",
        "TIPO_DEVOLUCAO", "TIPO_DEV", "DESCRICAO",
    ],
    "VENDEDOR": [
        "NOMEFUNC", "VENDEDOR", "NOME_VENDEDOR", "FUNCIONARIO",
        "REPR_VENDAS", "NOMEFUN",
    ],
    "SUPERVISOR": [
        "SUPERVISOR", "CODSUPERVISOR", "NOME_SUPERVISOR",
        "GERENTE", "AM",
    ],
    "FILIAL": [
        "FILIAL", "UNIDADE", "CD", "CENTRO_DISTRIBUICAO",
        "NOMREG", "REGIAO", "REGIONAL",
    ],
    "SEGMENTO": [
        "SEGMENTO", "SEGM", "CANAL", "TIPO_CLIENTE",
    ],
    "CIDADE": [
        "CIDADE", "MUNICIPIO", "MUNICÍPIO", "PRACA",
    ],
    "NOTA_FISCAL": [
        "NOTA_FISCAL", "NF", "NF_DEVOLUCAO", "NOTA_FISCAL",
        "NUMERO", "NUM", "NR_NF",
    ],
    "NUM_DEVOLUCAO": [
        "NUM_DEVOLUCAO", "NUMERO_DEVOLUCAO", "NR_DEVOLUCAO",
        "N_DEVOLUCAO", "DEVOLUCAO", "COD",
    ],
    "NUM_PEDIDO": [
        "NUM_PEDIDO", "PEDIDO", "NR_PEDIDO", "N_PEDIDO",
        "COD_PEDIDO", "CLI",
    ],
    "NUM_CARREGAMENTO": [
        "NUM_CARREGAMENTO", "CARREGAMENTO", "NR_CARREGAMENTO",
        "N_CARREGAMENTO",
    ],
    "NF_VENDA": [
        "NF_VENDA", "NOTA_VENDA", "NF_ENTRADA", "NF_SAIDA",
        "NOTA_SAIDA",
    ],
}

# Build rename map
COL_MAP = {}
existing = set(df_raw.columns)
for std_col, aliases in col_aliases.items():
    for alias in aliases:
        if alias in existing and alias not in COL_MAP:
            COL_MAP[alias] = std_col
            break

df_raw = df_raw.rename(columns=COL_MAP)

# Ensure all standard columns exist
for col in col_aliases.keys():
    if col not in df_raw.columns:
        df_raw[col] = "N/D"
    else:
        df_raw[col] = df_raw[col].fillna("N/D").astype(str).str.strip()

# Parse numeric value
def parse_brl(s):
    s = str(s).replace("R$", "").strip()
    # If has comma as decimal and dot as thousands: 1.234,56 → 1234.56
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    return pd.to_numeric(s, errors="coerce")

df_raw["VALOR_LIQUIDO"] = df_raw["VALOR_LIQUIDO"].apply(parse_brl).fillna(0)

# Parse date
df_raw["DATA_DT"] = pd.to_datetime(df_raw["DATA_DEVOLUCAO"], dayfirst=True, errors="coerce")

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
tab_filtros, tab_dash, tab_pesquisa, tab_dados, tab_config = st.tabs([
    "⚙️  Filtros",
    "📊  Dashboard",
    "🔎  Pesquisa",
    "📑  Dados Completos",
    "🛠️  Config",
])

# ════════════════════════════════════════════════════════
# ABA 1 — FILTROS (aplicados globalmente)
# ════════════════════════════════════════════════════════
with tab_filtros:
    st.markdown('<div class="filter-title">⚙️ Filtros Globais — Aplicados em todas as abas</div>', unsafe_allow_html=True)
    st.info("💡 Configure os filtros abaixo. Eles serão aplicados ao Dashboard, Pesquisa e Dados Completos.")
    st.markdown("")

    col_f1, col_f2, col_f3 = st.columns(3, gap="large")

    with col_f1:
        filiais = sorted([x for x in df_raw["FILIAL"].unique() if x not in ("N/D", "nan", "")])
        if filiais:
            sel_filial = st.multiselect("🏢 Filial / Regional", filiais, default=filiais, key="f_filial")
        else:
            sel_filial = []
            st.caption("Coluna Filial não detectada")

        supervisores = sorted([x for x in df_raw["SUPERVISOR"].unique() if x not in ("N/D", "nan", "")])
        if supervisores:
            sel_supervisor = st.multiselect("👔 Supervisor / AM", supervisores, default=supervisores, key="f_sup")
        else:
            sel_supervisor = []

    with col_f2:
        segmentos = sorted([x for x in df_raw["SEGMENTO"].unique() if x not in ("N/D", "nan", "")])
        if segmentos:
            sel_segmento = st.multiselect("🏷️ Segmento / Canal", segmentos, default=segmentos, key="f_seg")
        else:
            sel_segmento = []

        motivos = sorted([x for x in df_raw["MOTIVO_DEVOLUCAO"].unique() if x not in ("N/D", "nan", "")])
        if motivos:
            sel_motivo = st.multiselect("❗ Motivo de Devolução", motivos, default=motivos, key="f_mot")
        else:
            sel_motivo = []

    with col_f3:
        st.markdown("**📅 Período**")
        datas_validas = df_raw["DATA_DT"].dropna()
        if len(datas_validas) > 0:
            dt_min = datas_validas.min().date()
            dt_max = datas_validas.max().date()
            dt_ini = st.date_input("De", value=dt_min, min_value=dt_min, max_value=dt_max, key="f_dtini")
            dt_fim = st.date_input("Até", value=dt_max, min_value=dt_min, max_value=dt_max, key="f_dtfim")
            filtrar_data = True
        else:
            filtrar_data = False
            st.caption("Sem datas válidas para filtrar")

        st.markdown("")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("🔄 Atualizar Dados", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        with col_b2:
            if st.button("🗑️ Limpar Cache", use_container_width=True):
                st.cache_data.clear()
                st.rerun()

    st.markdown("---")
    col_info1, col_info2, col_info3, col_info4 = st.columns(4)
    col_info1.metric("📋 Registros na planilha", f"{len(df_raw):,}".replace(",", "."))
    col_info2.metric("📅 Datas válidas", f"{df_raw['DATA_DT'].notna().sum():,}".replace(",", "."))
    col_info3.metric("👤 Clientes únicos", f"{df_raw['NOME_CLIENTE'].nunique():,}".replace(",", "."))
    col_info4.metric("🕐 Cache", "1 minuto")

    st.caption(f"Última verificação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} • {len(actual_cols)} colunas detectadas na planilha")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()

try:
    if sel_filial:
        df = df[df["FILIAL"].isin(sel_filial)]
    if sel_supervisor:
        df = df[df["SUPERVISOR"].isin(sel_supervisor)]
    if sel_segmento:
        df = df[df["SEGMENTO"].isin(sel_segmento)]
    if sel_motivo:
        df = df[df["MOTIVO_DEVOLUCAO"].isin(sel_motivo)]
    if filtrar_data and len(datas_validas) > 0:
        mask = df["DATA_DT"].between(pd.Timestamp(dt_ini), pd.Timestamp(dt_fim), inclusive="both")
        df = df[mask | df["DATA_DT"].isna()]
except:
    df = df_raw.copy()

# ── Computed KPIs ─────────────────────────────────────────────────────────────
total_val      = df["VALOR_LIQUIDO"].sum()
total_notas    = len(df)
total_clientes = df["NOME_CLIENTE"].nunique()
ticket_medio   = total_val / total_notas if total_notas > 0 else 0
total_veiculos = df["PLACA"].nunique()

# ════════════════════════════════════════════════════════
# ABA 2 — DASHBOARD
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
            <div class="kpi-value">{total_notas:,}".replace(",", ".")</div>
            <div class="kpi-sub">Registros filtrados</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">👤</div>
            <div class="kpi-label">Clientes</div>
            <div class="kpi-value">{total_clientes:,}".replace(",", ".")</div>
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
            <div class="kpi-value">{total_veiculos}</div>
            <div class="kpi-sub">Placas únicas</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Row 1: Motivo + Evolução
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Devoluções por Motivo (Top 10)</h3></div>', unsafe_allow_html=True)
        df_m = (
            df[df["MOTIVO_DEVOLUCAO"] != "N/D"]
            .groupby("MOTIVO_DEVOLUCAO", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=True)
            .tail(10)
        )
        if not df_m.empty:
            fig_m = px.bar(
                df_m, x="VALOR_LIQUIDO", y="MOTIVO_DEVOLUCAO", orientation="h",
                color="VALOR_LIQUIDO", color_continuous_scale=RED,
                text=df_m["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"MOTIVO_DEVOLUCAO": "", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_m.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_m), use_container_width=True)
        else:
            st.info("Sem dados de motivos")

    with c2:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>📈 Evolução Mensal</h3></div>', unsafe_allow_html=True)
        df_t = df[df["DATA_DT"].notna()].copy()
        if not df_t.empty:
            df_t["MES"] = df_t["DATA_DT"].dt.to_period("M").astype(str)
            df_mes = df_t.groupby("MES", as_index=False)["VALOR_LIQUIDO"].sum().sort_values("MES")
            fig_t = px.area(
                df_mes, x="MES", y="VALOR_LIQUIDO",
                labels={"MES": "Mês", "VALOR_LIQUIDO": "Valor (R$)"},
                color_discrete_sequence=["#0ea5e9"],
            )
            fig_t.update_traces(fill="tozeroy", fillcolor="rgba(14,165,233,0.1)", line=dict(color="#0ea5e9", width=2))
            fig_t.add_scatter(
                x=df_mes["MES"], y=df_mes["VALOR_LIQUIDO"],
                mode="markers", marker=dict(color="#38bdf8", size=7),
                showlegend=False,
            )
            st.plotly_chart(plotly_layout(fig_t), use_container_width=True)
        else:
            st.info("Sem datas válidas para evolução temporal")

    # Row 2: Supervisor + Segmento
    c3, c4 = st.columns(2, gap="large")

    with c3:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>👔 Devoluções por Supervisor / AM</h3></div>', unsafe_allow_html=True)
        df_sup = (
            df[df["SUPERVISOR"] != "N/D"]
            .groupby("SUPERVISOR", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=True)
            .tail(12)
        )
        if not df_sup.empty:
            fig_sup = px.bar(
                df_sup, x="VALOR_LIQUIDO", y="SUPERVISOR", orientation="h",
                color="VALOR_LIQUIDO", color_continuous_scale=BLUE,
                text=df_sup["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"SUPERVISOR": "", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_sup.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_sup), use_container_width=True)
        else:
            st.info("Sem dados de supervisor")

    with c4:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏷️ Devoluções por Segmento</h3></div>', unsafe_allow_html=True)
        df_seg = (
            df[df["SEGMENTO"] != "N/D"]
            .groupby("SEGMENTO", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=False)
        )
        if not df_seg.empty:
            fig_seg = px.pie(
                df_seg, names="SEGMENTO", values="VALOR_LIQUIDO",
                color_discrete_sequence=MIXED, hole=0.48,
            )
            fig_seg.update_traces(
                textfont_size=11,
                marker=dict(line=dict(color="#060d1f", width=2.5)),
                pull=[0.04] + [0] * (len(df_seg) - 1),
            )
            st.plotly_chart(plotly_layout(fig_seg), use_container_width=True)
        else:
            st.info("Sem dados de segmento")

    # Row 3: Vendedor + Veículo
    c5, c6 = st.columns(2, gap="large")

    with c5:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🧑‍💼 Top 10 Vendedores / Funcionários</h3></div>', unsafe_allow_html=True)
        df_vend = (
            df[df["VENDEDOR"] != "N/D"]
            .groupby("VENDEDOR", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=True)
            .tail(10)
        )
        if not df_vend.empty:
            fig_vend = px.bar(
                df_vend, x="VALOR_LIQUIDO", y="VENDEDOR", orientation="h",
                color="VALOR_LIQUIDO", color_continuous_scale=RED,
                text=df_vend["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"VENDEDOR": "", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_vend.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_vend), use_container_width=True)
        else:
            st.info("Sem dados de vendedores/funcionários")

    with c6:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🚚 Top 12 Veículos / Praças</h3></div>', unsafe_allow_html=True)
        df_v = (
            df[df["PLACA"] != "N/D"]
            .groupby("PLACA", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=False)
            .head(12)
        )
        if not df_v.empty:
            fig_v = px.bar(
                df_v, x="PLACA", y="VALOR_LIQUIDO",
                color="VALOR_LIQUIDO", color_continuous_scale=BLUE,
                text=df_v["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"PLACA": "Veículo/Praça", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_v.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_v, margin_b=80), use_container_width=True)
        else:
            st.info("Sem dados de veículos")

    # Row 4: Ranking Motivos
    st.markdown("---")
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>📊 Ranking Completo de Motivos de Devolução</h3></div>', unsafe_allow_html=True)
    df_rank = (
        df.groupby("MOTIVO_DEVOLUCAO", as_index=False)
        .agg(Qtd=("VALOR_LIQUIDO", "count"), Total=("VALOR_LIQUIDO", "sum"))
        .sort_values("Total", ascending=False)
    )
    df_rank["Valor Total"] = df_rank["Total"].apply(fmt_brl)
    df_rank["% do Total"] = (df_rank["Total"] / total_val * 100).round(1).astype(str) + "%" if total_val > 0 else "0%"
    df_rank = df_rank.rename(columns={"MOTIVO_DEVOLUCAO": "Motivo", "Qtd": "Qtd"})
    st.dataframe(
        df_rank[["Motivo", "Qtd", "Valor Total", "% do Total"]],
        use_container_width=True, hide_index=True, height=280,
    )

    # Filial donut
    st.markdown("")
    c7, c8 = st.columns([1, 2], gap="large")
    with c7:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏢 Por Filial / Regional</h3></div>', unsafe_allow_html=True)
        df_fil = (
            df[~df["FILIAL"].isin(["N/D", "nan", ""])]
            .groupby("FILIAL", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=False)
        )
        if not df_fil.empty:
            fig_fil = px.pie(df_fil, names="FILIAL", values="VALOR_LIQUIDO",
                             color_discrete_sequence=BLUE, hole=0.5)
            fig_fil.update_traces(marker=dict(line=dict(color="#060d1f", width=2)))
            st.plotly_chart(plotly_layout(fig_fil), use_container_width=True)
        else:
            st.info("Sem dados de filial/regional")
    with c8:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🏙️ Top 10 Clientes por Valor Devolvido</h3></div>', unsafe_allow_html=True)
        df_cli = (
            df[df["NOME_CLIENTE"] != "N/D"]
            .groupby("NOME_CLIENTE", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=True)
            .tail(10)
        )
        if not df_cli.empty:
            fig_cli = px.bar(
                df_cli, x="VALOR_LIQUIDO", y="NOME_CLIENTE", orientation="h",
                color="VALOR_LIQUIDO", color_continuous_scale=MIXED,
                text=df_cli["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"NOME_CLIENTE": "", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_cli.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_cli), use_container_width=True)
        else:
            st.info("Sem dados de clientes")

# ════════════════════════════════════════════════════════
# ABA 3 — PESQUISA
# ════════════════════════════════════════════════════════
with tab_pesquisa:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🔎 Pesquisa Avançada de Devoluções</h3></div>', unsafe_allow_html=True)

    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3, gap="medium")
    with p1:
        s_cliente  = st.text_input("👤 Cliente (nome ou parte)", placeholder="Ex: MERCADO SILVA")
        s_vendedor = st.text_input("🧑‍💼 Vendedor / Funcionário", placeholder="Ex: ALBERTO")
    with p2:
        s_nf       = st.text_input("📄 Nota Fiscal (devolução)", placeholder="Ex: 12345")
        s_nf_venda = st.text_input("🧾 NF de Venda / Saída", placeholder="Ex: 537088")
    with p3:
        s_pedido   = st.text_input("📦 Nº do Pedido / CLI", placeholder="Ex: 10056")
        s_carreg   = st.text_input("🚛 Nº do Carregamento", placeholder="Ex: 8456")

    p4, p5, p6 = st.columns(3, gap="medium")
    with p4:
        s_placa    = st.text_input("🚚 Placa / Praça", placeholder="Ex: 4M-COR")
        s_motivo_p = st.text_input("❗ Motivo de Devolução", placeholder="Ex: Avaria")
    with p5:
        s_num_dev  = st.text_input("🔢 Nº da Devolução", placeholder="Ex: 8456")
        s_supervisor = st.text_input("👔 Supervisor / AM", placeholder="Ex: GILVAN")
    with p6:
        s_cidade   = st.text_input("🏙️ Cidade / Praça", placeholder="Ex: Manaus")
        s_filial   = st.text_input("🏢 Filial / Regional", placeholder="Ex: RTINS")

    st.markdown('</div>', unsafe_allow_html=True)

    col_pb1, col_pb2, _ = st.columns([1, 1, 4])
    with col_pb1:
        btn_pesq = st.button("🔍 Pesquisar", use_container_width=True)
    with col_pb2:
        btn_limpar = st.button("🗑️ Limpar", use_container_width=True)

    st.markdown("---")

    df_pesq = df.copy()

    def apply_search(df_in, col, val):
        if val.strip():
            return df_in[df_in[col].str.contains(val.strip(), case=False, na=False)]
        return df_in

    filtros = []
    if s_cliente:    df_pesq = apply_search(df_pesq, "NOME_CLIENTE",     s_cliente);    filtros.append(f"Cliente: {s_cliente}")
    if s_vendedor:   df_pesq = apply_search(df_pesq, "VENDEDOR",         s_vendedor);   filtros.append(f"Vendedor: {s_vendedor}")
    if s_nf:         df_pesq = apply_search(df_pesq, "NOTA_FISCAL",      s_nf);         filtros.append(f"NF: {s_nf}")
    if s_nf_venda:   df_pesq = apply_search(df_pesq, "NF_VENDA",         s_nf_venda);   filtros.append(f"NF Venda: {s_nf_venda}")
    if s_pedido:     df_pesq = apply_search(df_pesq, "NUM_PEDIDO",       s_pedido);     filtros.append(f"Pedido: {s_pedido}")
    if s_carreg:     df_pesq = apply_search(df_pesq, "NUM_CARREGAMENTO", s_carreg);     filtros.append(f"Carregamento: {s_carreg}")
    if s_placa:      df_pesq = apply_search(df_pesq, "PLACA",            s_placa);      filtros.append(f"Placa: {s_placa}")
    if s_motivo_p:   df_pesq = apply_search(df_pesq, "MOTIVO_DEVOLUCAO", s_motivo_p);   filtros.append(f"Motivo: {s_motivo_p}")
    if s_num_dev:    df_pesq = apply_search(df_pesq, "NUM_DEVOLUCAO",    s_num_dev);    filtros.append(f"Nº Dev: {s_num_dev}")
    if s_supervisor: df_pesq = apply_search(df_pesq, "SUPERVISOR",       s_supervisor); filtros.append(f"Supervisor: {s_supervisor}")
    if s_cidade:     df_pesq = apply_search(df_pesq, "CIDADE",           s_cidade);     filtros.append(f"Cidade: {s_cidade}")
    if s_filial:     df_pesq = apply_search(df_pesq, "FILIAL",           s_filial);     filtros.append(f"Filial: {s_filial}")

    if filtros:
        st.info(f"🔍 **{len(df_pesq)} resultado(s)** | Filtros: {' · '.join(filtros)}")
    else:
        st.caption(f"Exibindo todos os {len(df_pesq)} registros filtrados. Use os campos acima para refinar.")

    if len(df_pesq) == 0:
        st.warning("⚠️ Nenhum registro encontrado para os critérios informados.")
    elif len(df_pesq) <= 30:
        for _, row in df_pesq.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px;">
                    <div style="flex:1;">
                        <div class="rc-client">👤 {row['NOME_CLIENTE']}</div>
                        <div class="rc-row">
                            <span>📄 NF Dev: <b>{row['NOTA_FISCAL']}</b></span>
                            <span>🧾 NF Venda: <b>{row['NF_VENDA']}</b></span>
                            <span>📦 Pedido: <b>{row['NUM_PEDIDO']}</b></span>
                            <span>🚛 Carreg.: <b>{row['NUM_CARREGAMENTO']}</b></span>
                            <span>🔢 Dev: <b>{row['NUM_DEVOLUCAO']}</b></span>
                        </div>
                        <div class="rc-row" style="margin-top:8px;">
                            <span>🚚 {row['PLACA']}</span>
                            <span class="rc-badge">❗ {row['MOTIVO_DEVOLUCAO']}</span>
                            <span>🧑‍💼 {row['VENDEDOR']}</span>
                            <span>👔 {row['SUPERVISOR']}</span>
                            <span>📅 {row['DATA_DEVOLUCAO']}</span>
                        </div>
                        <div class="rc-row" style="margin-top:4px;">
                            <span>🏢 {row['FILIAL']}</span>
                            <span>🏙️ {row['CIDADE']}</span>
                            <span>🏷️ {row['SEGMENTO']}</span>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div class="rc-val">{fmt_brl(row['VALOR_LIQUIDO'])}</div>
                        <div style="font-size:0.7rem; color:#475569; margin-top:4px;">Valor líquido</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        COLS_P = [c for c in [
            "DATA_DEVOLUCAO", "NUM_DEVOLUCAO", "NOTA_FISCAL", "NF_VENDA",
            "NUM_PEDIDO", "NUM_CARREGAMENTO", "NOME_CLIENTE", "CIDADE",
            "MOTIVO_DEVOLUCAO", "PLACA", "VENDEDOR", "SUPERVISOR",
            "FILIAL", "SEGMENTO", "VALOR_LIQUIDO",
        ] if c in df_pesq.columns]
        df_sp = df_pesq[COLS_P].rename(columns={
            "DATA_DEVOLUCAO": "Data", "NUM_DEVOLUCAO": "Nº Dev.",
            "NOTA_FISCAL": "NF Dev.", "NF_VENDA": "NF Venda",
            "NUM_PEDIDO": "Pedido", "NUM_CARREGAMENTO": "Carregamento",
            "NOME_CLIENTE": "Cliente", "CIDADE": "Cidade",
            "MOTIVO_DEVOLUCAO": "Motivo", "PLACA": "Placa/Praça",
            "VENDEDOR": "Vendedor", "SUPERVISOR": "Supervisor",
            "FILIAL": "Filial", "SEGMENTO": "Segmento",
            "VALOR_LIQUIDO": "Valor (R$)",
        })
        st.dataframe(
            df_sp.style.format({"Valor (R$)": lambda v: fmt_brl(v)}),
            use_container_width=True, height=500, hide_index=True,
        )

    if len(df_pesq) > 0:
        st.markdown("---")
        csv_p = df_pesq.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button(
            "⬇️ Exportar resultado (.csv)",
            data=csv_p,
            file_name=f"pesquisa_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

# ════════════════════════════════════════════════════════
# ABA 4 — DADOS COMPLETOS
# ════════════════════════════════════════════════════════
with tab_dados:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>📑 Detalhamento Completo das Devoluções</h3></div>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3, gap="medium")
    with d1:
        sort_col = st.selectbox("Ordenar por", [
            "VALOR_LIQUIDO", "DATA_DEVOLUCAO", "NOME_CLIENTE",
            "SUPERVISOR", "MOTIVO_DEVOLUCAO", "FILIAL",
        ], format_func=lambda x: {
            "VALOR_LIQUIDO": "💰 Valor", "DATA_DEVOLUCAO": "📅 Data",
            "NOME_CLIENTE": "👤 Cliente", "SUPERVISOR": "👔 Supervisor",
            "MOTIVO_DEVOLUCAO": "❗ Motivo", "FILIAL": "🏢 Filial",
        }.get(x, x))
    with d2:
        sort_asc = st.radio("Direção", ["↑ Crescente", "↓ Decrescente"], horizontal=True) == "↑ Crescente"
    with d3:
        n_rows = st.selectbox("Máximo de linhas", [50, 100, 250, 500, 1000, "Todos"])

    df_sorted = df.sort_values(sort_col, ascending=sort_asc)
    if n_rows != "Todos":
        df_sorted = df_sorted.head(int(n_rows))

    SHOW = [c for c in [
        "DATA_DEVOLUCAO", "NUM_DEVOLUCAO", "NOTA_FISCAL", "NF_VENDA",
        "NUM_PEDIDO", "NUM_CARREGAMENTO", "NOME_CLIENTE", "CIDADE",
        "MOTIVO_DEVOLUCAO", "PLACA", "VENDEDOR", "SUPERVISOR",
        "FILIAL", "SEGMENTO", "VALOR_LIQUIDO",
    ] if c in df_sorted.columns]

    df_disp = df_sorted[SHOW].rename(columns={
        "DATA_DEVOLUCAO": "Data", "NUM_DEVOLUCAO": "Nº Dev.",
        "NOTA_FISCAL": "NF Dev.", "NF_VENDA": "NF Venda",
        "NUM_PEDIDO": "Pedido", "NUM_CARREGAMENTO": "Carregamento",
        "NOME_CLIENTE": "Cliente", "CIDADE": "Cidade",
        "MOTIVO_DEVOLUCAO": "Motivo", "PLACA": "Placa/Praça",
        "VENDEDOR": "Vendedor", "SUPERVISOR": "Supervisor",
        "FILIAL": "Filial", "SEGMENTO": "Segmento",
        "VALOR_LIQUIDO": "Valor (R$)",
    })

    st.dataframe(
        df_disp.style.format({"Valor (R$)": lambda v: fmt_brl(v)}),
        use_container_width=True, height=520, hide_index=True,
    )
    st.caption(f"Exibindo {len(df_disp)} de {len(df)} registros filtrados · Total bruto: {len(df_raw)}")

    st.markdown("---")
    e1, e2, e3 = st.columns(3, gap="medium")
    with e1:
        csv_all = df[SHOW].to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar filtrados (.csv)", data=csv_all,
            file_name=f"devolucoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)
    with e2:
        df_res = (df.groupby("MOTIVO_DEVOLUCAO", as_index=False)
            .agg(Qtd=("VALOR_LIQUIDO","count"), Total=("VALOR_LIQUIDO","sum"))
            .sort_values("Total", ascending=False))
        csv_res = df_res.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Resumo por Motivo (.csv)", data=csv_res,
            file_name=f"resumo_motivos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)
    with e3:
        df_sup_exp = (df.groupby("SUPERVISOR", as_index=False)
            .agg(Qtd=("VALOR_LIQUIDO","count"), Total=("VALOR_LIQUIDO","sum"))
            .sort_values("Total", ascending=False))
        csv_sup = df_sup_exp.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Resumo por Supervisor (.csv)", data=csv_sup,
            file_name=f"resumo_supervisores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)

    with st.expander("🔍 Diagnóstico: colunas detectadas na planilha"):
        st.write(f"**Colunas originais ({len(actual_cols)}):** `{actual_cols}`")
        st.write(f"**Mapeamentos aplicados:** `{COL_MAP}`")
        st.write(f"**Registros com Valor > 0:** {(df_raw['VALOR_LIQUIDO'] > 0).sum()}")
        st.write(f"**Registros com data válida:** {df_raw['DATA_DT'].notna().sum()}")
        st.markdown("**Amostra (5 linhas originais):**")
        st.dataframe(df_raw.head(5), use_container_width=True)

# ════════════════════════════════════════════════════════
# ABA 5 — CONFIG
# ════════════════════════════════════════════════════════
with tab_config:
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🛠️ Configurações e Instruções</h3></div>', unsafe_allow_html=True)

    cfg1, cfg2 = st.columns(2, gap="large")

    with cfg1:
        st.markdown("### 📋 Como configurar a planilha")
        st.markdown("""
**Para que os dados apareçam corretamente:**

1. Abra sua planilha no **Google Sheets**
2. Clique em **Arquivo → Compartilhar → Publicar na web**
3. Selecione a aba desejada → formato **CSV**
4. Clique em **Publicar** e copie o link gerado
5. Cole o link na variável `GSHEETS_URL` no código

> ⚠️ O link de publicação **é diferente** do link de compartilhamento normal.
> O link correto contém `/pub?` na URL.
        """)

        st.markdown("### 🔗 URL atual")
        st.code(GSHEETS_URL, language="text")

        st.markdown("### 🔄 Cache & Atualização")
        st.info("⏱️ Dados atualizados automaticamente a **cada 1 minuto**.")
        if st.button("🗑️ Limpar cache e recarregar agora", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache limpo!")
            st.rerun()

    with cfg2:
        st.markdown("### 📐 Colunas esperadas na planilha")
        st.markdown("""
| Coluna | Descrição |
|---|---|
| `NOMERCA` ou `NOME_CLIENTE` | Nome do cliente / mercado |
| `SUPERVISOR` | Supervisor / AM |
| `NOMEFUNC` ou `VENDEDOR` | Nome do funcionário/vendedor |
| `VLT` ou `VALOR_LIQUIDO` | Valor total da devolução |
| `NOTA_FISCAL` ou `NUMERO` | NF de devolução |
| `NF_VENDA` | NF de venda original |
| `NUM_PEDIDO` ou `CLI` | Número do pedido |
| `NUM_CARREGAMENTO` | Número do carregamento |
| `PLACA` ou `PRACA` | Placa do veículo / praça |
| `MOTIVO_DEVOLUCAO` | Motivo da devolução |
| `DATA_DEVOLUCAO` ou `DATA` | Data da devolução |
| `FILIAL` | Filial / Regional |
| `SEGMENTO` | Segmento de mercado |
| `CIDADE` | Cidade do cliente |
        """)

        st.markdown("### 📊 Status atual")
        st.metric("Colunas detectadas", len(actual_cols))
        st.metric("Mapeamentos aplicados", len(COL_MAP))
        st.metric("Registros com valor > 0", f"{(df_raw['VALOR_LIQUIDO'] > 0).sum():,}".replace(",","."))
