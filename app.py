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

/* ── Search cards ── */
.result-card {
    background: linear-gradient(135deg, rgba(13,31,60,0.85), rgba(15,36,68,0.85));
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 16px;
    padding: 18px 24px;
    margin-bottom: 12px;
}

/* ── Inputs ── */
.stTextInput input {
    background: rgba(10,18,40,0.8) !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0c4a6e, #1e3a8a) !important;
    color: #e0f2fe !important;
    border: 1px solid rgba(56,189,248,0.3) !important;
    border-radius: 10px !important;
}
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
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
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

with st.spinner("⏳ Carregando dados..."):
    df_raw = load_data(GSHEETS_URL)

# ── Normalize columns ─────────────────────────────────────────────────────────
df_raw.columns = [str(c).strip().upper().replace(" ", "_") for c in df_raw.columns]

VALOR_COL = next((c for c in ["VLT", "VALOR_LIQUIDO", "VALOR", "TOTAL", "VL_TOTAL", "VLF", "VL_DEVOLUCAO"] if c in df_raw.columns), "VLT")
if VALOR_COL not in df_raw.columns: df_raw[VALOR_COL] = 0.0

def parse_brl(s):
    s = str(s).replace("R$", "").strip()
    if "," in s and "." in s: s = s.replace(".", "").replace(",", ".")
    elif "," in s: s = s.replace(",", ".")
    return pd.to_numeric(s, errors="coerce")

df_raw[VALOR_COL] = df_raw[VALOR_COL].apply(parse_brl).fillna(0)

for col in df_raw.columns:
    if col != VALOR_COL:
        df_raw[col] = df_raw[col].fillna("").astype(str).str.strip()

def get_col(names):
    for n in names:
        if n in df_raw.columns: return n
    return None

COL_PLACA      = get_col(["PLACA", "PLACA_VEICULO", "VEICULO"])
COL_MOTIVO     = get_col(["MOTIVO", "MOTIVO_DEVOLUCAO", "MOTIVO_DEV"])
COL_CLIENTE    = get_col(["CLIENTE", "NOMERCA", "NOME_CLIENTE", "RAZAO_SOCIAL"])
COL_VENDEDOR   = get_col(["NOMERCA", "VENDEDOR", "NOMEFUNC_VEND"])
COL_DESTINO    = get_col(["DESTINO", "CIDADE", "MUNICIPIO", "PRACA"])
COL_NF_VENDA   = get_col(["NOTA_VENDA", "NF_VENDA", "NF_SAIDA"])
COL_CODCLI     = get_col(["CODCLI", "COD_CLI", "CLI"])
COL_DTSAIDA    = get_col(["DTSAIDA", "DATA_DEVOLUCAO", "DATA"])
COL_DTENTREGA  = get_col(["DTENTREGA", "DATA_ENTREGA"])

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
    <div class="topbar-brand"><div class="icon">📦</div><div><h1>DEVOLUÇÕES</h1><span>Sistema de Análise</span></div></div>
    <div class="topbar-right"><div class="live-badge"><span class="live-dot"></span>Ao Vivo</div><div class="topbar-time">🕐 {now_str}</div></div>
</div>
""", unsafe_allow_html=True)

tab_dash, tab_campos, tab_dados = st.tabs(["📊 Dashboard", "🗂️ Campos", "📑 Dados Completos"])

with tab_dash:
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-label">Valor Total</div><div class="kpi-value">{fmt_brl(total_val)}</div></div>
        <div class="kpi-card"><div class="kpi-label">Devoluções</div><div class="kpi-value">{total_notas}</div></div>
        <div class="kpi-card"><div class="kpi-label">Clientes</div><div class="kpi-value">{total_clientes}</div></div>
        <div class="kpi-card"><div class="kpi-label">Ticket Médio</div><div class="kpi-value">{fmt_brl(ticket_medio)}</div></div>
        <div class="kpi-card"><div class="kpi-label">Veículos</div><div class="kpi-value">{total_veiculos}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── GRÁFICO PRINCIPAL: Devoluções por Placa ────────────────────────────
    st.markdown('<div class="sec-header"><div class="bar"></div><h3>🚚 Devoluções por Placa</h3></div>', unsafe_allow_html=True)
    if COL_PLACA:
        # CORREÇÃO DO ERRO .agg() AQUI
        df_placa_all = (
            df[df[COL_PLACA].str.strip() != ""]
            .groupby(COL_PLACA)
            .agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
            .reset_index()
            .sort_values("Valor", ascending=True)
        )

        fig_placa = go.Figure(go.Bar(
            x=df_placa_all["Valor"], y=df_placa_all[COL_PLACA], orientation="h",
            text=[fmt_brl(v) for v in df_placa_all["Valor"]], textposition="outside",
            marker=dict(color="#0ea5e9")
        ))
        st.plotly_chart(plotly_layout(fig_p=fig_placa if 'fig_p' not in locals() else fig_placa), use_container_width=True)

    # Gráficos de Apoio
    c1, c2 = st.columns(2)
    with c1:
        if COL_MOTIVO:
            st.markdown('<div class="sec-header"><div class="bar"></div><h3>❗ Top Motivos</h3></div>', unsafe_allow_html=True)
            df_m = df.groupby(COL_MOTIVO).agg(Valor=(VALOR_COL, "sum")).reset_index().sort_values("Valor").tail(8)
            fig_m = px.bar(df_m, x="Valor", y=COL_MOTIVO, orientation="h", color_discrete_sequence=RED)
            st.plotly_chart(plotly_layout(fig_m), use_container_width=True)
    with c2:
        if COL_CLIENTE:
            st.markdown('<div class="sec-header"><div class="bar"></div><h3>👤 Top Clientes</h3></div>', unsafe_allow_html=True)
            df_cli = df.groupby(COL_CLIENTE).agg(Valor=(VALOR_COL, "sum")).reset_index().sort_values("Valor").tail(8)
            fig_cli = px.bar(df_cli, x="Valor", y=COL_CLIENTE, orientation="h", color_discrete_sequence=BLUE)
            st.plotly_chart(plotly_layout(fig_cli), use_container_width=True)

with tab_campos:
    st.dataframe(df, use_container_width=True)

with tab_dados:
    st.dataframe(df_raw, use_container_width=True)
