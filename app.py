import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
import os
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Reentregas Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
    background: #0a0f1e !important;
    font-family: 'DM Sans', sans-serif;
    color: #e2e8f0;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1630 0%, #0a0f1e 100%) !important;
    border-right: 1px solid rgba(99,179,237,0.15);
}
section[data-testid="stSidebar"] * { color: #cbd5e0 !important; }
section[data-testid="stSidebar"] label { color: #90cdf4 !important; font-weight: 600; }
.sidebar-logo {
    background: linear-gradient(135deg, #1a365d, #2a4a7f);
    border-bottom: 1px solid rgba(99,179,237,0.2);
    padding: 20px 16px 16px;
    margin: -1rem -1rem 1rem;
    text-align: center;
}
.sidebar-logo h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.1rem !important; font-weight: 800 !important;
    color: #90cdf4 !important; letter-spacing: 0.05em; margin: 0 !important;
}
.sidebar-logo p { font-size: 0.72rem; color: #718096 !important; margin: 4px 0 0; }
.main-header {
    background: linear-gradient(135deg, #1a365d 0%, #153e75 50%, #1a4a8a 100%);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 16px; padding: 28px 36px; margin-bottom: 24px;
    display: flex; align-items: center; justify-content: space-between;
    position: relative; overflow: hidden;
}
.main-header::before {
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.main-header h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.9rem !important; font-weight: 800 !important;
    color: #e2e8f0 !important; margin: 0 !important; letter-spacing: -0.01em;
    text-shadow: 0 2px 20px rgba(0,0,0,0.4) !important;
}
.main-header p { color: #90cdf4 !important; margin: 6px 0 0 !important; font-size: 0.9rem; }
.header-badge {
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 50px; padding: 8px 18px;
    font-size: 0.8rem; color: #90cdf4 !important; white-space: nowrap;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #141e38 0%, #1a2848 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 14px; padding: 20px 22px !important;
    transition: border-color 0.2s, transform 0.2s;
}
[data-testid="stMetric"]:hover { border-color: rgba(99,179,237,0.5); transform: translateY(-2px); }
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.55rem !important; font-weight: 700 !important; color: #90cdf4 !important;
}
[data-testid="stMetricLabel"] { color: #718096 !important; font-size: 0.82rem !important; }
.stTabs [data-baseweb="tab-list"] {
    background: #0d1630; border-radius: 12px; padding: 4px; gap: 4px;
    border: 1px solid rgba(99,179,237,0.15);
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 9px;
    color: #718096 !important; font-weight: 600; font-size: 0.88rem;
    padding: 10px 20px; transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a365d, #2b6cb0) !important;
    color: #e2e8f0 !important; box-shadow: 0 2px 12px rgba(43,108,176,0.4);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px; }
.stDataFrame {
    border-radius: 12px; overflow: hidden;
    border: 1px solid rgba(99,179,237,0.15) !important;
}
.section-title {
    font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700;
    color: #e2e8f0; border-left: 4px solid #4299e1;
    padding-left: 12px; margin-bottom: 16px;
}
.result-card {
    background: linear-gradient(135deg, #141e38, #1a2848);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: rgba(99,179,237,0.5); }
.rc-title { font-weight: 700; color: #90cdf4; font-size: 1rem; }
.rc-sub { color: #718096; font-size: 0.82rem; margin-top: 4px; }
.rc-val { font-family: 'Syne', sans-serif; font-weight: 700; color: #68d391; font-size: 1.1rem; }
.stButton > button {
    background: linear-gradient(135deg, #1a365d, #2b6cb0);
    color: #e2e8f0; border: 1px solid rgba(99,179,237,0.3);
    border-radius: 9px; font-weight: 600; padding: 8px 20px; transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2b6cb0, #3182ce);
    transform: translateY(-1px);
}
.stTextInput input {
    background: #0d1630 !important;
    border-color: rgba(99,179,237,0.25) !important;
    color: #e2e8f0 !important; border-radius: 8px !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: #1a365d !important; color: #90cdf4 !important;
}
.streamlit-expanderHeader {
    background: #141e38 !important; border-radius: 10px !important;
    color: #90cdf4 !important; font-weight: 600 !important;
}
hr { border-color: rgba(99,179,237,0.12) !important; margin: 18px 0 !important; }
.stCaption, small { color: #4a5568 !important; font-size: 0.78rem !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: #2b6cb0; border-radius: 3px; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def fmt_kg(v):
    try:
        return f"{float(v):,.3f} kg".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0 kg"

def plotly_layout(fig, margin_b=40):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="#cbd5e0", family="DM Sans"),
        coloraxis_showscale=False,
        margin=dict(t=30, b=margin_b, l=10, r=10),
        xaxis=dict(tickfont=dict(color="#718096", size=10),
                   gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(tickfont=dict(color="#718096", size=10),
                   gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(bgcolor="rgba(13,22,48,0.8)",
                    bordercolor="rgba(99,179,237,0.2)", borderwidth=1),
    )
    return fig

BLUE_SCALE  = ["#1a365d", "#2b6cb0", "#4299e1", "#90cdf4"]
RED_SCALE   = ["#742a2a", "#c53030", "#fc8181", "#fed7d7"]
GREEN_SCALE = ["#1c4532", "#276749", "#38a169", "#9ae6b4"]

# ── URL da planilha ────────────────────────────────────────────────────────────
# IMPORTANTE: Use o link gerado em Arquivo -> Publicar na web -> CSV
# O link abaixo tenta carregar diretamente pelo export do Google Sheets
SHEET_ID = "1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI"
GSHEETS_DEFAULT = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    "/export?format=csv&gid=0"
)
GSHEETS_URL = os.getenv("GSHEETS_URL", GSHEETS_DEFAULT)

# ── Carregamento ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_data(url: str) -> pd.DataFrame:
    try:
        resp = requests.get(url, timeout=30,
                            headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}\n\nVerifique se a planilha está publicada como CSV.")
        st.stop()

with st.spinner("Carregando dados da planilha..."):
    df_raw = load_data(GSHEETS_URL)

# ── Normalização ──────────────────────────────────────────────────────────────
# Limpa nomes de colunas
df_raw.columns = [str(c).strip().upper().replace(" ", "_") for c in df_raw.columns]

# Mapeamento dos nomes reais da aba REENTREGAS para nomes internos
RENAME = {
    "NUMNOTA":           "NOTA_FISCAL",
    "DTFAT":             "DATA_FAT",
    "SERIE":             "SERIE",
    "ESPECIE":           "ESPECIE",
    "DTSAIDA":           "DATA_SAIDA",
    "VLTOTGER":          "VALOR_TOTAL",
    "TOTPESO":           "PESO_TOTAL",
    "NUMTRANSVENDA":     "NUM_TRANSACAO",
    "NUMCARANTERIOR":    "NUM_CARREGAMENTO",
    "PLACAANT":          "PLACA",
    "COD_MOT_ANTERIOR":  "COD_MOTORISTA",
    "NOME_MOT_ANTERIOR": "MOTORISTA",
    "COD_AJU_ANTERIOR":  "COD_AJUDANTE",
    "NOME_AJU_ANTERIOR": "AJUDANTE",
}
rename_apply = {k: v for k, v in RENAME.items() if k in df_raw.columns}
df_raw = df_raw.rename(columns=rename_apply)

# Garante existência de todas as colunas esperadas
EXPECTED = [
    "NOTA_FISCAL", "DATA_FAT", "SERIE", "ESPECIE", "DATA_SAIDA",
    "VALOR_TOTAL", "PESO_TOTAL", "NUM_TRANSACAO", "NUM_CARREGAMENTO",
    "PLACA", "COD_MOTORISTA", "MOTORISTA", "COD_AJUDANTE", "AJUDANTE",
]
for col in EXPECTED:
    if col not in df_raw.columns:
        df_raw[col] = "N/D"
    else:
        df_raw[col] = df_raw[col].fillna("N/D").astype(str).str.strip()

# Numéricos — suporta ponto ou vírgula como decimal
def parse_num(s):
    return pd.to_numeric(
        s.astype(str).str.replace("R$","",regex=False)
         .str.replace(" ","",regex=False)
         .str.replace(".","",regex=False)
         .str.replace(",",".",regex=False),
        errors="coerce"
    ).fillna(0)

df_raw["VALOR_TOTAL"] = parse_num(df_raw["VALOR_TOTAL"])
df_raw["PESO_TOTAL"]  = parse_num(df_raw["PESO_TOTAL"])

# Datas
for dc in ["DATA_FAT", "DATA_SAIDA"]:
    df_raw[dc + "_DT"] = pd.to_datetime(df_raw[dc], dayfirst=True, errors="coerce")

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>🚚 REENTREGAS</h2>
        <p>8452 · Dashboard de Devoluções</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Filtros")

    placas = sorted([x for x in df_raw["PLACA"].unique() if x not in ("N/D","nan","")])
    sel_placa = st.multiselect("🚚 Placa", placas, default=placas)

    especies = sorted([x for x in df_raw["ESPECIE"].unique() if x not in ("N/D","nan","")])
    sel_especie = st.multiselect("📋 Espécie", especies, default=especies) if especies else []

    motoristas = sorted([x for x in df_raw["MOTORISTA"].unique() if x not in ("N/D","nan","")])
    sel_motor = st.multiselect("🧑‍✈️ Motorista", motoristas, default=motoristas) if motoristas else []

    st.markdown("---")
    st.markdown("### 📅 Período (Data Saída)")
    datas_v = df_raw["DATA_SAIDA_DT"].dropna()
    filtrar_data = False
    if len(datas_v) > 0:
        dt_min = datas_v.min().date()
        dt_max = datas_v.max().date()
        dt_ini = st.date_input("De",  value=dt_min, min_value=dt_min, max_value=dt_max)
        dt_fim = st.date_input("Até", value=dt_max, min_value=dt_min, max_value=dt_max)
        filtrar_data = True
    else:
        st.caption("Sem datas válidas para filtrar")

    st.markdown("---")
    cb1, cb2 = st.columns(2)
    with cb1:
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
            st.rerun()
    with cb2:
        if st.button("🗑️ Limpar"):
            st.rerun()

    st.markdown("---")
    st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    st.caption(f"📊 {len(df_raw)} registros")
    st.caption("♻️ Cache: 1 min")

# ── Filtros ───────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_placa:    df = df[df["PLACA"].isin(sel_placa)]
if sel_especie:  df = df[df["ESPECIE"].isin(sel_especie)]
if sel_motor:    df = df[df["MOTORISTA"].isin(sel_motor)]
if filtrar_data and len(datas_v) > 0:
    mask = df["DATA_SAIDA_DT"].between(
        pd.Timestamp(dt_ini), pd.Timestamp(dt_fim), inclusive="both"
    )
    df = df[mask | df["DATA_SAIDA_DT"].isna()]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
    <div>
        <h1>📦 Demonstrativo de Reentregas</h1>
        <p>8452 · Análise completa de devoluções e reentregas · Dados em tempo real</p>
    </div>
    <div class="header-badge">🟢 Ao Vivo &nbsp;|&nbsp; {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_val      = df["VALOR_TOTAL"].sum()
total_notas    = len(df)
total_veiculos = df["PLACA"].nunique()
total_peso     = df["PESO_TOTAL"].sum()
ticket_medio   = total_val / total_notas if total_notas else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Valor Total",   fmt_brl(total_val))
k2.metric("📄 Nº de Notas",  f"{total_notas:,}".replace(",","."))
k3.metric("🚚 Veículos",     str(total_veiculos))
k4.metric("⚖️ Peso Total",   fmt_kg(total_peso))
k5.metric("📊 Ticket Médio", fmt_brl(ticket_medio))

st.markdown("---")

# ── ABAS ──────────────────────────────────────────────────────────────────────
tab_dash, tab_pesquisa, tab_dados, tab_config = st.tabs([
    "📊  Dashboard",
    "🔎  Pesquisa",
    "📑  Dados Completos",
    "⚙️  Configurações",
])

# ════════════════════════════════════════
# ABA 1 — DASHBOARD
# ════════════════════════════════════════
with tab_dash:
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown('<div class="section-title">🚚 Valor Total por Veículo (Top 15)</div>', unsafe_allow_html=True)
        df_v = (df[df["PLACA"]!="N/D"]
                .groupby("PLACA", as_index=False)["VALOR_TOTAL"].sum()
                .sort_values("VALOR_TOTAL", ascending=False).head(15))
        if not df_v.empty:
            fig = px.bar(df_v, x="PLACA", y="VALOR_TOTAL",
                         color="VALOR_TOTAL", color_continuous_scale=BLUE_SCALE,
                         text=df_v["VALOR_TOTAL"].apply(fmt_brl),
                         labels={"PLACA":"Veículo","VALOR_TOTAL":"Valor (R$)"})
            fig.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig), use_container_width=True)
        else:
            st.info("Sem dados de veículo")

    with col_r:
        st.markdown('<div class="section-title">📄 Qtd de Notas por Veículo</div>', unsafe_allow_html=True)
        df_q = (df[df["PLACA"]!="N/D"]
                .groupby("PLACA", as_index=False).size()
                .rename(columns={"size":"QTD"})
                .sort_values("QTD", ascending=False).head(15))
        if not df_q.empty:
            fig = px.bar(df_q, x="PLACA", y="QTD",
                         color="QTD", color_continuous_scale=RED_SCALE, text="QTD",
                         labels={"PLACA":"Veículo","QTD":"Qtd Notas"})
            fig.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig), use_container_width=True)
        else:
            st.info("Sem dados")

    col_l2, col_r2 = st.columns(2, gap="large")

    with col_l2:
        st.markdown('<div class="section-title">📈 Evolução por Data de Saída</div>', unsafe_allow_html=True)
        df_t = df[df["DATA_SAIDA_DT"].notna()].copy()
        if not df_t.empty:
            df_t["DIA"] = df_t["DATA_SAIDA_DT"].dt.date.astype(str)
            df_dia = df_t.groupby("DIA",as_index=False)["VALOR_TOTAL"].sum().sort_values("DIA")
            fig = px.area(df_dia, x="DIA", y="VALOR_TOTAL",
                          labels={"DIA":"Data","VALOR_TOTAL":"Valor (R$)"},
                          color_discrete_sequence=["#4299e1"])
            fig.update_traces(fill="tozeroy", fillcolor="rgba(66,153,225,0.15)",
                              line=dict(color="#4299e1",width=2))
            st.plotly_chart(plotly_layout(fig), use_container_width=True)
        else:
            st.info("Sem datas válidas")

    with col_r2:
        st.markdown('<div class="section-title">⚖️ Peso Total por Veículo</div>', unsafe_allow_html=True)
        df_p = (df[df["PLACA"]!="N/D"]
                .groupby("PLACA",as_index=False)["PESO_TOTAL"].sum()
                .sort_values("PESO_TOTAL",ascending=False).head(15))
        if not df_p.empty:
            fig = px.bar(df_p, x="PLACA", y="PESO_TOTAL",
                         color="PESO_TOTAL", color_continuous_scale=GREEN_SCALE,
                         text=df_p["PESO_TOTAL"].apply(lambda v: f"{v:,.1f}".replace(",","X").replace(".",",").replace("X",".")),
                         labels={"PLACA":"Veículo","PESO_TOTAL":"Peso (kg)"})
            fig.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig), use_container_width=True)
        else:
            st.info("Sem dados de peso")

    col_l3, col_r3 = st.columns(2, gap="large")

    with col_l3:
        st.markdown('<div class="section-title">🧑‍✈️ Valor por Motorista (Top 10)</div>', unsafe_allow_html=True)
        df_m = (df[~df["MOTORISTA"].isin(["N/D","nan",""])]
                .groupby("MOTORISTA",as_index=False)["VALOR_TOTAL"].sum()
                .sort_values("VALOR_TOTAL",ascending=True).tail(10))
        if not df_m.empty:
            fig = px.bar(df_m, x="VALOR_TOTAL", y="MOTORISTA", orientation="h",
                         color="VALOR_TOTAL", color_continuous_scale=BLUE_SCALE,
                         text=df_m["VALOR_TOTAL"].apply(fmt_brl),
                         labels={"MOTORISTA":"","VALOR_TOTAL":"Valor (R$)"})
            fig.update_traces(textposition="outside", textfont_size=9, cliponaxis=False)
            st.plotly_chart(plotly_layout(fig), use_container_width=True)
        else:
            st.info("Sem dados de motorista")

    with col_r3:
        st.markdown('<div class="section-title">📋 Distribuição por Espécie</div>', unsafe_allow_html=True)
        df_e = (df[~df["ESPECIE"].isin(["N/D","nan",""])]
                .groupby("ESPECIE",as_index=False)["VALOR_TOTAL"].sum()
                .sort_values("VALOR_TOTAL",ascending=False))
        if not df_e.empty:
            fig = px.pie(df_e, names="ESPECIE", values="VALOR_TOTAL",
                         color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.45)
            fig.update_traces(textfont_size=11,
                              marker=dict(line=dict(color="#0a0f1e",width=2)))
            st.plotly_chart(plotly_layout(fig), use_container_width=True)
        else:
            st.info("Sem dados de espécie")

    st.markdown("---")
    st.markdown('<div class="section-title">🏆 Ranking por Veículo</div>', unsafe_allow_html=True)
    df_rank = (
        df[df["PLACA"]!="N/D"]
        .groupby("PLACA",as_index=False)
        .agg(Qtd=("VALOR_TOTAL","count"), Valor=("VALOR_TOTAL","sum"), Peso=("PESO_TOTAL","sum"))
        .sort_values("Valor",ascending=False)
    )
    df_rank["Valor_Fmt"] = df_rank["Valor"].apply(fmt_brl)
    df_rank["Peso_Fmt"]  = df_rank["Peso"].apply(fmt_kg)
    pct = (df_rank["Valor"]/total_val*100).round(1).astype(str)+"%"  if total_val>0 else "0%"
    df_rank["% Total"] = pct
    st.dataframe(
        df_rank[["PLACA","Qtd","Valor_Fmt","Peso_Fmt","% Total"]]
        .rename(columns={"PLACA":"Placa","Qtd":"Qtd Notas","Valor_Fmt":"Valor Total","Peso_Fmt":"Peso Total"}),
        use_container_width=True, hide_index=True, height=300,
    )

# ════════════════════════════════════════
# ABA 2 — PESQUISA
# ════════════════════════════════════════
with tab_pesquisa:
    st.markdown('<div class="section-title">🔎 Pesquisa Avançada</div>', unsafe_allow_html=True)

    cs1, cs2, cs3 = st.columns(3)
    with cs1:
        s_nota   = st.text_input("📄 Nº Nota Fiscal",        placeholder="Ex: 380634")
        s_transac= st.text_input("🔢 Nº Transação de Venda", placeholder="Ex: 575740046")
    with cs2:
        s_placa  = st.text_input("🚚 Placa do Veículo",      placeholder="Ex: QZV6H85")
        s_carreg = st.text_input("🚛 Nº Carregamento",       placeholder="Número do carregamento")
    with cs3:
        s_motor  = st.text_input("🧑‍✈️ Motorista",           placeholder="Nome do motorista")
        s_ajud   = st.text_input("🙋 Ajudante",              placeholder="Nome do ajudante")

    st.markdown("---")

    def srch(df_in, col, val):
        if val.strip():
            return df_in[df_in[col].astype(str).str.contains(val.strip(), case=False, na=False)]
        return df_in

    dp = df.copy()
    filtros = []
    if s_nota:    dp = srch(dp,"NOTA_FISCAL",    s_nota);    filtros.append(f"NF: {s_nota}")
    if s_transac: dp = srch(dp,"NUM_TRANSACAO",  s_transac); filtros.append(f"Transação: {s_transac}")
    if s_placa:   dp = srch(dp,"PLACA",          s_placa);   filtros.append(f"Placa: {s_placa}")
    if s_carreg:  dp = srch(dp,"NUM_CARREGAMENTO",s_carreg); filtros.append(f"Carregamento: {s_carreg}")
    if s_motor:   dp = srch(dp,"MOTORISTA",      s_motor);   filtros.append(f"Motorista: {s_motor}")
    if s_ajud:    dp = srch(dp,"AJUDANTE",       s_ajud);    filtros.append(f"Ajudante: {s_ajud}")

    if filtros:
        st.info(f"🔍 **{' | '.join(filtros)}** — {len(dp)} resultado(s)")
    else:
        st.caption(f"Exibindo todos os {len(dp)} registros. Use os campos acima para filtrar.")

    if len(dp) == 0:
        st.warning("Nenhum registro encontrado.")
    elif len(dp) <= 30:
        for _, row in dp.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div class="rc-title">📄 NF: {row['NOTA_FISCAL']} &nbsp;·&nbsp; 🚚 Placa: {row['PLACA']}</div>
                        <div class="rc-sub">
                            📅 Fat: {row['DATA_FAT']} &nbsp;|&nbsp; 🚛 Saída: {row['DATA_SAIDA']}
                            &nbsp;|&nbsp; 📋 Série: {row['SERIE']} &nbsp;|&nbsp; Espécie: {row['ESPECIE']}
                        </div>
                        <div class="rc-sub" style="margin-top:6px;">
                            🔢 Transação: {row['NUM_TRANSACAO']} &nbsp;|&nbsp; 🚛 Carregamento: {row['NUM_CARREGAMENTO']}
                        </div>
                        <div class="rc-sub">
                            🧑‍✈️ Motorista: {row['MOTORISTA']} &nbsp;|&nbsp; 🙋 Ajudante: {row['AJUDANTE']}
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div class="rc-val">{fmt_brl(row['VALOR_TOTAL'])}</div>
                        <div class="rc-sub">{fmt_kg(row['PESO_TOTAL'])}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        COLS_P = [c for c in ["NOTA_FISCAL","DATA_FAT","DATA_SAIDA","SERIE","ESPECIE",
                               "NUM_TRANSACAO","NUM_CARREGAMENTO","PLACA",
                               "MOTORISTA","AJUDANTE","VALOR_TOTAL","PESO_TOTAL"] if c in dp.columns]
        st.dataframe(
            dp[COLS_P].rename(columns={
                "NOTA_FISCAL":"Nota Fiscal","DATA_FAT":"Dt Fat","DATA_SAIDA":"Dt Saída",
                "SERIE":"Série","ESPECIE":"Espécie","NUM_TRANSACAO":"Transação",
                "NUM_CARREGAMENTO":"Carregamento","PLACA":"Placa",
                "MOTORISTA":"Motorista","AJUDANTE":"Ajudante",
                "VALOR_TOTAL":"Valor (R$)","PESO_TOTAL":"Peso (kg)",
            }).style.format({"Valor (R$)":lambda v:fmt_brl(v),"Peso (kg)":lambda v:fmt_kg(v)}),
            use_container_width=True, height=500, hide_index=True,
        )

    if len(dp) > 0:
        st.markdown("---")
        csv_p = dp.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar resultado (.csv)", data=csv_p,
                           file_name=f"pesquisa_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                           mime="text/csv")

# ════════════════════════════════════════
# ABA 3 — DADOS COMPLETOS
# ════════════════════════════════════════
with tab_dados:
    st.markdown('<div class="section-title">📑 Todos os Registros</div>', unsafe_allow_html=True)

    co1, co2, co3 = st.columns(3)
    with co1:
        sort_col = st.selectbox("Ordenar por", ["VALOR_TOTAL","DATA_SAIDA","NOTA_FISCAL","PLACA","MOTORISTA"],
                                format_func=lambda x: {"VALOR_TOTAL":"💰 Valor","DATA_SAIDA":"📅 Data Saída",
                                                        "NOTA_FISCAL":"📄 NF","PLACA":"🚚 Placa",
                                                        "MOTORISTA":"🧑‍✈️ Motorista"}.get(x,x))
    with co2:
        asc = st.radio("Direção", ["↓ Decrescente","↑ Crescente"], horizontal=True) == "↑ Crescente"
    with co3:
        n_rows = st.selectbox("Linhas", [50,100,250,500,1000,"Todos"])

    df_s = df.sort_values(sort_col, ascending=asc)
    if n_rows != "Todos": df_s = df_s.head(int(n_rows))

    ALL_COLS = [c for c in ["NOTA_FISCAL","DATA_FAT","DATA_SAIDA","SERIE","ESPECIE",
                             "NUM_TRANSACAO","NUM_CARREGAMENTO","PLACA",
                             "COD_MOTORISTA","MOTORISTA","COD_AJUDANTE","AJUDANTE",
                             "VALOR_TOTAL","PESO_TOTAL"] if c in df_s.columns]
    RENAME_D = {"NOTA_FISCAL":"Nota Fiscal","DATA_FAT":"Dt Faturamento","DATA_SAIDA":"Dt Saída",
                "SERIE":"Série","ESPECIE":"Espécie","NUM_TRANSACAO":"Transação Venda",
                "NUM_CARREGAMENTO":"Carregamento","PLACA":"Placa","COD_MOTORISTA":"Cód Motor.",
                "MOTORISTA":"Motorista","COD_AJUDANTE":"Cód Ajud.","AJUDANTE":"Ajudante",
                "VALOR_TOTAL":"Valor (R$)","PESO_TOTAL":"Peso (kg)"}

    st.dataframe(
        df_s[ALL_COLS].rename(columns=RENAME_D)
        .style.format({"Valor (R$)":lambda v:fmt_brl(v),"Peso (kg)":lambda v:fmt_kg(v)}),
        use_container_width=True, height=520, hide_index=True,
    )
    st.caption(f"Exibindo {len(df_s)} de {len(df)} filtrados (total bruto: {len(df_raw)})")

    st.markdown("---")
    ce1, ce2 = st.columns(2)
    with ce1:
        csv_all = df[ALL_COLS].to_csv(index=False,sep=";",decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar todos filtrados (.csv)", data=csv_all,
                           file_name=f"reentregas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                           mime="text/csv", use_container_width=True)
    with ce2:
        df_rp = (df.groupby("PLACA",as_index=False)
                 .agg(Qtd=("VALOR_TOTAL","count"),Total=("VALOR_TOTAL","sum"),Peso=("PESO_TOTAL","sum"))
                 .sort_values("Total",ascending=False))
        csv_rp = df_rp.to_csv(index=False,sep=";",decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar resumo por placa (.csv)", data=csv_rp,
                           file_name=f"resumo_placas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                           mime="text/csv", use_container_width=True)

    with st.expander("🔍 Diagnóstico — colunas detectadas"):
        raw_cols = [c for c in df_raw.columns if not c.endswith("_DT")]
        st.write(f"**Colunas na planilha:** {raw_cols}")
        st.write(f"**Mapeamentos aplicados:** {rename_apply}")

# ════════════════════════════════════════
# ABA 4 — CONFIGURAÇÕES
# ════════════════════════════════════════
with tab_config:
    st.markdown('<div class="section-title">⚙️ Configurações e Ajuda</div>', unsafe_allow_html=True)

    st.markdown("### 🔗 URL Atual")
    st.code(GSHEETS_URL, language="text")

    st.markdown("### 📋 Como publicar a planilha corretamente")
    st.markdown("""
**Passo a passo obrigatório:**

1. Abra a planilha **8452 - DEVOLUCAO 2026** no Google Sheets
2. Menu **Arquivo → Compartilhar → Publicar na web**
3. Selecione a aba **REENTREGAS**
4. Selecione formato **Valores separados por vírgula (.csv)**
5. Clique em **Publicar** e confirme
6. **Copie o link gerado** — ele termina com `...pub?gid=XXXXX&single=true&output=csv`
7. No `app.py`, substitua `GSHEETS_DEFAULT` pelo link copiado

> ⚠️ O link `/edit?usp=sharing` **não funciona**. Use apenas o link de publicação.
    """)

    st.markdown("### 📐 Mapeamento de Colunas (aba REENTREGAS)")
    ca, cb = st.columns(2)
    with ca:
        st.markdown("""
| Coluna na planilha | Campo no Dashboard |
|---|---|
| `NUMNOTA` | Nota Fiscal |
| `DTFAT` | Data Faturamento |
| `DTSAIDA` | Data Saída |
| `VLTOTGER` | Valor Total |
| `TOTPESO` | Peso Total |
| `NUMTRANSVENDA` | Transação de Venda |
        """)
    with cb:
        st.markdown("""
| Coluna na planilha | Campo no Dashboard |
|---|---|
| `NUMCARANTERIOR` | Nº Carregamento |
| `PLACAANT` | Placa do Veículo |
| `NOME MOT ANTERIOR` | Motorista |
| `COD MOT ANTERIOR` | Código Motorista |
| `NOME AJU ANTERIOR` | Ajudante |
| `COD AJU ANTERIOR` | Código Ajudante |
        """)

    st.markdown("---")
    st.markdown("### 🔄 Cache")
    c_c1, c_c2 = st.columns(2)
    with c_c1:
        st.info("⏱️ Dados atualizados automaticamente **a cada 1 minuto**.")
    with c_c2:
        if st.button("🗑️ Limpar cache agora", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache limpo!")
            st.rerun()

    with st.expander("🔎 Amostra dos dados brutos (primeiras 10 linhas)"):
        st.dataframe(df_raw.drop(columns=[c for c in df_raw.columns if c.endswith("_DT")], errors="ignore").head(10),
                     use_container_width=True)
