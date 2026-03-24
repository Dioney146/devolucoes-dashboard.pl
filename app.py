import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
import os
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Demonstrativo de Devoluções",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Background + CSS ─────────────────────────────────────────────────────────
UNSPLASH_BG = (
    "https://images.unsplash.com/photo-1554224155-6726b3ff858f"
    "?auto=format&fit=crop&w=1920&q=80"
)

st.markdown(
    f"""
    <style>
    /* ---- background ---- */
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
        backdrop-filter: blur(6px) brightness(0.45);
        -webkit-backdrop-filter: blur(6px) brightness(0.45);
        z-index: 0;
    }}

    /* ---- all content above blur overlay ---- */
    section[data-testid="stSidebar"],
    .block-container,
    header[data-testid="stHeader"] {{
        position: relative;
        z-index: 1;
    }}

    /* ---- sidebar ---- */
    section[data-testid="stSidebar"] {{
        background: rgba(10, 30, 60, 0.82) !important;
        backdrop-filter: blur(4px);
        border-right: 1px solid rgba(255,255,255,0.12);
    }}
    section[data-testid="stSidebar"] * {{
        color: #e8eaf6 !important;
    }}

    /* ---- cards / metric boxes ---- */
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

    /* ---- dataframe ---- */
    .stDataFrame {{ border-radius: 10px; overflow: hidden; }}

    /* ---- headings ---- */
    h1, h2, h3, h4 {{
        color: #e3f2fd !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }}
    p, label, .stMarkdown {{
        color: #cfd8dc !important;
    }}

    /* ---- expander ---- */
    .streamlit-expanderHeader {{
        background: rgba(13, 27, 62, 0.7) !important;
        color: #e3f2fd !important;
        border-radius: 8px;
    }}

    /* ---- dividers ---- */
    hr {{ border-color: rgba(255,255,255,0.15); }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Data loading ──────────────────────────────────────────────────────────────
GSHEETS_URL = os.getenv("GSHEETS_URL", "")
LOCAL_CSV   = "devolucoes_filtradas.csv"

@st.cache_data(ttl=300)
def load_data(url: str, local: str) -> pd.DataFrame:
    if url:
        try:
            export = url.replace("/edit#gid=", "/export?format=csv&gid=") \
                        .replace("/edit?usp=sharing", "/export?format=csv")
            if "/export" not in export:
                export = url.rstrip("/") + "/export?format=csv"
            resp = requests.get(export, timeout=15)
            resp.raise_for_status()
            df = pd.read_csv(io.StringIO(resp.text))
            return df
        except Exception as e:
            st.sidebar.warning(f"⚠️ Google Sheets indisponível: {e}\nUsando arquivo local.")
    if os.path.exists(local):
        return pd.read_csv(local)
    st.error("Nenhuma fonte de dados encontrada.")
    st.stop()

df_raw = load_data(GSHEETS_URL, LOCAL_CSV)

# ── Normalise ─────────────────────────────────────────────────────────────────
df_raw.columns = [c.strip().upper() for c in df_raw.columns]
df_raw["VALOR_LIQUIDO"] = pd.to_numeric(df_raw.get("VALOR_LIQUIDO", 0), errors="coerce").fillna(0)
for col in ["DATA_DEVOLUCAO", "NOME_CLIENTE", "PLACA", "MOTIVO_DEVOLUCAO",
            "VENDEDOR", "SUPERVISOR", "FILIAL", "SEGMENTO"]:
    if col not in df_raw.columns:
        df_raw[col] = "N/D"
    else:
        df_raw[col] = df_raw[col].fillna("N/D").astype(str).str.strip()

# ── Sidebar filters ───────────────────────────────────────────────────────────
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
    st.markdown("### ⚙️ Fonte de dados")
    gsheets_input = st.text_input(
        "URL do Google Sheets (opcional)",
        value=GSHEETS_URL,
        help="Cole aqui a URL de compartilhamento da planilha Google Sheets."
    )
    if st.button("🔄 Atualizar dados"):
        st.cache_data.clear()
        st.rerun()
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["FILIAL"].isin(sel_filial) &
    df_raw["SEGMENTO"].isin(sel_segmento) &
    df_raw["SUPERVISOR"].isin(sel_supervisor)
].copy()

if search:
    mask = (
        df["NOME_CLIENTE"].str.contains(search, case=False, na=False) |
        df["PLACA"].str.contains(search, case=False, na=False) |
        df.get("NOTA_FISCAL", pd.Series(dtype=str)).astype(str).str.contains(search, case=False, na=False)
    )
    df = df[mask]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 📋 Demonstrativo de Devoluções")
st.markdown("Notas fiscais de devolução — análise por veículo e motivo")
st.markdown("---")

# ── KPI cards ─────────────────────────────────────────────────────────────────
total_val  = df["VALOR_LIQUIDO"].sum()
total_notas = len(df)
total_clientes = df["NOME_CLIENTE"].nunique()
ticket_medio = total_val / total_notas if total_notas else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Valor Total Devolvido", f"R$ {total_val:,.2f}".replace(",","X").replace(".",",").replace("X","."))
c2.metric("📄 Nº de Devoluções",      f"{total_notas}")
c3.metric("👤 Clientes Únicos",       f"{total_clientes}")
c4.metric("📊 Ticket Médio",          f"R$ {ticket_medio:,.2f}".replace(",","X").replace(".",",").replace("X","."))

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2, gap="large")

# Chart 1 – Devoluções por Veículo (PLACA)
with col_left:
    st.markdown("### 🚚 Devoluções por Veículo")
    df_veiculo = (
        df.groupby("PLACA", as_index=False)["VALOR_LIQUIDO"]
        .sum()
        .sort_values("VALOR_LIQUIDO", ascending=False)
    )
    fig_v = px.bar(
        df_veiculo,
        x="PLACA",
        y="VALOR_LIQUIDO",
        color="VALOR_LIQUIDO",
        color_continuous_scale=["#1565c0", "#42a5f5", "#e3f2fd"],
        labels={"PLACA": "Veículo (Placa)", "VALOR_LIQUIDO": "Valor (R$)"},
        text=df_veiculo["VALOR_LIQUIDO"].apply(
            lambda v: f"R$ {v:,.0f}".replace(",",".")
        ),
    )
    fig_v.update_traces(textposition="outside", textfont_size=11)
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

# Chart 2 – Devoluções por Motivo
with col_right:
    st.markdown("### ❗ Devoluções por Motivo")
    df_motivo = (
        df.groupby("MOTIVO_DEVOLUCAO", as_index=False)["VALOR_LIQUIDO"]
        .sum()
        .sort_values("VALOR_LIQUIDO", ascending=False)
    )
    fig_m = px.bar(
        df_motivo,
        x="MOTIVO_DEVOLUCAO",
        y="VALOR_LIQUIDO",
        color="VALOR_LIQUIDO",
        color_continuous_scale=["#b71c1c", "#ef5350", "#ffcdd2"],
        labels={"MOTIVO_DEVOLUCAO": "Motivo", "VALOR_LIQUIDO": "Valor (R$)"},
        text=df_motivo["VALOR_LIQUIDO"].apply(
            lambda v: f"R$ {v:,.0f}".replace(",",".")
        ),
    )
    fig_m.update_traces(textposition="outside", textfont_size=11)
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

# ── Data table ────────────────────────────────────────────────────────────────
st.markdown("### 📑 Detalhamento das Devoluções")

SHOW_COLS = [c for c in [
    "DATA_DEVOLUCAO","NUM_DEVOLUCAO","NOTA_FISCAL","NOME_CLIENTE",
    "CIDADE","MOTIVO_DEVOLUCAO","PLACA","VENDEDOR","SUPERVISOR",
    "FILIAL","VALOR_LIQUIDO"
] if c in df.columns]

df_show = df[SHOW_COLS].rename(columns={
    "DATA_DEVOLUCAO":    "Data",
    "NUM_DEVOLUCAO":     "Nº Devolução",
    "NOTA_FISCAL":       "Nota Fiscal",
    "NOME_CLIENTE":      "Cliente",
    "CIDADE":            "Cidade",
    "MOTIVO_DEVOLUCAO":  "Motivo",
    "PLACA":             "Placa",
    "VENDEDOR":          "Vendedor",
    "SUPERVISOR":        "Supervisor",
    "FILIAL":            "Filial",
    "VALOR_LIQUIDO":     "Valor (R$)",
})

st.dataframe(
    df_show.style.format({"Valor (R$)": "R$ {:,.2f}"}),
    use_container_width=True,
    height=420,
)

st.caption(f"Exibindo {len(df)} de {len(df_raw)} registros  •  Dados atualizados a cada 5 min quando conectado ao Google Sheets")
