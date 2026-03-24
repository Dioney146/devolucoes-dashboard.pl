import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Dashboard Devoluções", layout="wide")

# =========================
# 🔗 URL DA PLANILHA
# =========================
url = "https://docs.google.com/spreadsheets/d/1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI/export?format=csv"

# =========================
# 🔧 FUNÇÃO NORMALIZAR COLUNAS
# =========================
def normalize_col(c):
    c = str(c).strip().upper()
    c = re.sub(r"[^\w\s]", "", c)  # remove símbolos
    c = c.replace(" ", "_")
    return c

# =========================
# 🔄 CARREGAR DADOS
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(url)
    df.columns = [normalize_col(c) for c in df.columns]
    return df

# =========================
# 🧠 MAPEAMENTO DE COLUNAS
# =========================
def map_columns(df):
    col_aliases = {

        "DATA_DEVOLUCAO": ["DATA_DEVOLUCAO", "DATA", "DATA_DEV"],

        "NUM_DEVOLUCAO": ["NUM_DEVOLUCAO", "N_DEV", "DEV"],

        "NOTA_FISCAL": ["NOTA_FISCAL", "NF_DEV", "NF"],

        "NF_VENDA": ["NF_VENDA", "NFVENDA"],

        "NUM_PEDIDO": ["NUM_PEDIDO", "PEDIDO"],

        "NUM_CARREGAMENTO": ["NUM_CARREGAMENTO", "CARREGAMENTO"],

        "VALOR_LIQUIDO": ["VALOR", "TOTAL", "VLT"],

        "NOME_CLIENTE": ["CLIENTE", "NOME"],

    }

    df_final = pd.DataFrame()

    for col_final, aliases in col_aliases.items():
        found = None
        for alias in aliases:
            if alias in df.columns:
                found = alias
                break

        if found:
            df_final[col_final] = df[found]
        else:
            df_final[col_final] = "N/D"

    return df_final

# =========================
# 🚨 TRATAMENTO DE ERRO
# =========================
try:
    df_raw = load_data()
    df = map_columns(df_raw)

except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

# =========================
# 📊 DASHBOARD
# =========================
st.title("📦 Dashboard de Devoluções")

# KPI
col1, col2 = st.columns(2)

with col1:
    total = len(df)
    st.metric("Total de Devoluções", total)

with col2:
    if "VALOR_LIQUIDO" in df.columns:
        valor_total = pd.to_numeric(df["VALOR_LIQUIDO"], errors="coerce").sum()
        st.metric("💰 Valor Total", f"R$ {valor_total:,.2f}")

# =========================
# 📋 TABELA
# =========================
st.subheader("📋 Dados")

df_display = df.rename(columns={
    "DATA_DEVOLUCAO": "Data",
    "NUM_DEVOLUCAO": "Nº Dev.",
    "NOTA_FISCAL": "NF Dev.",
    "NF_VENDA": "NF Venda",
    "NUM_PEDIDO": "Pedido",
    "NUM_CARREGAMENTO": "Carregamento",
})

st.dataframe(df_display, use_container_width=True)

# =========================
# 🧪 DEBUG (OPCIONAL)
# =========================
with st.expander("🔍 DEBUG"):
    st.write("Colunas encontradas:")
    st.write(df_raw.columns)

    st.write("Primeiras linhas:")
    st.write(df_raw.head())
