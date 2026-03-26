import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Dashboard de Devoluções", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1600&q=80");
    background-size: cover; background-position: center; background-attachment: fixed;
}
[data-testid="stAppViewContainer"]::before {
    content: ""; position: fixed; inset: 0;
    backdrop-filter: blur(6px) brightness(0.3); z-index: 0;
}
[data-testid="stAppViewContainer"] > * { position: relative; z-index: 1; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background-color: rgba(10,12,30,0.92) !important; border-right: 1px solid rgba(255,255,255,0.08); }
[data-testid="stSidebar"] * { color: #D0D0F0 !important; }
[data-testid="stSidebar"] label { color: #8888AA !important; font-size:11px !important; text-transform:uppercase; letter-spacing:0.05em; }
.kpi-card { background: rgba(20,22,45,0.85); border-radius:14px; padding:20px 24px; border-left:4px solid; backdrop-filter:blur(4px); border-top:1px solid rgba(255,255,255,0.07); }
.kpi-value { font-size:30px; font-weight:600; font-family:'IBM Plex Mono',monospace; margin:4px 0; }
.kpi-label { font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:#8888AA; }
.kpi-delta { font-size:12px; color:#6666AA; margin-top:4px; }
.chart-box { background:rgba(15,17,38,0.85); border-radius:14px; padding:16px 18px 10px; border:1px solid rgba(255,255,255,0.07); backdrop-filter:blur(4px); margin-bottom:16px; }
.section-title { font-size:12px; font-weight:500; text-transform:uppercase; letter-spacing:0.1em; color:#8888BB; margin:0 0 12px 0; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.08); }
.result-card { background:rgba(20,22,45,0.92); border-radius:10px; padding:14px 18px; border:1px solid rgba(255,255,255,0.08); margin-bottom:10px; color:#D0D0F0; }
.result-card strong { color:#FFFFFF; }
.result-card .tag { display:inline-block; font-size:11px; padding:2px 8px; border-radius:4px; background:rgba(79,142,247,0.2); color:#7AACFF; margin-right:6px; font-family:'IBM Plex Mono',monospace; }
</style>
""", unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Sans", color="#D0D0F0"),
    margin=dict(l=10, r=20, t=10, b=10), coloraxis_showscale=False,
)

# ─────────────────────────────────────────────────────────────
# 49 COLUNAS EXATAS DO SISTEMA
# ─────────────────────────────────────────────────────────────
COLUNAS_ARQUIVO = [
    "CODFILIAL",
    "DTENT",
    "NOTA_DEVOLUCAO",
    "CODFUNCLANC",
    "DTSAIDA",
    "NOTA_VENDA",
    "NUMCAR",
    "PLACA",
    "DESTINO",
    "DTENTREGA",
    "VLTOTAL",
    "CODDEVOL",
    "OBS",
    "MOTIVO",
    "NUMTRANSENT",
    "COD_FORNEC_FRETE_SAIDA",
    "FORNECEDOR FRETE SAIDA",
    "COD.FORNEC.FRETE ENTRADA",
    "FORNECEDOR FRETE ENTRADA",
    "TOTPESO",
    "CODFILIALNF",
    "CODCLI",
    "CLIENTE",
    "NOME_CIDADE",
    "ENDERENT",
    "TELENT",
    "ROTINALANC",
    "CODMOTORISTADEVOL",
    "MOTORISTA",
    "CODRCA",
    "NOMERCA",
    "CODSUPERVISOR",
    "SUPERVISOR",
    "NOMEFUNC",
    "QTAVARIA",
    "VLAVARIA",
    "CONF_MATRICULA",
    "CONF_NOME",
    "VLFRETE",
    "VLOUTRAS",
    "VLTOTNF",
    "VALOR_VENDA",
    "NUMBONUS",
    "CLI_REDE",
    "CODPRACA",
    "PRACA",
    "ROTA",
    "FINALIZADO",
    "TIPO_MERCADO",
]

LABELS = {
    "CODFILIAL":                "Filial",
    "DTENT":                    "Dt. Devolução",
    "NOTA_DEVOLUCAO":           "Nº Dev.",
    "CODFUNCLANC":              "Cód. Func. Lanç.",
    "DTSAIDA":                  "Dt. Saída",
    "NOTA_VENDA":               "Nº Venda",
    "NUMCAR":                   "Nº Carregamento",
    "PLACA":                    "Placa",
    "DESTINO":                  "Destino",
    "DTENTREGA":                "Dt. Entrega",
    "VLTOTAL":                  "Valor Total",
    "CODDEVOL":                 "Cód. Motivo",
    "OBS":                      "Observações",
    "MOTIVO":                   "Motivo",
    "NUMTRANSENT":              "NF Entrada",
    "COD_FORNEC_FRETE_SAIDA":   "Cód. Forn. Frete Saída",
    "FORNECEDOR FRETE SAIDA":   "Transp. Saída",
    "COD.FORNEC.FRETE ENTRADA": "Cód. Forn. Frete Entrada",
    "FORNECEDOR FRETE ENTRADA": "Transp. Entrada",
    "TOTPESO":                  "Peso Total",
    "CODFILIALNF":              "Filial NF",
    "CODCLI":                   "Cód. Cliente",
    "CLIENTE":                  "Nome Cliente",
    "NOME_CIDADE":              "Cidade",
    "ENDERENT":                 "Endereço",
    "TELENT":                   "Telefone",
    "ROTINALANC":               "Rotina Lanç.",
    "CODMOTORISTADEVOL":        "Cód. Motorista",
    "MOTORISTA":                "Motorista",
    "CODRCA":                   "Cód. RCA",
    "NOMERCA":                  "Vendedor (RCA)",
    "CODSUPERVISOR":            "Cód. Supervisor",
    "SUPERVISOR":               "Supervisor",
    "NOMEFUNC":                 "Gerente / Func.",
    "QTAVARIA":                 "Qt. Avaria",
    "VLAVARIA":                 "Vl. Avaria",
    "CONF_MATRICULA":           "Matr. Conferente",
    "CONF_NOME":                "Nome Conferente",
    "VLFRETE":                  "Vl. Frete",
    "VLOUTRAS":                 "Vl. Outras",
    "VLTOTNF":                  "Vl. Líq. NF",
    "VALOR_VENDA":              "Vl. Venda Original",
    "NUMBONUS":                 "Nº Bônus",
    "CLI_REDE":                 "Cód. Rede",
    "CODPRACA":                 "Cód. Praça",
    "PRACA":                    "Praça / Segmento",
    "ROTA":                     "Rota / Zona",
    "FINALIZADO":               "Finalizado",
    "TIPO_MERCADO":             "Tipo Mercado",
}


def ler_arquivo(arquivo):
    """Lê .xlsx, .xls ou .csv e retorna (DataFrame, aviso_ou_None)."""
    try:
        nome = arquivo.name.lower()

        if nome.endswith(".csv"):
            df = pd.read_csv(arquivo, sep=None, engine="python", dtype=str)
        elif nome.endswith(".xls"):
            try:
                df = pd.read_excel(arquivo, engine="openpyxl", dtype=str)
            except Exception:
                df = pd.read_excel(arquivo, dtype=str)
        else:
            df = None
            for sheet in [0, "Devoluções", "Sheet1", "Plan1", "Planilha1"]:
                try:
                    df = pd.read_excel(arquivo, sheet_name=sheet, dtype=str)
                    break
                except Exception:
                    continue
            if df is None:
                raise ValueError("Não foi possível ler nenhuma aba do arquivo.")

        # Verifica colunas
        presentes = [c for c in COLUNAS_ARQUIVO if c in df.columns]
        ausentes  = [c for c in COLUNAS_ARQUIVO if c not in df.columns]

        if len(presentes) < 5:
            raise ValueError(
                f"O arquivo não possui as colunas esperadas do sistema.\n"
                f"Primeiras colunas encontradas: {df.columns.tolist()[:8]}"
            )

        # Mantém apenas as colunas do sistema presentes no arquivo
        df = df[[c for c in COLUNAS_ARQUIVO if c in df.columns]].copy()

        # Converte datas
        for dcol in ["DTENT", "DTSAIDA", "DTENTREGA"]:
            if dcol in df.columns:
                df[dcol] = pd.to_datetime(df[dcol], errors="coerce").dt.strftime("%d/%m/%Y")

        # Converte numéricos
        for ncol in ["VLTOTAL", "VLTOTNF", "VALOR_VENDA", "VLAVARIA",
                     "VLFRETE", "VLOUTRAS", "TOTPESO", "QTAVARIA"]:
            if ncol in df.columns:
                df[ncol] = pd.to_numeric(df[ncol], errors="coerce").fillna(0)

        # Converte inteiros (IDs, números)
        for icol in ["NOTA_DEVOLUCAO", "NOTA_VENDA", "NUMTRANSENT", "CODCLI",
                     "CODDEVOL", "CODRCA", "CODSUPERVISOR", "NUMCAR",
                     "CODPRACA", "NUMBONUS", "CODFUNCLANC", "CODMOTORISTADEVOL"]:
            if icol in df.columns:
                df[icol] = df[icol].apply(
                    lambda x: str(int(float(x))) if pd.notna(x) and str(x).strip() not in ("", "nan") else ""
                )

        # Limpa strings
        obj_cols = df.select_dtypes(include="object").columns
        df[obj_cols] = df[obj_cols].fillna("").astype(str).apply(lambda s: s.str.strip())

        aviso = f"⚠️ Colunas não encontradas no arquivo (serão ignoradas): {', '.join(ausentes)}" if ausentes else None
        return df, aviso

    except Exception as e:
        return None, str(e)


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📦 Dashboard\n**Devoluções**")
    st.markdown("---")
    st.markdown("**IMPORTAR DADOS**")
    st.markdown(
        "<div style='font-size:11px;color:#8888AA;line-height:1.8'>"
        "Formatos aceitos: <b>.xlsx · .xls · .csv</b><br>"
        "O arquivo deve conter as colunas exportadas pelo sistema "
        "(DTENT, NOTA_DEVOLUCAO, MOTIVO, VLTOTAL, PLACA, ROTA…)"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    arquivo = st.file_uploader("Arraste o arquivo aqui", type=["xlsx", "xls", "csv"])

    df = pd.DataFrame()
    aviso_colunas = None

    if arquivo:
        df_novo, resultado = ler_arquivo(arquivo)
        if df_novo is None:
            st.error(f"Erro ao ler arquivo:\n{resultado}")
        else:
            df = df_novo
            aviso_colunas = resultado
            st.success(f"✓ {len(df)} registros carregados")
    else:
        st.info("Nenhum arquivo carregado.\nImporte um arquivo para visualizar o dashboard.")

    st.markdown("---")
    st.markdown("**FILTROS**")

    def opts(col, rotulo_todos):
        if not df.empty and col in df.columns:
            vals = sorted(df[col].replace("", pd.NA).dropna().unique().tolist())
            return [rotulo_todos] + vals
        return [rotulo_todos]

    rota_sel   = st.selectbox("Rota / Zona",  opts("ROTA",       "Todas"))
    motivo_sel = st.selectbox("Motivo",        opts("MOTIVO",     "Todos"))
    sup_sel    = st.selectbox("Supervisor",    opts("SUPERVISOR", "Todos"))
    placa_sel  = st.selectbox("Placa",         opts("PLACA",      "Todas"))


# ─────────────────────────────────────────────────────────────
# FILTRO
# ─────────────────────────────────────────────────────────────
df_f = df.copy()
if not df_f.empty:
    if rota_sel   != "Todas": df_f = df_f[df_f["ROTA"]      == rota_sel]
    if motivo_sel != "Todos": df_f = df_f[df_f["MOTIVO"]     == motivo_sel]
    if sup_sel    != "Todos": df_f = df_f[df_f["SUPERVISOR"] == sup_sel]
    if placa_sel  != "Todas": df_f = df_f[df_f["PLACA"]      == placa_sel]


# ─────────────────────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────────────────────
st.markdown("## 📦 Devoluções — Visão Geral")

if aviso_colunas:
    st.warning(aviso_colunas)

if df.empty:
    st.warning("⬅️ Importe um arquivo Excel ou CSV na barra lateral para visualizar o dashboard.")
    st.stop()


# ─────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card" style="border-color:#E05C3A">
        <div class="kpi-label">Total de Devoluções</div>
        <div class="kpi-value" style="color:#E05C3A">{len(df_f)}</div>
        <div class="kpi-delta">registros no período</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card" style="border-color:#4F8EF7">
        <div class="kpi-label">Valor Total (VLTOTAL)</div>
        <div class="kpi-value" style="color:#4F8EF7">R$ {df_f["VLTOTAL"].sum():,.0f}</div>
        <div class="kpi-delta">soma dos pedidos devolvidos</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card" style="border-color:#34D399">
        <div class="kpi-label">Valor Líquido NF (VLTOTNF)</div>
        <div class="kpi-value" style="color:#34D399">R$ {df_f["VLTOTNF"].sum():,.0f}</div>
        <div class="kpi-delta">valor líquido das NFs</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card" style="border-color:#A78BFA">
        <div class="kpi-label">Clientes Únicos</div>
        <div class="kpi-value" style="color:#A78BFA">{df_f["CODCLI"].nunique()}</div>
        <div class="kpi-delta">com devolução</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ABAS
# ─────────────────────────────────────────────────────────────
aba1, aba2, aba3 = st.tabs(["📊  Gráficos", "🔍  Pesquisa", "📋  Tabela Completa"])


# ── ABA 1: GRÁFICOS ──────────────────────────────────────────
with aba1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-box"><div class="section-title">Devoluções por Motivo</div>', unsafe_allow_html=True)
        mot = (df_f.groupby("MOTIVO")
                   .agg(QTD=("NOTA_DEVOLUCAO","count"), VALOR=("VLTOTAL","sum"))
                   .reset_index().sort_values("QTD", ascending=True))
        fig1 = px.bar(mot, x="QTD", y="MOTIVO", orientation="h",
                      color="VALOR", color_continuous_scale=[[0,"#1E3A5F"],[1,"#4F8EF7"]],
                      labels={"QTD":"Qtd","MOTIVO":"","VALOR":"Valor (R$)"}, text="QTD")
        fig1.update_traces(textposition="outside", textfont_color="#FFFFFF")
        fig1.update_layout(**PLOT_LAYOUT, height=320,
                           xaxis=dict(gridcolor="rgba(255,255,255,0.07)", color="#9090B0"),
                           yaxis=dict(color="#CCCCEE", tickfont=dict(size=11)))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-box"><div class="section-title">Valor Devolvido por Placa</div>', unsafe_allow_html=True)
        placa_grp = (df_f[df_f["PLACA"].str.strip() != ""]
                     .groupby("PLACA")
                     .agg(QTD=("NOTA_DEVOLUCAO","count"), VALOR=("VLTOTAL","sum"))
                     .reset_index().sort_values("VALOR", ascending=True))
        fig2 = px.bar(placa_grp, x="VALOR", y="PLACA", orientation="h",
                      color="VALOR", color_continuous_scale=[[0,"#1B3A5E"],[1,"#34D399"]],
                      labels={"VALOR":"Valor (R$)","PLACA":"","QTD":"Qtd"},
                      text=placa_grp["VALOR"].apply(lambda v: f"R$ {v:,.0f}"))
        fig2.update_traces(textposition="outside", textfont_color="#FFFFFF", textfont_size=10)
        fig2.update_layout(**PLOT_LAYOUT, height=320,
                           xaxis=dict(gridcolor="rgba(255,255,255,0.07)", color="#9090B0", tickformat=",.0f"),
                           yaxis=dict(color="#CCCCEE", tickfont=dict(size=11)))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="chart-box"><div class="section-title">Top Supervisores por Valor</div>', unsafe_allow_html=True)
        sup_grp = (df_f.groupby("SUPERVISOR")["VLTOTAL"]
                       .sum().reset_index()
                       .sort_values("VLTOTAL", ascending=False).head(8))
        fig3 = px.bar(sup_grp, x="SUPERVISOR", y="VLTOTAL",
                      color="VLTOTAL", color_continuous_scale=[[0,"#7C1A1A"],[1,"#E05C3A"]],
                      labels={"SUPERVISOR":"","VLTOTAL":"Valor (R$)"})
        fig3.update_layout(**PLOT_LAYOUT, height=280,
                           xaxis=dict(tickangle=-30, tickfont=dict(size=10), color="#9090B0"),
                           yaxis=dict(gridcolor="rgba(255,255,255,0.07)", color="#9090B0"))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-box"><div class="section-title">Top 10 Clientes — Valor Devolvido</div>', unsafe_allow_html=True)
        cli = (df_f.groupby(["CODCLI","CLIENTE"])["VLTOTAL"]
                   .sum().reset_index()
                   .sort_values("VLTOTAL", ascending=True).tail(10))
        cli["NOME_CURTO"] = cli["CLIENTE"].str[:28]
        fig4 = px.bar(cli, x="VLTOTAL", y="NOME_CURTO", orientation="h",
                      color="VLTOTAL", color_continuous_scale=[[0,"#2D1B5E"],[1,"#A78BFA"]],
                      labels={"VLTOTAL":"Valor (R$)","NOME_CURTO":""})
        fig4.update_layout(**PLOT_LAYOUT, height=280,
                           xaxis=dict(gridcolor="rgba(255,255,255,0.07)", color="#9090B0"),
                           yaxis=dict(color="#CCCCEE", tickfont=dict(size=10)))
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── ABA 2: PESQUISA ───────────────────────────────────────────
with aba2:
    st.markdown("#### 🔍 Pesquisar Devoluções")
    col_tipo, col_termo = st.columns([1, 3])
    with col_tipo:
        tipo_busca = st.selectbox("Buscar por", [
            "Nº Devolução",
            "Nº Nota de Venda",
            "NF Entrada",
            "Cód. Cliente",
            "Nome do Cliente",
            "Motivo",
            "Rota / Zona",
            "Placa",
            "Supervisor",
            "Vendedor (RCA)",
            "Motorista",
            "Praça / Segmento",
            "Destino",
        ])
    with col_termo:
        termo = st.text_input("Digite o que deseja buscar",
                              placeholder="Ex: 3771, RUFINO, PHW6348...")

    mapa_busca = {
        "Nº Devolução":       "NOTA_DEVOLUCAO",
        "Nº Nota de Venda":   "NOTA_VENDA",
        "NF Entrada":         "NUMTRANSENT",
        "Cód. Cliente":       "CODCLI",
        "Nome do Cliente":    "CLIENTE",
        "Motivo":             "MOTIVO",
        "Rota / Zona":        "ROTA",
        "Placa":              "PLACA",
        "Supervisor":         "SUPERVISOR",
        "Vendedor (RCA)":     "NOMERCA",
        "Motorista":          "MOTORISTA",
        "Praça / Segmento":   "PRACA",
        "Destino":            "DESTINO",
    }

    if termo.strip():
        coluna = mapa_busca[tipo_busca]
        if coluna in df.columns:
            resultado = df[df[coluna].astype(str).str.upper().str.contains(termo.strip().upper(), na=False)]
        else:
            resultado = pd.DataFrame()

        if resultado.empty:
            st.warning("Nenhum registro encontrado.")
        else:
            st.markdown(f"**{len(resultado)} registro(s) encontrado(s)**")
            for _, row in resultado.iterrows():
                transp = row.get("FORNECEDOR FRETE SAIDA", "") or row.get("FORNECEDOR FRETE ENTRADA", "") or "—"
                st.markdown(f"""<div class="result-card">
                    <span class="tag">Dev. {row['NOTA_DEVOLUCAO']}</span>
                    <span class="tag">NF {row['NUMTRANSENT']}</span>
                    <span class="tag">Venda {row['NOTA_VENDA']}</span>
                    <span class="tag">Placa {row['PLACA']}</span>
                    <span class="tag">Car. {row['NUMCAR']}</span><br><br>
                    <strong>{row['CLIENTE']}</strong> &nbsp;·&nbsp; Cód. {row['CODCLI']}<br>
                    <span style="color:#8888AA;font-size:12px">{row['ENDERENT']} — {row['NOME_CIDADE']}</span><br>
                    <span style="color:#8888AA;font-size:12px">Tel: {row['TELENT']}</span><br><br>
                    <span style="color:#E05C3A">⚠ {row['MOTIVO']}</span>
                    &nbsp;·&nbsp; <span style="color:#9090BB">{row['ROTA']}</span>
                    &nbsp;·&nbsp; <span style="color:#34D399">Vl. Total: R$ {float(row['VLTOTAL']):,.2f}</span>
                    &nbsp;·&nbsp; <span style="color:#A78BFA">Líq. NF: R$ {float(row['VLTOTNF']):,.2f}</span><br>
                    <span style="color:#AAAACC;font-size:12px">
                        Vl. Venda Original: R$ {float(row['VALOR_VENDA']):,.2f}
                        &nbsp;·&nbsp; Peso: {row['TOTPESO']} kg
                        &nbsp;·&nbsp; Praça: {row['PRACA']}
                    </span><br>
                    <span style="font-size:11px;color:#666688">
                        Supervisor: {row['SUPERVISOR']}
                        &nbsp;|&nbsp; RCA: {row['NOMERCA']}
                        &nbsp;|&nbsp; Motorista: {row['MOTORISTA']}
                        &nbsp;|&nbsp; Transp.: {transp}
                        &nbsp;|&nbsp; Gerente: {row['NOMEFUNC']}
                        &nbsp;|&nbsp; Dt. Dev.: {row['DTENT']}
                        &nbsp;|&nbsp; Dt. Saída: {row['DTSAIDA']}
                        &nbsp;|&nbsp; Dt. Entrega: {row['DTENTREGA']}
                        &nbsp;|&nbsp; Finalizado: {row['FINALIZADO']}
                        &nbsp;|&nbsp; Tipo: {row['TIPO_MERCADO']}
                    </span>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<br><div style='color:#555577;text-align:center'>Digite um termo acima para pesquisar</div>",
                    unsafe_allow_html=True)


# ── ABA 3: TABELA COMPLETA ────────────────────────────────────
with aba3:
    colunas_disp = [c for c in COLUNAS_ARQUIVO if c in df_f.columns]
    df_tab = df_f[colunas_disp].copy()

    for vcol in ["VLTOTAL", "VLTOTNF", "VALOR_VENDA", "VLAVARIA", "VLFRETE", "VLOUTRAS"]:
        if vcol in df_tab.columns:
            df_tab[vcol] = df_tab[vcol].apply(
                lambda x: f"R$ {float(x):,.2f}" if str(x) not in ("", "0", "0.0") else "—"
            )

    df_tab.columns = [LABELS.get(c, c) for c in df_tab.columns]

    st.dataframe(df_tab, use_container_width=True, height=460)
    st.markdown("<br>", unsafe_allow_html=True)

    buf = BytesIO()
    df_f[colunas_disp].to_excel(buf, index=False, sheet_name="Devoluções Filtradas")
    st.download_button(
        "⬇️ Exportar dados filtrados (.xlsx)",
        data=buf.getvalue(),
        file_name="devolucoes_filtradas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

st.markdown(
    "<br><div style='text-align:center;color:#33334A;font-size:11px'>"
    "Dashboard de Devoluções · Manaus · 2026</div>",
    unsafe_allow_html=True,
)
