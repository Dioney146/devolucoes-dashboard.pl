import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
import os
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Demonstrativo de Devoluções",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Background + CSS ──────────────────────────────────────────────────────────
UNSPLASH_BG = (
    "https://images.unsplash.com/photo-1554224155-6726b3ff858f"
    "?auto=format&fit=crop&w=1920&q=80"
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{UNSPLASH_BG}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        backdrop-filter: blur(6px) brightness(0.42);
        -webkit-backdrop-filter: blur(6px) brightness(0.42);
        z-index: 0;
    }}
    section[data-testid="stSidebar"],
    .block-container,
    header[data-testid="stHeader"] {{
        position: relative;
        z-index: 1;
    }}
    section[data-testid="stSidebar"] {{
        background: rgba(10, 30, 60, 0.82) !important;
        backdrop-filter: blur(4px);
        border-right: 1px solid rgba(255,255,255,0.12);
    }}
    section[data-testid="stSidebar"] * {{
        color: #e8eaf6 !important;
    }}
    [data-testid="stMetric"] {{
        background: rgba(13, 27, 62, 0.75);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 14px 18px;
        backdrop-filter: blur(3px);
    }}
    [data-testid="stMetricValue"] {{
        color: #90caf9 !important;
        font-size: 1.6rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: #b0bec5 !important;
    }}
    .stDataFrame {{ border-radius: 10px; overflow: hidden; }}
    h1, h2, h3, h4 {{
        color: #e3f2fd !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }}
    p, label, .stMarkdown {{ color: #cfd8dc !important; }}
    .streamlit-expanderHeader {{
        background: rgba(13, 27, 62, 0.7) !important;
        color: #e3f2fd !important;
        border-radius: 8px;
    }}
    hr {{ border-color: rgba(255,255,255,0.15); }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── URL da planilha publicada no Google Sheets ────────────────────────────────
# Para atualizar: substitua apenas esta URL pelo novo link publicado
GSHEETS_XLSX_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTxXqj7xGZh1mU2AhbOnNyLTymIPAvS-3gTx-ZqunrqFsDfODXFCxyziRUHklsLOM6STFfUB11h-tCx"
    "/pub?output=xlsx"
)

# Também pode ser sobrescrita por variável de ambiente (Streamlit Cloud Secrets)
GSHEETS_URL = os.getenv("GSHEETS_URL", GSHEETS_XLSX_URL)

# ── Carregamento dos dados ────────────────────────────────────────────────────
@st.cache_data(ttl=300)   # atualiza a cada 5 minutos
def load_data(url: str) -> pd.DataFrame:
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        if "output=csv" in url:
            df = pd.read_csv(io.StringIO(resp.text))
        else:
            df = pd.read_excel(io.BytesIO(resp.content))
        return df
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao carregar Google Sheets:\n{e}")
        st.stop()

df_raw = load_data(GSHEETS_URL)

# ── Normalização das colunas ──────────────────────────────────────────────────
df_raw.columns = [c.strip().upper() for c in df_raw.columns]
df_raw["VALOR_LIQUIDO"] = pd.to_numeric(
    df_raw.get("VALOR_LIQUIDO", pd.Series(dtype=float)), errors="coerce"
).fillna(0)

for col in ["DATA_DEVOLUCAO", "NOME_CLIENTE", "PLACA", "MOTIVO_DEVOLUCAO",
            "VENDEDOR", "SUPERVISOR", "FILIAL", "SEGMENTO", "CIDADE",
            "NOTA_FISCAL", "NUM_DEVOLUCAO", "NUM_PEDIDO"]:
    if col not in df_raw.columns:
        df_raw[col] = "N/D"
    else:
        df_raw[col] = df_raw[col].fillna("N/D").astype(str).str.strip()

# ── Sidebar — filtros ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filtros")
    st.markdown("---")

    filiais = sorted(df_raw["FILIAL"].unique())
    sel_filial = st.multiselect("Filial", filiais, default=filiais)

    segmentos = sorted(df_raw["SEGMENTO"].unique())
    sel_segmento = st.multiselect("Segmento", segmentos, default=segmentos)

    supervisores = sorted(df_raw["SUPERVISOR"].unique())
    sel_supervisor = st.multiselect("Supervisor", supervisores, default=supervisores)

    st.markdown("---")
    search = st.text_input("🔎 Buscar cliente / nota / placa")

    st.markdown("---")
    if st.button("🔄 Atualizar dados agora"):
        st.cache_data.clear()
        st.rerun()

    st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.caption("⏱ Cache de 5 min — dados sempre frescos do Google Sheets")

# ── Aplicar filtros ───────────────────────────────────────────────────────────
df = df_raw[
    df_raw["FILIAL"].isin(sel_filial) &
    df_raw["SEGMENTO"].isin(sel_segmento) &
    df_raw["SUPERVISOR"].isin(sel_supervisor)
].copy()

if search:
    s = search.strip()
    mask = (
        df["NOME_CLIENTE"].str.contains(s, case=False, na=False) |
        df["PLACA"].str.contains(s, case=False, na=False) |
        df["NOTA_FISCAL"].str.contains(s, case=False, na=False)
    )
    df = df[mask]

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.markdown("# 📋 Demonstrativo de Devoluções")
st.markdown("Análise de notas fiscais de devolução por veículo e motivo")
st.markdown("---")

# ── KPIs ──────────────────────────────────────────────────────────────────────
def fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

total_val      = df["VALOR_LIQUIDO"].sum()
total_notas    = len(df)
total_clientes = df["NOME_CLIENTE"].nunique()
ticket_medio   = total_val / total_notas if total_notas else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Valor Total Devolvido", fmt_brl(total_val))
c2.metric("📄 Nº de Devoluções",      str(total_notas))
c3.metric("👤 Clientes Únicos",       str(total_clientes))
c4.metric("📊 Ticket Médio",          fmt_brl(ticket_medio))

st.markdown("---")

# ── Gráficos ──────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2, gap="large")

# Gráfico 1 — Por Veículo
with col_left:
    st.markdown("### 🚚 Devoluções por Veículo")
    df_v = (
        df.groupby("PLACA", as_index=False)["VALOR_LIQUIDO"]
        .sum()
        .sort_values("VALOR_LIQUIDO", ascending=False)
    )
    fig_v = px.bar(
        df_v,
        x="PLACA",
        y="VALOR_LIQUIDO",
        color="VALOR_LIQUIDO",
        color_continuous_scale=["#1565c0", "#42a5f5", "#e3f2fd"],
        labels={"PLACA": "Veículo (Placa)", "VALOR_LIQUIDO": "Valor (R$)"},
        text=df_v["VALOR_LIQUIDO"].apply(lambda v: fmt_brl(v)),
    )
    fig_v.update_traces(textposition="outside", textfont_size=10)
    fig_v.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.06)",
        font_color="#e3f2fd",
        coloraxis_showscale=False,
        margin=dict(t=20, b=40),
        xaxis=dict(tickfont=dict(color="#b0bec5"), gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(tickfont=dict(color="#b0bec5"), gridcolor="rgba(255,255,255,0.08)"),
    )
    st.plotly_chart(fig_v, use_container_width=True)

# Gráfico 2 — Por Motivo
with col_right:
    st.markdown("### ❗ Devoluções por Motivo")
    df_m = (
        df.groupby("MOTIVO_DEVOLUCAO", as_index=False)["VALOR_LIQUIDO"]
        .sum()
        .sort_values("VALOR_LIQUIDO", ascending=False)
    )
    fig_m = px.bar(
        df_m,
        x="MOTIVO_DEVOLUCAO",
        y="VALOR_LIQUIDO",
        color="VALOR_LIQUIDO",
        color_continuous_scale=["#b71c1c", "#ef5350", "#ffcdd2"],
        labels={"MOTIVO_DEVOLUCAO": "Motivo", "VALOR_LIQUIDO": "Valor (R$)"},
        text=df_m["VALOR_LIQUIDO"].apply(lambda v: fmt_brl(v)),
    )
    fig_m.update_traces(textposition="outside", textfont_size=10)
    fig_m.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.06)",
        font_color="#e3f2fd",
        coloraxis_showscale=False,
        margin=dict(t=20, b=80),
        xaxis=dict(
            tickfont=dict(color="#b0bec5", size=9),
            gridcolor="rgba(255,255,255,0.08)",
            tickangle=-25,
        ),
        yaxis=dict(tickfont=dict(color="#b0bec5"), gridcolor="rgba(255,255,255,0.08)"),
    )
    st.plotly_chart(fig_m, use_container_width=True)

st.markdown("---")

# ── Tabela detalhada ──────────────────────────────────────────────────────────
st.markdown("### 📑 Detalhamento das Devoluções")

SHOW_COLS = [c for c in [
    "DATA_DEVOLUCAO", "NUM_DEVOLUCAO", "NOTA_FISCAL", "NOME_CLIENTE",
    "CIDADE", "MOTIVO_DEVOLUCAO", "PLACA", "VENDEDOR", "SUPERVISOR",
    "FILIAL", "VALOR_LIQUIDO",
] if c in df.columns]

df_show = df[SHOW_COLS].rename(columns={
    "DATA_DEVOLUCAO":   "Data",
    "NUM_DEVOLUCAO":    "Nº Devolução",
    "NOTA_FISCAL":      "Nota Fiscal",
    "NOME_CLIENTE":     "Cliente",
    "CIDADE":           "Cidade",
    "MOTIVO_DEVOLUCAO": "Motivo",
    "PLACA":            "Placa",
    "VENDEDOR":         "Vendedor",
    "SUPERVISOR":       "Supervisor",
    "FILIAL":           "Filial",
    "VALOR_LIQUIDO":    "Valor (R$)",
})

st.dataframe(
    df_show.style.format({"Valor (R$)": "R$ {:,.2f}"}),
    use_container_width=True,
    height=420,
)

st.caption(
    f"Exibindo {len(df)} de {len(df_raw)} registros  •  "
    "Fonte: Google Sheets (atualização automática a cada 5 min)"
)
