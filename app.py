import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# =========================
# CONFIG
# =========================
URL = "https://docs.google.com/spreadsheets/d/1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI/export?format=csv"

COL_PLACA = "PLACA"          # ajuste se necessário
VALOR_COL = "VALOR_LIQUIDO"  # ajuste se necessário

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip().str.upper()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

st.title("📦 Dashboard de Devoluções")

# =========================
# KPIs
# =========================
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Registros", len(df))

with col2:
    if VALOR_COL in df.columns:
        total_valor = pd.to_numeric(df[VALOR_COL], errors="coerce").sum()
        st.metric("Valor Total", f"R$ {total_valor:,.2f}")

# =========================
# TABELA
# =========================
st.subheader("📋 Dados")
st.dataframe(df, use_container_width=True)

# =========================
# AGRUPAMENTO POR PLACA (CORRIGIDO)
# =========================
st.subheader("🚚 Análise por Placa")

if COL_PLACA in df.columns and VALOR_COL in df.columns:

    df_placa_all = (
        df[df[COL_PLACA].astype(str).str.strip() != ""]
        .groupby(COL_PLACA)
        .agg(
            Valor=(VALOR_COL, "sum"),   # ✅ CORREÇÃO AQUI
            Qtd=(VALOR_COL, "count")
        )
        .reset_index()
        .sort_values("Valor", ascending=False)
    )

    st.dataframe(df_placa_all, use_container_width=True)

else:
    st.warning("Colunas de placa ou valor não encontradas")

# =========================
# DEBUG
# =========================
with st.expander("🔍 DEBUG"):
    st.write("Colunas encontradas:")
    st.write(df.columns)

    st.write("Primeiras linhas:")
    st.write(df.head())
