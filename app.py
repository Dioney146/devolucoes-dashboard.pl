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
    initial_sidebar_state="expanded",
)

# ── CSS Global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #0a0f1e !important;
    font-family: 'DM Sans', sans-serif;
    color: #e2e8f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1630 0%, #0a0f1e 100%) !important;
    border-right: 1px solid rgba(99,179,237,0.15);
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] * { color: #cbd5e0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stTextInput label { color: #90cdf4 !important; font-weight: 600; }

/* ── Sidebar logo area ── */
.sidebar-logo {
    background: linear-gradient(135deg, #1a365d, #2a4a7f);
    border-bottom: 1px solid rgba(99,179,237,0.2);
    padding: 20px 16px 16px;
    margin: -1rem -1rem 1rem;
    text-align: center;
}
.sidebar-logo h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    color: #90cdf4 !important;
    letter-spacing: 0.05em;
    margin: 0 !important;
    text-shadow: none !important;
}
.sidebar-logo p { font-size: 0.72rem; color: #718096 !important; margin: 4px 0 0; }

/* ── Main header ── */
.main-header {
    background: linear-gradient(135deg, #1a365d 0%, #153e75 50%, #1a4a8a 100%);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.main-header h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: #e2e8f0 !important;
    text-shadow: 0 2px 20px rgba(0,0,0,0.4) !important;
    margin: 0 !important;
    letter-spacing: -0.01em;
}
.main-header p { color: #90cdf4 !important; margin: 6px 0 0 !important; font-size: 0.9rem; }
.header-badge {
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 50px;
    padding: 8px 18px;
    font-size: 0.8rem;
    color: #90cdf4 !important;
    white-space: nowrap;
}

/* ── KPI cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #141e38 0%, #1a2848 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 14px;
    padding: 20px 22px !important;
    transition: border-color 0.2s, transform 0.2s;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(99,179,237,0.5);
    transform: translateY(-2px);
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    color: #90cdf4 !important;
}
[data-testid="stMetricLabel"] { color: #718096 !important; font-size: 0.82rem !important; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1630;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(99,179,237,0.15);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 9px;
    color: #718096 !important;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 10px 20px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a365d, #2b6cb0) !important;
    color: #e2e8f0 !important;
    box-shadow: 0 2px 12px rgba(43,108,176,0.4);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px; }

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(99,179,237,0.15) !important;
}
.stDataFrame thead th {
    background: #1a365d !important;
    color: #90cdf4 !important;
    font-weight: 700 !important;
}

/* ── Section titles ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
    border-left: 4px solid #4299e1;
    padding-left: 12px;
    margin-bottom: 16px;
}

/* ── Search result card ── */
.result-card {
    background: linear-gradient(135deg, #141e38, #1a2848);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: rgba(99,179,237,0.5); }
.result-card .rc-title { font-weight: 700; color: #90cdf4; font-size: 1rem; }
.result-card .rc-sub { color: #718096; font-size: 0.82rem; margin-top: 4px; }
.result-card .rc-val { font-family: 'Syne', sans-serif; font-weight: 700; color: #68d391; font-size: 1.1rem; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1a365d, #2b6cb0);
    color: #e2e8f0;
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 9px;
    font-weight: 600;
    padding: 8px 20px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2b6cb0, #3182ce);
    border-color: rgba(99,179,237,0.6);
    transform: translateY(-1px);
}

/* ── Dividers ── */
hr { border-color: rgba(99,179,237,0.12) !important; margin: 18px 0 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #141e38 !important;
    border-radius: 10px !important;
    color: #90cdf4 !important;
    font-weight: 600 !important;
}
details[open] .streamlit-expanderHeader { border-radius: 10px 10px 0 0 !important; }

/* ── Input fields ── */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background: #0d1630 !important;
    border-color: rgba(99,179,237,0.25) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: #1a365d !important;
    color: #90cdf4 !important;
}

/* ── Caption / small text ── */
.stCaption, small { color: #4a5568 !important; font-size: 0.78rem !important; }

/* ── Info / alert ── */
.stAlert { border-radius: 10px; }

/* ── Radio ── */
.stRadio label { color: #cbd5e0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: #2b6cb0; border-radius: 3px; }

/* ── Hide streamlit default branding ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def plotly_layout(fig, margin_b=40):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="#cbd5e0", family="DM Sans"),
        coloraxis_showscale=False,
        margin=dict(t=30, b=margin_b, l=10, r=10),
        xaxis=dict(
            tickfont=dict(color="#718096", size=10),
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.08)",
        ),
        yaxis=dict(
            tickfont=dict(color="#718096", size=10),
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.08)",
        ),
        legend=dict(
            bgcolor="rgba(13,22,48,0.8)",
            bordercolor="rgba(99,179,237,0.2)",
            borderwidth=1,
            font=dict(color="#cbd5e0"),
        ),
    )
    return fig

BLUE_SCALE  = ["#1a365d", "#2b6cb0", "#4299e1", "#90cdf4"]
RED_SCALE   = ["#742a2a", "#c53030", "#fc8181", "#fed7d7"]
GREEN_SCALE = ["#1c4532", "#276749", "#38a169", "#9ae6b4"]
MIXED_SCALE = ["#1a365d", "#4299e1", "#38a169", "#ecc94b", "#e53e3e"]

# ── URL da planilha ───────────────────────────────────────────────────────────
# Publica a planilha em: Arquivo > Compartilhar > Publicar na web > CSV
# e cole o link abaixo (ou configure a variável de ambiente GSHEETS_URL)
GSHEETS_DEFAULT = (
    "https://docs.google.com/spreadsheets/d/1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI/edit?usp=sharing"
)
GSHEETS_URL = os.getenv("GSHEETS_URL", GSHEETS_DEFAULT)

# ── Carregamento ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)  # atualiza a cada 1 minuto
def load_data(url: str) -> pd.DataFrame:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/csv,application/csv,*/*",
    }
    try:
        resp = requests.get(url, timeout=25, headers=headers)
        resp.raise_for_status()
        if "format=csv" in url or "output=csv" in url:
            df = pd.read_csv(io.StringIO(resp.text))
        else:
            df = pd.read_excel(io.BytesIO(resp.content))
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}\n\nVerifique se a planilha está publicada publicamente.")
        st.stop()

with st.spinner("Carregando dados da planilha..."):
    df_raw = load_data(GSHEETS_URL)

# ── Normalização ──────────────────────────────────────────────────────────────
df_raw.columns = [str(c).strip().upper().replace(" ", "_") for c in df_raw.columns]

# Mapeamento flexível de colunas comuns
COL_MAP = {}
col_aliases = {
    "VALOR_LIQUIDO":    ["VALOR_LIQUIDO", "VALOR LIQUIDO", "VALOR", "TOTAL", "VLR_LIQUIDO", "VALOR_LIQ"],
    "DATA_DEVOLUCAO":   ["DATA_DEVOLUCAO", "DATA DEVOLUÇÃO", "DATA", "DT_DEVOLUCAO", "DATA_DEV"],
    "NOME_CLIENTE":     ["NOME_CLIENTE", "CLIENTE", "NOME CLIENTE", "RAZAO_SOCIAL", "RAZÃO SOCIAL"],
    "PLACA":            ["PLACA", "PLACA_VEICULO", "VEICULO", "VEÍCULO"],
    "MOTIVO_DEVOLUCAO": ["MOTIVO_DEVOLUCAO", "MOTIVO DEVOLUÇÃO", "MOTIVO", "MOTIVO_DEV"],
    "VENDEDOR":         ["VENDEDOR", "NOME_VENDEDOR", "REPR_VENDAS"],
    "SUPERVISOR":       ["SUPERVISOR", "NOME_SUPERVISOR", "GERENTE"],
    "FILIAL":           ["FILIAL", "UNIDADE", "CD", "CENTRO_DISTRIBUICAO"],
    "SEGMENTO":         ["SEGMENTO", "SEGM", "CANAL", "TIPO_CLIENTE"],
    "CIDADE":           ["CIDADE", "MUNICIPIO", "MUNICÍPIO"],
    "NOTA_FISCAL":      ["NOTA_FISCAL", "NF", "NF_DEVOLUCAO", "NOTA FISCAL", "NF_SAIDA"],
    "NUM_DEVOLUCAO":    ["NUM_DEVOLUCAO", "NUMERO_DEVOLUCAO", "NR_DEVOLUCAO", "N_DEVOLUCAO", "DEVOLUCAO"],
    "NUM_PEDIDO":       ["NUM_PEDIDO", "PEDIDO", "NR_PEDIDO", "N_PEDIDO", "COD_PEDIDO"],
    "NUM_CARREGAMENTO": ["NUM_CARREGAMENTO", "CARREGAMENTO", "NR_CARREGAMENTO", "N_CARREGAMENTO"],
    "NF_VENDA":         ["NF_VENDA", "NOTA_VENDA", "NF_ENTRADA", "NF VENDA"],
}

existing_cols = set(df_raw.columns)
for std_col, aliases in col_aliases.items():
    for alias in aliases:
        if alias in existing_cols:
            COL_MAP[alias] = std_col
            break

df_raw = df_raw.rename(columns=COL_MAP)

# Garante que todas as colunas padrão existam
all_std_cols = list(col_aliases.keys())
for col in all_std_cols:
    if col not in df_raw.columns:
        df_raw[col] = "N/D"
    else:
        df_raw[col] = df_raw[col].fillna("N/D").astype(str).str.strip()

# Valor numérico
df_raw["VALOR_LIQUIDO"] = pd.to_numeric(
    df_raw["VALOR_LIQUIDO"].astype(str)
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip(),
    errors="coerce"
).fillna(0)

# Data
try:
    df_raw["DATA_DEVOLUCAO_DT"] = pd.to_datetime(df_raw["DATA_DEVOLUCAO"], dayfirst=True, errors="coerce")
except:
    df_raw["DATA_DEVOLUCAO_DT"] = pd.NaT

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>📦 DEVOLUÇÕES</h2>
        <p>Sistema de Análise e Controle</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Filtros Globais")

    # Filial
    filiais = sorted([x for x in df_raw["FILIAL"].unique() if x != "N/D"])
    if filiais:
        sel_filial = st.multiselect("🏢 Filial", filiais, default=filiais)
    else:
        sel_filial = []
        st.info("Coluna FILIAL não encontrada")

    # Segmento
    segmentos = sorted([x for x in df_raw["SEGMENTO"].unique() if x != "N/D"])
    if segmentos:
        sel_segmento = st.multiselect("🏷️ Segmento", segmentos, default=segmentos)
    else:
        sel_segmento = []

    # Supervisor
    supervisores = sorted([x for x in df_raw["SUPERVISOR"].unique() if x != "N/D"])
    if supervisores:
        sel_supervisor = st.multiselect("👔 Supervisor", supervisores, default=supervisores)
    else:
        sel_supervisor = []

    # Período
    st.markdown("---")
    st.markdown("### 📅 Período")
    datas_validas = df_raw["DATA_DEVOLUCAO_DT"].dropna()
    if len(datas_validas) > 0:
        dt_min = datas_validas.min().date()
        dt_max = datas_validas.max().date()
        dt_ini = st.date_input("De", value=dt_min, min_value=dt_min, max_value=dt_max)
        dt_fim = st.date_input("Até", value=dt_max, min_value=dt_min, max_value=dt_max)
        filtrar_data = True
    else:
        filtrar_data = False
        st.caption("Sem datas válidas para filtrar")

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
            st.rerun()
    with col_btn2:
        if st.button("🗑️ Limpar"):
            st.rerun()

    st.markdown("---")
    st.caption(f"🕐 Última verificação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    st.caption(f"📊 Total de registros: {len(df_raw)}")
    st.caption("♻️ Cache: 1 minuto")

# ── Aplicar filtros ───────────────────────────────────────────────────────────
df = df_raw.copy()

if sel_filial:
    df = df[df["FILIAL"].isin(sel_filial)]
if sel_segmento:
    df = df[df["SEGMENTO"].isin(sel_segmento)]
if sel_supervisor:
    df = df[df["SUPERVISOR"].isin(sel_supervisor)]
if filtrar_data and len(datas_validas) > 0:
    dt_ini_ts = pd.Timestamp(dt_ini)
    dt_fim_ts = pd.Timestamp(dt_fim)
    mask_data = df["DATA_DEVOLUCAO_DT"].between(dt_ini_ts, dt_fim_ts, inclusive="both")
    df = df[mask_data | df["DATA_DEVOLUCAO_DT"].isna()]

# ── HEADER ────────────────────────────────────────────────────────────────────
now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"""
<div class="main-header">
    <div>
        <h1>📦 Demonstrativo de Devoluções</h1>
        <p>Análise completa de notas fiscais de devolução • Dados em tempo real</p>
    </div>
    <div class="header-badge">🟢 Ao Vivo &nbsp;|&nbsp; {now_str}</div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_val       = df["VALOR_LIQUIDO"].sum()
total_notas     = len(df)
total_clientes  = df["NOME_CLIENTE"].nunique()
ticket_medio    = total_val / total_notas if total_notas else 0
total_veiculos  = df["PLACA"].nunique()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Valor Total", fmt_brl(total_val))
k2.metric("📄 Devoluções",  f"{total_notas:,}".replace(",", "."))
k3.metric("👤 Clientes",    f"{total_clientes:,}".replace(",", "."))
k4.metric("📊 Ticket Médio", fmt_brl(ticket_medio))
k5.metric("🚚 Veículos",    f"{total_veiculos:,}".replace(",", "."))

st.markdown("---")

# ── ABAS ──────────────────────────────────────────────────────────────────────
tab_dash, tab_pesquisa, tab_dados, tab_config = st.tabs([
    "📊  Dashboard",
    "🔎  Pesquisa",
    "📑  Dados Completos",
    "⚙️  Configurações",
])

# ════════════════════════════════════════════════════════
# ABA 1 — DASHBOARD
# ════════════════════════════════════════════════════════
with tab_dash:

    # Row 1: Veículo + Motivo
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown('<div class="section-title">🚚 Devoluções por Veículo (Top 15)</div>', unsafe_allow_html=True)
        df_v = (
            df.groupby("PLACA", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=False)
            .head(15)
        )
        if not df_v.empty:
            fig_v = px.bar(
                df_v, x="PLACA", y="VALOR_LIQUIDO",
                color="VALOR_LIQUIDO",
                color_continuous_scale=BLUE_SCALE,
                text=df_v["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"PLACA": "Veículo", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_v.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_v), use_container_width=True)
        else:
            st.info("Sem dados de veículos")

    with col_r:
        st.markdown('<div class="section-title">❗ Devoluções por Motivo</div>', unsafe_allow_html=True)
        df_m = (
            df.groupby("MOTIVO_DEVOLUCAO", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=False)
            .head(10)
        )
        if not df_m.empty:
            fig_m = px.bar(
                df_m, x="MOTIVO_DEVOLUCAO", y="VALOR_LIQUIDO",
                color="VALOR_LIQUIDO",
                color_continuous_scale=RED_SCALE,
                text=df_m["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"MOTIVO_DEVOLUCAO": "Motivo", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_m.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_m, margin_b=100), use_container_width=True)
        else:
            st.info("Sem dados de motivos")

    # Row 2: Evolução temporal + Filial
    col_l2, col_r2 = st.columns(2, gap="large")

    with col_l2:
        st.markdown('<div class="section-title">📈 Evolução Temporal</div>', unsafe_allow_html=True)
        df_t = df[df["DATA_DEVOLUCAO_DT"].notna()].copy()
        if not df_t.empty:
            df_t["MES"] = df_t["DATA_DEVOLUCAO_DT"].dt.to_period("M").astype(str)
            df_mes = (
                df_t.groupby("MES", as_index=False)["VALOR_LIQUIDO"]
                .sum()
                .sort_values("MES")
            )
            fig_t = px.area(
                df_mes, x="MES", y="VALOR_LIQUIDO",
                labels={"MES": "Mês", "VALOR_LIQUIDO": "Valor (R$)"},
                color_discrete_sequence=["#4299e1"],
            )
            fig_t.update_traces(
                fill="tozeroy",
                fillcolor="rgba(66,153,225,0.15)",
                line=dict(color="#4299e1", width=2),
            )
            st.plotly_chart(plotly_layout(fig_t), use_container_width=True)
        else:
            st.info("Sem datas válidas para evolução temporal")

    with col_r2:
        st.markdown('<div class="section-title">🏢 Devoluções por Filial</div>', unsafe_allow_html=True)
        df_f = (
            df.groupby("FILIAL", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=False)
        )
        df_f = df_f[df_f["FILIAL"] != "N/D"]
        if not df_f.empty:
            fig_f = px.pie(
                df_f, names="FILIAL", values="VALOR_LIQUIDO",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                hole=0.45,
            )
            fig_f.update_traces(
                textfont_size=11,
                marker=dict(line=dict(color="#0a0f1e", width=2)),
            )
            st.plotly_chart(plotly_layout(fig_f), use_container_width=True)
        else:
            st.info("Sem dados de filial")

    # Row 3: Vendedor + Segmento
    col_l3, col_r3 = st.columns(2, gap="large")

    with col_l3:
        st.markdown('<div class="section-title">🧑‍💼 Top Vendedores por Devolução</div>', unsafe_allow_html=True)
        df_vend = (
            df[df["VENDEDOR"] != "N/D"]
            .groupby("VENDEDOR", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=True)
            .tail(10)
        )
        if not df_vend.empty:
            fig_vend = px.bar(
                df_vend, x="VALOR_LIQUIDO", y="VENDEDOR",
                orientation="h",
                color="VALOR_LIQUIDO",
                color_continuous_scale=RED_SCALE,
                text=df_vend["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"VENDEDOR": "", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_vend.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_vend), use_container_width=True)
        else:
            st.info("Sem dados de vendedores")

    with col_r3:
        st.markdown('<div class="section-title">🏷️ Devoluções por Segmento</div>', unsafe_allow_html=True)
        df_seg = (
            df[df["SEGMENTO"] != "N/D"]
            .groupby("SEGMENTO", as_index=False)["VALOR_LIQUIDO"]
            .sum()
            .sort_values("VALOR_LIQUIDO", ascending=False)
        )
        if not df_seg.empty:
            fig_seg = px.bar(
                df_seg, x="SEGMENTO", y="VALOR_LIQUIDO",
                color="VALOR_LIQUIDO",
                color_continuous_scale=GREEN_SCALE,
                text=df_seg["VALOR_LIQUIDO"].apply(fmt_brl),
                labels={"SEGMENTO": "Segmento", "VALOR_LIQUIDO": "Valor (R$)"},
            )
            fig_seg.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig_seg), use_container_width=True)
        else:
            st.info("Sem dados de segmento")

    # Ranking motivos
    st.markdown("---")
    st.markdown('<div class="section-title">📊 Ranking Completo — Motivos de Devolução</div>', unsafe_allow_html=True)
    df_rank = (
        df.groupby("MOTIVO_DEVOLUCAO", as_index=False)
        .agg(
            Quantidade=("VALOR_LIQUIDO", "count"),
            Valor_Total=("VALOR_LIQUIDO", "sum"),
        )
        .sort_values("Valor_Total", ascending=False)
    )
    df_rank["Valor_Total_Fmt"] = df_rank["Valor_Total"].apply(fmt_brl)
    df_rank["% do Total"] = (df_rank["Valor_Total"] / total_val * 100).round(1).astype(str) + "%"
    df_rank = df_rank.rename(columns={
        "MOTIVO_DEVOLUCAO": "Motivo",
        "Quantidade": "Qtd",
        "Valor_Total_Fmt": "Valor Total",
    })
    st.dataframe(
        df_rank[["Motivo", "Qtd", "Valor Total", "% do Total"]],
        use_container_width=True,
        hide_index=True,
        height=300,
    )

# ════════════════════════════════════════════════════════
# ABA 2 — PESQUISA
# ════════════════════════════════════════════════════════
with tab_pesquisa:
    st.markdown('<div class="section-title">🔎 Pesquisa Avançada</div>', unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        s_cliente  = st.text_input("👤 Cliente", placeholder="Nome ou parte do nome...")
        s_placa    = st.text_input("🚚 Placa do Veículo", placeholder="Ex: ABC1234")
    with col_s2:
        s_nf       = st.text_input("📄 Nota Fiscal", placeholder="Número da NF...")
        s_nf_venda = st.text_input("🧾 NF de Venda", placeholder="Número da NF de venda...")
    with col_s3:
        s_pedido   = st.text_input("📦 Nº Pedido", placeholder="Número do pedido...")
        s_carreg   = st.text_input("🚛 Nº Carregamento", placeholder="Número do carregamento...")

    col_s4, col_s5 = st.columns(2)
    with col_s4:
        s_motivo   = st.text_input("❗ Motivo de Devolução", placeholder="Ex: Avaria, Excesso...")
    with col_s5:
        s_num_dev  = st.text_input("🔢 Nº Devolução", placeholder="Número da devolução...")

    btn_pesq = st.button("🔍 Pesquisar", use_container_width=False)
    st.markdown("---")

    # Aplicar pesquisa
    df_pesq = df.copy()
    filtros_aplicados = []

    def apply_search(df_in, col, val):
        if val.strip():
            return df_in[df_in[col].str.contains(val.strip(), case=False, na=False)]
        return df_in

    if s_cliente:  df_pesq = apply_search(df_pesq, "NOME_CLIENTE",     s_cliente);  filtros_aplicados.append(f"Cliente: {s_cliente}")
    if s_placa:    df_pesq = apply_search(df_pesq, "PLACA",            s_placa);    filtros_aplicados.append(f"Placa: {s_placa}")
    if s_nf:       df_pesq = apply_search(df_pesq, "NOTA_FISCAL",      s_nf);       filtros_aplicados.append(f"NF: {s_nf}")
    if s_nf_venda: df_pesq = apply_search(df_pesq, "NF_VENDA",         s_nf_venda); filtros_aplicados.append(f"NF Venda: {s_nf_venda}")
    if s_pedido:   df_pesq = apply_search(df_pesq, "NUM_PEDIDO",       s_pedido);   filtros_aplicados.append(f"Pedido: {s_pedido}")
    if s_carreg:   df_pesq = apply_search(df_pesq, "NUM_CARREGAMENTO", s_carreg);   filtros_aplicados.append(f"Carregamento: {s_carreg}")
    if s_motivo:   df_pesq = apply_search(df_pesq, "MOTIVO_DEVOLUCAO", s_motivo);   filtros_aplicados.append(f"Motivo: {s_motivo}")
    if s_num_dev:  df_pesq = apply_search(df_pesq, "NUM_DEVOLUCAO",    s_num_dev);  filtros_aplicados.append(f"Nº Devolução: {s_num_dev}")

    if filtros_aplicados:
        st.info(f"🔍 Filtros ativos: **{' | '.join(filtros_aplicados)}** — {len(df_pesq)} resultado(s)")
    else:
        st.caption(f"Exibindo todos os {len(df_pesq)} registros (aplique filtros acima para refinar)")

    # Resultado em cards se poucos, tabela se muitos
    if len(df_pesq) == 0:
        st.warning("Nenhum registro encontrado para os critérios informados.")
    elif len(df_pesq) <= 20:
        for _, row in df_pesq.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="rc-title">👤 {row['NOME_CLIENTE']}</div>
                        <div class="rc-sub">
                            📄 NF: {row['NOTA_FISCAL']} &nbsp;|&nbsp;
                            🔢 Dev: {row['NUM_DEVOLUCAO']} &nbsp;|&nbsp;
                            📦 Pedido: {row['NUM_PEDIDO']} &nbsp;|&nbsp;
                            🚛 Carg.: {row['NUM_CARREGAMENTO']}
                        </div>
                        <div class="rc-sub" style="margin-top:6px;">
                            🚚 {row['PLACA']} &nbsp;|&nbsp;
                            ❗ {row['MOTIVO_DEVOLUCAO']} &nbsp;|&nbsp;
                            👔 {row['VENDEDOR']} &nbsp;|&nbsp;
                            📅 {row['DATA_DEVOLUCAO']}
                        </div>
                        <div class="rc-sub">🏢 Filial: {row['FILIAL']} &nbsp;|&nbsp; 🏙️ {row['CIDADE']}</div>
                    </div>
                    <div class="rc-val">{fmt_brl(row['VALOR_LIQUIDO'])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        COLS_PESQ = [c for c in [
            "DATA_DEVOLUCAO", "NUM_DEVOLUCAO", "NOTA_FISCAL", "NF_VENDA",
            "NUM_PEDIDO", "NUM_CARREGAMENTO", "NOME_CLIENTE", "CIDADE",
            "MOTIVO_DEVOLUCAO", "PLACA", "VENDEDOR", "SUPERVISOR",
            "FILIAL", "VALOR_LIQUIDO",
        ] if c in df_pesq.columns]

        df_show_pesq = df_pesq[COLS_PESQ].rename(columns={
            "DATA_DEVOLUCAO": "Data", "NUM_DEVOLUCAO": "Nº Dev.",
            "NOTA_FISCAL": "NF Devolução", "NF_VENDA": "NF Venda",
            "NUM_PEDIDO": "Pedido", "NUM_CARREGAMENTO": "Carregamento",
            "NOME_CLIENTE": "Cliente", "CIDADE": "Cidade",
            "MOTIVO_DEVOLUCAO": "Motivo", "PLACA": "Placa",
            "VENDEDOR": "Vendedor", "SUPERVISOR": "Supervisor",
            "FILIAL": "Filial", "VALOR_LIQUIDO": "Valor (R$)",
        })
        st.dataframe(
            df_show_pesq.style.format({"Valor (R$)": lambda v: fmt_brl(v)}),
            use_container_width=True,
            height=500,
            hide_index=True,
        )

    # Export
    if len(df_pesq) > 0:
        st.markdown("---")
        csv_pesq = df_pesq.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button(
            "⬇️ Exportar resultado (.csv)",
            data=csv_pesq,
            file_name=f"pesquisa_devolucoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

# ════════════════════════════════════════════════════════
# ABA 3 — DADOS COMPLETOS
# ════════════════════════════════════════════════════════
with tab_dados:
    st.markdown('<div class="section-title">📑 Detalhamento Completo das Devoluções</div>', unsafe_allow_html=True)

    col_ord1, col_ord2, col_ord3 = st.columns(3)
    with col_ord1:
        sort_col = st.selectbox(
            "Ordenar por",
            options=["VALOR_LIQUIDO", "DATA_DEVOLUCAO", "NOME_CLIENTE", "FILIAL", "MOTIVO_DEVOLUCAO"],
            format_func=lambda x: {
                "VALOR_LIQUIDO": "💰 Valor",
                "DATA_DEVOLUCAO": "📅 Data",
                "NOME_CLIENTE": "👤 Cliente",
                "FILIAL": "🏢 Filial",
                "MOTIVO_DEVOLUCAO": "❗ Motivo",
            }.get(x, x),
        )
    with col_ord2:
        sort_asc = st.radio("Direção", ["↑ Crescente", "↓ Decrescente"], horizontal=True) == "↑ Crescente"
    with col_ord3:
        n_rows = st.selectbox("Linhas por página", [50, 100, 250, 500, 1000, "Todos"])

    df_sorted = df.sort_values(sort_col, ascending=sort_asc)
    if n_rows != "Todos":
        df_sorted = df_sorted.head(int(n_rows))

    SHOW_COLS = [c for c in [
        "DATA_DEVOLUCAO", "NUM_DEVOLUCAO", "NOTA_FISCAL", "NF_VENDA",
        "NUM_PEDIDO", "NUM_CARREGAMENTO", "NOME_CLIENTE", "CIDADE",
        "MOTIVO_DEVOLUCAO", "PLACA", "VENDEDOR", "SUPERVISOR",
        "FILIAL", "SEGMENTO", "VALOR_LIQUIDO",
    ] if c in df_sorted.columns]

    df_display = df_sorted[SHOW_COLS].rename(columns={
        "DATA_DEVOLUCAO": "Data", "NUM_DEVOLUCAO": "Nº Dev.",
        "NOTA_FISCAL": "NF Devolução", "NF_VENDA": "NF Venda",
        "NUM_PEDIDO": "Pedido", "NUM_CARREGAMENTO": "Carregamento",
        "NOME_CLIENTE": "Cliente", "CIDADE": "Cidade",
        "MOTIVO_DEVOLUCAO": "Motivo", "PLACA": "Placa",
        "VENDEDOR": "Vendedor", "SUPERVISOR": "Supervisor",
        "FILIAL": "Filial", "SEGMENTO": "Segmento",
        "VALOR_LIQUIDO": "Valor (R$)",
    })

    st.dataframe(
        df_display.style.format({"Valor (R$)": lambda v: fmt_brl(v)}),
        use_container_width=True,
        height=520,
        hide_index=True,
    )

    st.caption(f"Exibindo {len(df_display)} de {len(df)} registros filtrados (total bruto: {len(df_raw)})")

    st.markdown("---")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        csv_all = df[SHOW_COLS].to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button(
            "⬇️ Exportar todos os filtrados (.csv)",
            data=csv_all,
            file_name=f"devolucoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_exp2:
        # Exportar resumo por motivo
        df_res = (
            df.groupby("MOTIVO_DEVOLUCAO", as_index=False)
            .agg(Qtd=("VALOR_LIQUIDO", "count"), Total=("VALOR_LIQUIDO", "sum"))
            .sort_values("Total", ascending=False)
        )
        csv_res = df_res.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button(
            "⬇️ Exportar resumo por motivo (.csv)",
            data=csv_res,
            file_name=f"resumo_motivos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Colunas disponíveis
    with st.expander("ℹ️ Colunas detectadas na planilha"):
        st.write(f"**Colunas originais:** {list(df_raw.columns.difference(['DATA_DEVOLUCAO_DT']))}")
        if COL_MAP:
            st.write(f"**Mapeamentos aplicados:** {COL_MAP}")
        else:
            st.warning("Nenhum mapeamento de coluna foi aplicado. Verifique os nomes das colunas na planilha.")

# ════════════════════════════════════════════════════════
# ABA 4 — CONFIGURAÇÕES
# ════════════════════════════════════════════════════════
with tab_config:
    st.markdown('<div class="section-title">⚙️ Configurações do Sistema</div>', unsafe_allow_html=True)

    st.markdown("### 📋 Como configurar sua planilha")
    st.markdown("""
**Para que os dados apareçam corretamente, siga estes passos:**

1. **Abra sua planilha no Google Sheets**
2. Clique em **Arquivo → Compartilhar → Publicar na web**
3. Selecione a aba desejada e o formato **CSV (.csv)**
4. Clique em **Publicar** e copie o link gerado
5. Atualize a variável `GSHEETS_URL` no código com o novo link

> ⚠️ O link de publicação é **diferente** do link de compartilhamento normal.
    """)

    st.markdown("---")
    st.markdown("### 🔗 URL Atual da Planilha")
    st.code(GSHEETS_URL, language="text")

    st.markdown("### 📐 Nomes de Colunas Esperados")
    col_info_l, col_info_r = st.columns(2)
    with col_info_l:
        st.markdown("""
| Coluna na planilha | Dado |
|---|---|
| `DATA_DEVOLUCAO` | Data da devolução |
| `NUM_DEVOLUCAO` | Número da devolução |
| `NOTA_FISCAL` | NF de devolução |
| `NF_VENDA` | NF de venda original |
| `NUM_PEDIDO` | Número do pedido |
| `NUM_CARREGAMENTO` | Número do carregamento |
| `NOME_CLIENTE` | Nome do cliente |
        """)
    with col_info_r:
        st.markdown("""
| Coluna na planilha | Dado |
|---|---|
| `CIDADE` | Cidade do cliente |
| `MOTIVO_DEVOLUCAO` | Motivo da devolução |
| `PLACA` | Placa do veículo |
| `VENDEDOR` | Nome do vendedor |
| `SUPERVISOR` | Nome do supervisor |
| `FILIAL` | Filial / CD |
| `SEGMENTO` | Segmento de mercado |
| `VALOR_LIQUIDO` | Valor da devolução |
        """)

    st.markdown("---")
    st.markdown("### 🔄 Controle de Cache")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.info("⏱️ Os dados são atualizados automaticamente **a cada 1 minuto**.")
    with col_c2:
        if st.button("🗑️ Limpar cache e recarregar agora", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache limpo! Recarregando...")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Diagnóstico da Planilha")
    with st.expander("Ver diagnóstico completo"):
        st.write(f"**Registros carregados:** {len(df_raw)}")
        st.write(f"**Colunas encontradas:** {list(df_raw.columns.difference(['DATA_DEVOLUCAO_DT']))}")
        st.write(f"**Registros com valor > 0:** {(df_raw['VALOR_LIQUIDO'] > 0).sum()}")
        st.write(f"**Registros com data válida:** {df_raw['DATA_DEVOLUCAO_DT'].notna().sum()}")
        st.write("**Amostra dos dados (5 linhas):**")
        st.dataframe(df_raw.head(5), use_container_width=True)
