import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
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

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

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

.topbar-brand h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.6rem !important;
    color: #f0f9ff !important;
    margin: 0 !important;
}

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
    backdrop-filter: blur(10px);
}

.kpi-value { 
    font-family: 'Bebas Neue', sans-serif; 
    font-size: 1.7rem; 
    color: #38bdf8; 
}

.sec-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}

.sec-header .bar { 
    width: 3px; height: 24px; 
    background: #38bdf8; 
    box-shadow: 0 0 10px rgba(56,189,248,0.5);
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
        margin=dict(t=20, b=margin_b, l=10, r=10),
    )
    return fig

# ── Google Sheets URL ─────────────────────────────────────────────────────────
SHEET_ID = "1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI"
GSHEETS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return pd.read_csv(io.StringIO(resp.text))
    except Exception as e:
        st.error(f"Erro: {e}"); st.stop()

df_raw = load_data(GSHEETS_URL)
df_raw.columns = [str(c).strip().upper().replace(" ", "_") for c in df_raw.columns]

# Detecção de Colunas
VALOR_COL = next((c for c in ["VLT", "VALOR", "TOTAL", "VL_DEVOLUCAO"] if c in df_raw.columns), None)
if not VALOR_COL:
    df_raw["VLT"] = 0.0
    VALOR_COL = "VLT"

COL_PLACA = next((c for c in ["PLACA", "VEICULO"] if c in df_raw.columns), "PLACA")
COL_MOTIVO = next((c for c in ["MOTIVO", "MOTIVO_DEV"] if c in df_raw.columns), "MOTIVO")
COL_CLIENTE = next((c for c in ["CLIENTE", "RAZAO_SOCIAL"] if c in df_raw.columns), "CLIENTE")

# Parse Valores
def parse_brl(s):
    s = str(s).replace("R$", "").strip()
    if "," in s: s = s.replace(".", "").replace(",", ".")
    return pd.to_numeric(s, errors="coerce")

df_raw[VALOR_COL] = df_raw[VALOR_COL].apply(parse_brl).fillna(0)
df = df_raw.copy()

# ── Dashboard Layout ──────────────────────────────────────────────────────────
now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f'<div class="topbar"><h1>DEVOLUÇÕES</h1><span>{now_str}</span></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Dashboard", "📑 Dados"])

with tab1:
    # KPIs
    c_kpi = st.container()
    total_v = df[VALOR_COL].sum()
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-value">{fmt_brl(total_v)}</div><small>Total</small></div>
        <div class="kpi-card"><div class="kpi-value">{len(df)}</div><small>Registros</small></div>
    </div>
    """, unsafe_allow_html=True)

    # Gráfico de Placas (CORRIGIDO)
    if COL_PLACA in df.columns:
        st.markdown('<div class="sec-header"><div class="bar"></div><h3>🚚 Por Placa</h3></div>', unsafe_allow_html=True)
        df_p = df.groupby(COL_PLACA).agg(
            Valor=(VALOR_COL, "sum"), 
            Qtd=(VALOR_COL, "count")
        ).reset_index().sort_values("Valor")
        
        fig_p = px.bar(df_p, x="Valor", y=COL_PLACA, orientation="h", text_auto=True)
        st.plotly_chart(plotly_layout(fig_p), use_container_width=True)

with tab2:
    st.dataframe(df, use_container_width=True)
