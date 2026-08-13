# ── COLUMN FIXES APPLIED based on real spreadsheet:
# ABA DEVOLUÇÕES (8456- DEVOLUCAO 2026):
#   VLTOTAL, DTENT (filter), DTENTREGA (delivery), NOTA_VENDA, NOTA_DEVOLUCAO,
#   NUMCAR, PLACA, DESTINO, MOTIVO, CODCLI, CLIENTE, MOTORISTA, NOMERCA,
#   NOMEFUNC, SUPERVISOR, TIPO_MERCADO, DTSAIDA, PRACA, NOME_CIDADE
# ABA REENTREGAS (8261 - REENTREGAS 2026):
#   VLTOTGER, DTRANSF, NUMTRANSVENDA, CODUSUR, TOTPESO, PLACAANT, PLACAATUAL,
#   MOTIVOTRANSF, CODMOTIVO, CLIENTE, NUMNOTA, NUMPED, PRACA, NOME (vendedor)
#
# ── REDESIGN VISUAL (v2) ─────────────────────────────────────────────────────
# Nenhuma regra de negócio, cálculo, filtro, consulta ou fonte de dados foi
# alterada. As mudanças são exclusivamente de apresentação e organização:
#   • Menu lateral fixo (navegação por páginas em vez de abas)
#   • Novo cabeçalho com status de sincronização, notificações e usuário
#   • Painel de filtros compacto + limpar filtros
#   • Cards de indicadores redesenhados
#   • Gráficos com eixos discretos, grid quase imperceptível e tooltip moderno
#   • Layout responsivo (desktop / notebook / tablet)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
from datetime import datetime, date

st.set_page_config(
    page_title="Gestão de Devoluções Delly's",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root{
  --bg-0:#04070f; --bg-1:#070c18; --bg-2:#0b1424;
  --panel:rgba(14,23,41,0.62); --panel-solid:rgba(10,17,32,0.94);
  --line:rgba(120,170,225,0.13); --line-strong:rgba(56,189,248,0.30);
  --cyan:#22d3ee; --blue:#3b82f6; --sky:#38bdf8;
  --violet:#a78bfa; --green:#34d399; --amber:#fbbf24; --red:#f87171;
  --txt-0:#f1f6fc; --txt-1:#b9c8dc; --txt-2:#7c8ea8; --txt-3:#4e5f78;
  --r-lg:20px; --r-md:14px; --r-sm:10px;
}

*,*::before,*::after{box-sizing:border-box;}
html,body,.stApp{font-family:'Inter',sans-serif;color:var(--txt-1);background:var(--bg-0);}

/* ── Fundo espacial discreto ─────────────────────────────────────────────── */
.bg-overlay{position:fixed;inset:0;z-index:0;pointer-events:none;}
.bg-img{position:absolute;inset:0;
  background-image:url('https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1920&q=80');
  background-size:cover;background-position:center;
  filter:blur(7px) brightness(0.16) saturate(0.35);transform:scale(1.1);opacity:0.55;}
.bg-tint{position:absolute;inset:0;
  background:
    radial-gradient(1100px 620px at 18% -8%,rgba(34,211,238,0.09),transparent 62%),
    radial-gradient(900px 560px at 88% 4%,rgba(167,139,250,0.07),transparent 60%),
    linear-gradient(180deg,rgba(4,7,15,0.90) 0%,rgba(4,7,15,0.955) 55%,rgba(4,7,15,0.98) 100%);}

.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stAppViewContainer"]>section{background:transparent!important;}
#MainMenu,footer,header{visibility:hidden!important;display:none!important;}
.stDeployButton,[data-testid="stStatusWidget"],[data-testid="stToolbar"],
[data-testid="stHeader"],[data-testid="stDecoration"]{display:none!important;}
.main .block-container{position:relative;z-index:1;padding-top:1.1rem!important;
  padding-bottom:3rem!important;padding-left:2.1rem!important;padding-right:2.1rem!important;max-width:100%!important;}

/* ── Menu lateral ────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,rgba(7,12,24,0.99),rgba(9,16,31,0.99))!important;
  border-right:1px solid var(--line)!important;box-shadow:1px 0 40px rgba(0,0,0,0.5);}
section[data-testid="stSidebar"] .block-container{padding-top:1.4rem!important;}
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"]{opacity:.35;}
.side-brand{display:flex;align-items:center;gap:12px;padding:2px 6px 18px;
  border-bottom:1px solid var(--line);margin-bottom:16px;}
.side-mark{width:40px;height:40px;border-radius:12px;flex:0 0 40px;
  background:linear-gradient(140deg,#0891b2,#2563eb);display:flex;align-items:center;
  justify-content:center;font-size:19px;
  box-shadow:0 0 0 1px rgba(56,189,248,0.28),0 6px 22px rgba(8,145,178,0.35);}
.side-brand-t{font-family:'Sora',sans-serif;font-size:0.86rem;font-weight:600;
  color:var(--txt-0);line-height:1.15;letter-spacing:.01em;}
.side-brand-s{font-size:0.6rem;color:var(--txt-3);letter-spacing:.16em;
  text-transform:uppercase;font-weight:600;margin-top:3px;}
.side-cap{font-size:0.6rem;color:var(--txt-3);letter-spacing:.2em;text-transform:uppercase;
  font-weight:700;margin:14px 0 8px 8px;}

section[data-testid="stSidebar"] div[role="radiogroup"]{gap:2px!important;}
section[data-testid="stSidebar"] div[role="radiogroup"] label{
  width:100%;padding:9px 12px!important;border-radius:var(--r-sm)!important;
  border:1px solid transparent!important;transition:all .18s ease;cursor:pointer;
  background:transparent!important;margin:0!important;}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
  background:rgba(56,189,248,0.06)!important;}
section[data-testid="stSidebar"] div[role="radiogroup"] label>div:first-child{display:none!important;}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{
  font-size:0.83rem!important;font-weight:500!important;color:var(--txt-2)!important;
  letter-spacing:.005em;margin:0!important;}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){
  background:linear-gradient(90deg,rgba(34,211,238,0.16),rgba(37,99,235,0.07))!important;
  border-color:rgba(56,189,248,0.30)!important;
  box-shadow:inset 3px 0 0 var(--cyan),0 4px 18px rgba(8,145,178,0.14);}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{
  color:#e6fbff!important;font-weight:600!important;}
.side-foot{margin-top:20px;padding:12px 12px;border-top:1px solid var(--line);
  font-size:0.66rem;color:var(--txt-3);line-height:1.7;}

/* ── Cabeçalho ───────────────────────────────────────────────────────────── */
.topbar{display:flex;align-items:center;justify-content:space-between;gap:22px;
  background:linear-gradient(100deg,rgba(9,15,29,0.90),rgba(11,20,38,0.86));
  border:1px solid var(--line);border-radius:var(--r-lg);
  padding:16px 24px;margin-bottom:16px;
  backdrop-filter:blur(20px);box-shadow:0 10px 44px rgba(0,0,0,0.42);}
.tb-left{display:flex;align-items:center;gap:16px;min-width:0;}
.tb-icon{width:46px;height:46px;flex:0 0 46px;border-radius:13px;
  background:linear-gradient(140deg,#0e7490,#1d4ed8);display:flex;align-items:center;
  justify-content:center;font-size:21px;
  box-shadow:0 0 0 1px rgba(56,189,248,0.25),0 8px 26px rgba(14,165,233,0.28);}
.tb-title{font-family:'Sora',sans-serif;font-size:1.16rem;font-weight:600;
  color:var(--txt-0);letter-spacing:.015em;line-height:1.2;margin:0;}
.tb-sub{font-size:0.63rem;color:var(--txt-3);font-weight:600;letter-spacing:.19em;
  text-transform:uppercase;margin:5px 0 0;}
.tb-right{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:flex-end;}
.tb-chip{display:flex;align-items:center;gap:8px;padding:8px 13px;border-radius:999px;
  background:rgba(255,255,255,0.035);border:1px solid var(--line);
  font-size:0.72rem;color:var(--txt-1);font-weight:500;white-space:nowrap;}
.tb-chip .dot{width:7px;height:7px;border-radius:50%;background:var(--green);
  box-shadow:0 0 9px rgba(52,211,153,0.85);}
.tb-chip.bell{position:relative;padding:8px 12px;font-size:0.85rem;}
.tb-badge{position:absolute;top:2px;right:4px;min-width:16px;height:16px;padding:0 4px;
  border-radius:999px;background:var(--red);color:#2a0606;font-size:0.6rem;font-weight:700;
  display:flex;align-items:center;justify-content:center;border:2px solid var(--bg-1);}
.tb-user{display:flex;align-items:center;gap:10px;padding:6px 14px 6px 6px;border-radius:999px;
  background:rgba(255,255,255,0.035);border:1px solid var(--line);}
.tb-av{width:31px;height:31px;border-radius:50%;background:linear-gradient(140deg,#22d3ee,#6366f1);
  display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;color:#04121a;}
.tb-un{font-size:0.75rem;color:var(--txt-0);font-weight:600;line-height:1.1;}
.tb-ur{font-size:0.62rem;color:var(--txt-3);letter-spacing:.08em;text-transform:uppercase;margin-top:2px;}

/* ── Painéis / cards ─────────────────────────────────────────────────────── */
.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-lg);
  padding:18px 20px 8px;backdrop-filter:blur(16px);
  box-shadow:0 8px 34px rgba(0,0,0,0.3);margin-bottom:18px;}
.panel-h{display:flex;align-items:center;justify-content:space-between;gap:14px;
  margin-bottom:14px;}
.panel-t{display:flex;align-items:center;gap:11px;}
.panel-t .bar{width:3px;height:19px;border-radius:2px;
  background:linear-gradient(180deg,var(--cyan),var(--blue));box-shadow:0 0 11px rgba(34,211,238,0.5);}
.panel-t h3{font-family:'Sora',sans-serif;font-size:0.9rem;font-weight:600;color:var(--txt-0);
  margin:0;letter-spacing:.01em;}
.panel-tag{font-size:0.64rem;color:var(--txt-3);letter-spacing:.13em;text-transform:uppercase;
  font-weight:600;padding:5px 11px;border-radius:999px;border:1px solid var(--line);
  background:rgba(255,255,255,0.025);white-space:nowrap;}

/* ── KPIs ────────────────────────────────────────────────────────────────── */
.kpi-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;margin-bottom:20px;}
.kpi{position:relative;overflow:hidden;border-radius:var(--r-lg);padding:18px 19px 16px;
  background:linear-gradient(150deg,rgba(16,26,46,0.82),rgba(10,17,32,0.72));
  border:1px solid var(--line);backdrop-filter:blur(14px);
  transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease;}
.kpi:hover{transform:translateY(-3px);border-color:var(--line-strong);
  box-shadow:0 14px 40px rgba(8,145,178,0.14);}
.kpi::after{content:'';position:absolute;left:18px;right:18px;bottom:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--acc,var(--cyan)),transparent);opacity:.55;}
.kpi-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px;}
.kpi-ico{width:31px;height:31px;border-radius:9px;display:flex;align-items:center;
  justify-content:center;font-size:0.92rem;background:rgba(255,255,255,0.045);
  border:1px solid var(--line);}
.kpi-delta{font-family:'JetBrains Mono',monospace;font-size:0.66rem;font-weight:700;
  padding:3px 8px;border-radius:999px;letter-spacing:.02em;}
.kpi-up{color:#fecaca;background:rgba(248,113,113,0.14);border:1px solid rgba(248,113,113,0.28);}
.kpi-down{color:#bbf7d0;background:rgba(52,211,153,0.13);border:1px solid rgba(52,211,153,0.28);}
.kpi-flat{color:var(--txt-2);background:rgba(255,255,255,0.04);border:1px solid var(--line);}
.kpi-val{font-family:'JetBrains Mono',monospace;font-size:1.62rem;font-weight:700;
  color:var(--acc,var(--cyan));line-height:1.05;letter-spacing:-0.02em;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.kpi-lab{font-size:0.63rem;color:var(--txt-2);font-weight:600;letter-spacing:.13em;
  text-transform:uppercase;margin:9px 0 4px;}
.kpi-sub{font-size:0.66rem;color:var(--txt-3);}

/* ── Filtros ─────────────────────────────────────────────────────────────── */
.filters{background:linear-gradient(120deg,rgba(12,20,38,0.80),rgba(9,15,29,0.74));
  border:1px solid var(--line);border-radius:var(--r-lg);padding:14px 20px 4px;
  margin-bottom:18px;backdrop-filter:blur(16px);}
.filters-h{display:flex;align-items:center;gap:9px;font-size:0.63rem;color:var(--txt-2);
  letter-spacing:.17em;text-transform:uppercase;font-weight:700;margin-bottom:6px;}
.filters-h .pip{width:6px;height:6px;border-radius:50%;background:var(--cyan);
  box-shadow:0 0 9px rgba(34,211,238,0.8);}

label,.stSelectbox label,.stMultiSelect label,.stTextInput label,.stRadio label p{
  color:var(--txt-2)!important;font-size:0.68rem!important;font-weight:600!important;
  letter-spacing:.11em!important;text-transform:uppercase!important;}
.stTextInput input,.stDateInput input{background:rgba(255,255,255,0.035)!important;
  border:1px solid var(--line)!important;border-radius:var(--r-sm)!important;
  color:var(--txt-0)!important;font-family:'Inter',sans-serif!important;font-size:0.85rem!important;}
.stTextInput input:focus{border-color:var(--line-strong)!important;
  box-shadow:0 0 0 3px rgba(34,211,238,0.10)!important;}
.stSelectbox div[data-baseweb="select"]>div,.stMultiSelect div[data-baseweb="select"]>div{
  background:rgba(255,255,255,0.035)!important;border:1px solid var(--line)!important;
  border-radius:var(--r-sm)!important;color:var(--txt-0)!important;}
.stMultiSelect span[data-baseweb="tag"]{background:rgba(34,211,238,0.15)!important;
  color:#a5f3fc!important;border-radius:6px!important;}
div[data-baseweb="popover"] ul{background:var(--panel-solid)!important;
  border:1px solid var(--line)!important;}

.stButton>button{background:rgba(255,255,255,0.04)!important;color:var(--txt-1)!important;
  border:1px solid var(--line)!important;border-radius:var(--r-sm)!important;
  font-weight:600!important;font-size:0.8rem!important;padding:9px 18px!important;
  transition:all .2s ease!important;}
.stButton>button:hover{border-color:var(--line-strong)!important;color:var(--txt-0)!important;
  background:rgba(56,189,248,0.09)!important;}
.stButton>button[kind="primary"]{
  background:linear-gradient(120deg,#0891b2,#2563eb)!important;color:#ecfeff!important;
  border:1px solid rgba(56,189,248,0.45)!important;
  box-shadow:0 6px 22px rgba(8,145,178,0.34)!important;}
.stButton>button[kind="primary"]:hover{transform:translateY(-1px);
  box-shadow:0 10px 30px rgba(8,145,178,0.46)!important;}
.stDownloadButton>button{background:rgba(52,211,153,0.09)!important;color:#6ee7b7!important;
  border:1px solid rgba(52,211,153,0.28)!important;border-radius:var(--r-sm)!important;
  font-weight:600!important;}

/* ── Card do gráfico comparativo ─────────────────────────────────────────── */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.cc-head){
  background:linear-gradient(155deg,rgba(13,22,40,0.72),rgba(8,14,27,0.66))!important;
  border:1px solid rgba(56,189,248,0.16)!important;border-radius:22px!important;
  padding:22px 26px 18px!important;margin-bottom:18px;
  backdrop-filter:blur(18px);
  box-shadow:0 18px 60px rgba(0,0,0,0.45),inset 0 1px 0 rgba(255,255,255,0.035);}
.cc-head{display:flex;align-items:flex-start;justify-content:space-between;gap:26px;
  flex-wrap:wrap;padding-bottom:16px;margin-bottom:6px;
  border-bottom:1px solid rgba(120,170,225,0.09);}
.cc-head-l{min-width:240px;}
.cc-title{font-family:'Sora',sans-serif;font-size:1.02rem;font-weight:600;color:#f1f6fc;
  letter-spacing:.01em;margin:0;line-height:1.25;}
.cc-sub{font-size:0.76rem;color:#7c8ea8;margin:7px 0 0;font-weight:400;}
.cc-head-r{display:flex;align-items:stretch;gap:12px;flex-wrap:wrap;}
.cc-mini{display:flex;flex-direction:column;justify-content:center;gap:3px;
  min-width:132px;padding:11px 16px;border-radius:14px;
  background:rgba(255,255,255,0.032);border:1px solid rgba(120,170,225,0.13);}
.cc-mini-lab{font-size:0.6rem;color:#6d8099;font-weight:700;letter-spacing:.15em;
  text-transform:uppercase;}
.cc-mini-val{font-family:'JetBrains Mono',monospace;font-size:1.16rem;font-weight:700;
  letter-spacing:-0.02em;line-height:1.1;}
.cc-mini-sub{font-size:0.63rem;color:#4e5f78;}
.cc-ctrls{display:flex;align-items:center;gap:8px;}
.cc-pick{font-size:0.73rem;color:#b9c8dc;padding:9px 14px;border-radius:11px;
  background:rgba(255,255,255,0.03);border:1px solid rgba(120,170,225,0.13);white-space:nowrap;}
.cc-dots{font-size:1.05rem;color:#6d8099;padding:6px 11px;border-radius:11px;
  background:rgba(255,255,255,0.03);border:1px solid rgba(120,170,225,0.13);line-height:1.1;}
.cc-foot{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:4px;
  padding:15px 20px;border-radius:16px;
  background:linear-gradient(120deg,rgba(255,255,255,0.035),rgba(255,255,255,0.015));
  border:1px solid rgba(120,170,225,0.11);}
.cc-foot-i{display:flex;flex-direction:column;gap:5px;flex:1 1 170px;min-width:150px;}
.cc-foot-lab{display:flex;align-items:center;gap:7px;font-size:0.66rem;color:#6d8099;
  font-weight:700;letter-spacing:.13em;text-transform:uppercase;}
.cc-foot-lab .d{width:7px;height:7px;border-radius:50%;display:inline-block;}
.cc-foot-val{font-family:'JetBrains Mono',monospace;font-size:1.24rem;font-weight:700;
  letter-spacing:-0.02em;}
.cc-foot-sep{width:1px;align-self:stretch;
  background:linear-gradient(180deg,transparent,rgba(120,170,225,0.18),transparent);}
@media (max-width:900px){
  .cc-head{gap:16px;}
  .cc-head-r{width:100%;}
  .cc-mini{flex:1 1 140px;min-width:0;}
  .cc-ctrls{display:none;}
  .cc-foot-sep{display:none;}
  .cc-foot-val{font-size:1.06rem;}
  div[data-testid="stVerticalBlockBorderWrapper"]:has(.cc-head){padding:18px 16px 14px!important;}
}

/* ── Tabelas ─────────────────────────────────────────────────────────────── */
.tbl-wrap{background:rgba(6,11,22,0.86);border:1px solid var(--line);
  border-radius:var(--r-md);overflow:auto;max-height:540px;}
.tbl-wrap table{width:100%;border-collapse:collapse;}
.tbl-wrap th{position:sticky;top:0;background:rgba(11,20,38,0.99);color:var(--sky);
  font-size:0.68rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
  text-align:left;padding:11px 14px;white-space:nowrap;border-bottom:1px solid var(--line-strong);}
.tbl-wrap td{padding:9px 14px;color:var(--txt-1);font-size:0.8rem;white-space:nowrap;
  border-bottom:1px solid rgba(120,170,225,0.06);}
.tbl-wrap tr:hover td{background:rgba(56,189,248,0.05);}
.num{font-family:'JetBrains Mono',monospace;font-weight:600;}

/* ── Diversos ────────────────────────────────────────────────────────────── */
hr{border-color:var(--line)!important;margin:20px 0!important;}
.stAlert{background:rgba(12,22,42,0.8)!important;border:1px solid var(--line)!important;
  border-radius:var(--r-md)!important;}
.stCaption,[data-testid="stCaptionContainer"]{color:var(--txt-3)!important;font-size:.72rem!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(9,16,31,0.8)!important;border-radius:var(--r-md)!important;
  padding:4px!important;gap:4px!important;border:1px solid var(--line)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;border-radius:var(--r-sm)!important;
  color:var(--txt-2)!important;font-weight:600!important;font-size:0.8rem!important;}
.stTabs [aria-selected="true"]{background:rgba(34,211,238,0.13)!important;color:#e6fbff!important;}
.streamlit-expanderHeader,details summary{color:var(--txt-2)!important;font-size:0.8rem!important;}
::-webkit-scrollbar{width:8px;height:8px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(56,189,248,0.20);border-radius:8px;}
::-webkit-scrollbar-thumb:hover{background:rgba(56,189,248,0.38);}

/* ── Responsivo ──────────────────────────────────────────────────────────── */
@media (max-width:1500px){ .kpi-val{font-size:1.42rem;} }
@media (max-width:1200px){
  .kpi-grid{grid-template-columns:repeat(3,minmax(0,1fr));}
  .main .block-container{padding-left:1.2rem!important;padding-right:1.2rem!important;}
  .tb-title{font-size:1.02rem;}
}
@media (max-width:820px){
  .kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr));}
  .topbar{flex-direction:column;align-items:flex-start;gap:14px;}
  .tb-right{justify-content:flex-start;}
}
@media (prefers-reduced-motion:reduce){
  .kpi,.stButton>button{transition:none!important;}
  .kpi:hover{transform:none;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bg-overlay"><div class="bg-img"></div><div class="bg-tint"></div></div>',
            unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# HELPERS DE FORMATAÇÃO E GRÁFICOS  (regras de cálculo inalteradas)
# ═════════════════════════════════════════════════════════════════════════════
def fmt_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"


def fmt_brl0(v):
    """Formata valor monetário em R$ SEM casas decimais (arredondado), usado nos gráficos."""
    try:
        return f"R$ {round(float(v)):,}".replace(",", ".")
    except:
        return "R$ 0"


HOVER = dict(bgcolor="rgba(8,14,28,0.96)", bordercolor="rgba(56,189,248,0.35)",
             font=dict(color="#e8f4ff", family="Inter", size=12))

GRID = "rgba(120,170,225,0.07)"


def plotly_dark(fig, height=None, margin_b=40):
    u = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             font=dict(color="#b9c8dc", family="Inter"), coloraxis_showscale=False,
             margin=dict(t=18, b=margin_b, l=8, r=12),
             hoverlabel=HOVER,
             xaxis=dict(tickfont=dict(color="#8fa3bd", size=12, family="Inter"),
                        gridcolor=GRID, linecolor="rgba(120,170,225,0.10)", zeroline=False),
             yaxis=dict(tickfont=dict(color="#8fa3bd", size=12),
                        gridcolor=GRID, linecolor="rgba(120,170,225,0.10)", zeroline=False),
             legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
                         font=dict(color="#b9c8dc", size=12)))
    if height:
        u["height"] = height
    fig.update_layout(**u)
    return fig


BLUE = ["#0c4a6e", "#0369a1", "#0ea5e9", "#7dd3fc", "#bae6fd"]
RED = ["#7f1d1d", "#b91c1c", "#ef4444", "#fca5a5"]
GREEN = ["#14532d", "#15803d", "#22c55e", "#86efac", "#bbf7d0"]
MIXED = ["#22d3ee", "#34d399", "#fbbf24", "#f87171", "#a78bfa", "#f472b6", "#2dd4bf", "#fb923c"]

C_CRIT, C_WARN, C_BASE, C_OK = "#f87171", "#fb923c", "#38bdf8", "#34d399"


def ramp(n, top=5, mid=10, base=C_BASE):
    """Escala de cor por criticidade (mesma lógica de destaque do layout original)."""
    return [C_CRIT if i < top else C_WARN if i < mid else base for i in range(n)]


def panel_open(title, tag=None, icon=""):
    tg = f'<span class="panel-tag">{tag}</span>' if tag else ""
    st.markdown(
        f'<div class="panel"><div class="panel-h"><div class="panel-t"><div class="bar"></div>'
        f'<h3>{icon} {title}</h3></div>{tg}</div>', unsafe_allow_html=True)


def panel_close():
    st.markdown('</div>', unsafe_allow_html=True)


def html_table(df_in, accent="#38bdf8", max_rows=500, min_width=900):
    heads = "".join([f"<th>{c}</th>" for c in df_in.columns])
    rws = ""
    for _, row in df_in.head(max_rows).iterrows():
        cells = "".join([f"<td>{v}</td>" for v in row.values])
        rws += f"<tr>{cells}</tr>"
    st.markdown(
        f'<div class="tbl-wrap"><table style="min-width:{min_width}px;">'
        f'<thead><tr>{heads}</tr></thead><tbody>{rws}</tbody></table></div>',
        unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# FONTE DE DADOS  (inalterada)
# ═════════════════════════════════════════════════════════════════════════════
SHEET_ID = "1GCw6vE5lrIZYJUKnQlKvBMX71CgIdxcRBA1YCrjFadI"
GSHEETS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}"

REENTREGAS_URLS = [
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=8261+-+REENTREGAS+2026",
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=8261%20-%20REENTREGAS%202026",
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=REENTREGAS+2026",
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=REENTREGAS",
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1",
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=2",
]


@st.cache_data(ttl=60)
def load_data(url):
    r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))


@st.cache_data(ttl=60)
def load_reentregas():
    """Tenta múltiplas URLs até encontrar a aba de reentregas com dados válidos."""
    erros = []
    for url in REENTREGAS_URLS:
        try:
            r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            df = pd.read_csv(io.StringIO(r.text))
            cols_up = [str(c).strip().upper().replace(" ", "_") for c in df.columns]
            if any(c in cols_up for c in ["DTRANSF", "MOTIVOTRANSF", "NUMNOTA", "VLTOTGER"]):
                return df, url, None
            else:
                erros.append(f"URL ok mas colunas não reconhecidas: {cols_up[:6]}")
        except Exception as e:
            erros.append(f"{url.split('sheet=')[-1][:40]} → {str(e)[:80]}")
    return None, None, erros


def parse_brl(s):
    s = str(s).replace("R$", "").strip()
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    return pd.to_numeric(s, errors="coerce")


with st.spinner("Carregando dados..."):
    try:
        df_raw = load_data(GSHEETS_URL)
    except Exception as e:
        st.error(f"Não foi possível carregar as devoluções: {e}")
        st.stop()

df_reent_raw = None
reent_load_error = None
reent_url_usada = None
try:
    df_reent_raw, reent_url_usada, _erros = load_reentregas()
    if df_reent_raw is None:
        reent_load_error = "Nenhuma URL funcionou: " + " | ".join(_erros or [])
except Exception as e:
    reent_load_error = str(e)

# ── Normaliza colunas devoluções ────────────────────────────────────────────
df_raw.columns = [str(c).strip().upper().replace(" ", "_") for c in df_raw.columns]
actual_cols = list(df_raw.columns)


def get_col(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None


VALOR_COL = get_col(df_raw, ["VLTOTAL", "VLT", "VL_TOTAL", "VALOR_LIQUIDO", "VALOR", "TOTAL"]) or "VLTOTAL"
COL_PLACA = get_col(df_raw, ["PLACA"])
COL_MOTIVO = get_col(df_raw, ["MOTIVO", "MOTIVO_DEVOLUCAO", "MOTIVO_DEV"])
COL_CLIENTE = get_col(df_raw, ["CLIENTE", "NOME_CLIENTE", "RAZAO_SOCIAL"])
COL_VENDEDOR = get_col(df_raw, ["NOMERCA", "VENDEDOR", "NOME_VENDEDOR"])
COL_DEVOLUCION = get_col(df_raw, ["NOMEFUNC", "DEVOLUCIONISTA", "FUNCIONARIO"])
COL_MOTORISTA = get_col(df_raw, ["MOTORISTA", "ENTREGADOR"])
COL_DESTINO = get_col(df_raw, ["DESTINO", "NOME_CIDADE", "CIDADE", "MUNICIPIO"])
COL_NF_VENDA = get_col(df_raw, ["NOTA_VENDA", "NF_VENDA", "NF_SAIDA", "NOTA_SAIDA", "NOTA_FISCAL"])
COL_NOTA_DEV = get_col(df_raw, ["NOTA_DEVOLUCAO", "NF_DEVOLUCAO"])
COL_NUMCAR = get_col(df_raw, ["NUMCAR", "NUM_CARREGAMENTO", "CARREGAMENTO"])
COL_CODCLI = get_col(df_raw, ["CODCLI", "COD_CLI", "CLI"])
COL_SUPERVISOR = get_col(df_raw, ["SUPERVISOR", "AM", "GERENTE"])
COL_PRACA = get_col(df_raw, ["PRACA"])
COL_TIPO_MERC = get_col(df_raw, ["TIPO_MERCADO", "CANAL", "SEGMENTO"])
COL_DTSAIDA = get_col(df_raw, ["DTSAIDA", "DATA_DEVOLUCAO", "DATA", "DT_DEVOLUCAO"])
COL_DTENTREGA = get_col(df_raw, ["DTENT", "DTENTREGA", "DATA_ENTREGA", "DT_ENTREGA"])

if VALOR_COL not in df_raw.columns:
    df_raw[VALOR_COL] = 0.0

df_raw[VALOR_COL] = df_raw[VALOR_COL].apply(parse_brl).fillna(0)
for col in df_raw.columns:
    if col != VALOR_COL:
        df_raw[col] = df_raw[col].fillna("").astype(str).str.strip()

if COL_DTENTREGA:
    df_raw["_DTENTREGA_DT"] = pd.to_datetime(df_raw[COL_DTENTREGA], dayfirst=True, errors="coerce")
    mask_nat = df_raw["_DTENTREGA_DT"].isna() & (df_raw[COL_DTENTREGA] != "")
    if mask_nat.any():
        df_raw.loc[mask_nat, "_DTENTREGA_DT"] = pd.to_datetime(
            df_raw.loc[mask_nat, COL_DTENTREGA], format="%Y-%m-%d", errors="coerce")
else:
    df_raw["_DTENTREGA_DT"] = pd.NaT

# ── Normaliza colunas reentregas ────────────────────────────────────────────
REENT_COLS_MAP = {
    "NUMNOTA": ["NUMNOTA"],
    "DTFAT": ["DTFAT"],
    "SERIE": ["SERIE"],
    "ESPECIE": ["ESPECIE"],
    "DTSAIDA": ["DTSAIDA"],
    "VLTOTGER": ["VLTOTGER", "VLTOT", "VLTOTAL"],
    "TOTPESO": ["TOTPESO", "PESO"],
    "NUMTRANSVENDA": ["NUMTRANSVENDA", "NUMTRANS"],
    "NUMCARANTERIOR": ["NUMCARANTERIOR"],
    "PLACAANT": ["ANTERIOR", "PLACAANT", "PLACA_ANT", "PLACAANTERIOR"],
    "COD_MOT_ANTERIOR": ["COD_MOT_ANTERIOR"],
    "NOME_MOT_ANTERIOR": ["NOME_MOT_ANTERIOR"],
    "COD_AJU_ANTERIOR": ["COD_AJU_ANTERIOR"],
    "NOME_AJU_ANTERIOR": ["NOME_AJU_ANTERIOR"],
    "NUMCARATUAL": ["NUMCARATUAL"],
    "PLACAATUAL": ["PLACA_ATUAL", "PLACAATUAL", "PLACA_ATU"],
    "COD_MOT_ATUAL": ["COD_MOT_ATUAL"],
    "NOME_MOT_ATUAL": ["NOME_MOT_ATUAL"],
    "COD_AJU_ATUAL": ["COD_AJU_ATUAL"],
    "NOME_AJU_ATUAL": ["NOME_AJU_ATUAL"],
    "DATATRANSF": ["DTRANSF", "DATATRANSF", "DATA_TRANSF"],
    "CODMOTIVO": ["CODMOTIVO"],
    "MOTIVOTRANSF": ["MOTIVOTRANSF", "MOTIVO_TRANSF"],
    "CODCLI": ["CODCLI"],
    "CLIENTE": ["CLIENTE"],
    "BAIRROENT": ["BAIRROENT"],
    "CODPRACA": ["CODPRACA"],
    "PRACA": ["PRACA"],
    "ROTA": ["ROTA"],
    "NUMPED": ["NUMPED"],
    "CODUSU": ["CODUSUR", "CODUSU"],
    "NOME": ["NOME", "RNOME"],
}

df_reent = None
reent_cols = {}
REENT_VALOR_COL = "_VALOR_REENT"

if df_reent_raw is not None:
    df_reent_raw.columns = [str(c).strip().upper().replace(" ", "_") for c in df_reent_raw.columns]

    def get_col_reent(alts):
        for n in alts:
            if n.strip().upper().replace(" ", "_") in df_reent_raw.columns:
                return n.strip().upper().replace(" ", "_")
        return None

    for canonical, alts in REENT_COLS_MAP.items():
        reent_cols[canonical] = get_col_reent(alts)

    rv = get_col_reent(["VLTOTGER", "VLTOT", "VLTOTAL", "VALOR", "TOTAL"])
    if rv:
        REENT_VALOR_COL = rv
        df_reent_raw[rv] = df_reent_raw[rv].apply(parse_brl).fillna(0)
    else:
        df_reent_raw["_VALOR_REENT"] = 0.0

    for col in df_reent_raw.columns:
        if col != REENT_VALOR_COL:
            df_reent_raw[col] = df_reent_raw[col].fillna("").astype(str).str.strip()

    dt_col_r = reent_cols.get("DATATRANSF")
    if not dt_col_r:
        for _c in ["DTRANSF", "DATATRANSF", "DATA_TRANSF"]:
            if _c in df_reent_raw.columns:
                dt_col_r = _c
                reent_cols["DATATRANSF"] = _c
                break
    if dt_col_r and dt_col_r in df_reent_raw.columns:
        df_reent_raw["_DATATRANSF_DT"] = pd.to_datetime(df_reent_raw[dt_col_r], dayfirst=True, errors="coerce")
        m2 = df_reent_raw["_DATATRANSF_DT"].isna() & (df_reent_raw[dt_col_r] != "")
        if m2.any():
            df_reent_raw.loc[m2, "_DATATRANSF_DT"] = pd.to_datetime(
                df_reent_raw.loc[m2, dt_col_r], format="%Y-%m-%d", errors="coerce")
    else:
        df_reent_raw["_DATATRANSF_DT"] = pd.NaT

    df_reent = df_reent_raw.copy()


# ═════════════════════════════════════════════════════════════════════════════
# CABEÇALHO
# ═════════════════════════════════════════════════════════════════════════════
_sync = datetime.now().strftime("%d/%m/%Y às %H:%M")
_n_reent = len(df_reent) if df_reent is not None else 0

st.markdown(f"""
<div class="topbar">
  <div class="tb-left">
    <div class="tb-icon">📦</div>
    <div>
      <p class="tb-title">GESTÃO DE DEVOLUÇÕES DELLY'S</p>
      <p class="tb-sub">Módulo de análise e controle operacional</p>
    </div>
  </div>
  <div class="tb-right">
    <div class="tb-chip"><span class="dot"></span> Sincronizado {_sync}</div>
    <div class="tb-chip bell">🔔<span class="tb-badge">{min(_n_reent, 99)}</span></div>
    <div class="tb-user">
      <div class="tb-av">DL</div>
      <div>
        <div class="tb-un">Delly's Logística</div>
        <div class="tb-ur">Roteirização</div>
      </div>
    </div>
    <div class="tb-chip">⚙️ Perfil</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# MENU LATERAL
# ═════════════════════════════════════════════════════════════════════════════
PAGINAS = [
    "📊  Dashboard",
    "🔄  Reentregas",
    "🔍  Detalhes Reentregas",
    "🗂️  Campos",
    "📑  Dados Completos",
    "👥  Clientes",
    "❗  Motivos",
    "🚚  Veículos",
    "📤  Relatórios",
    "⚙️  Configurações",
]

with st.sidebar:
    st.markdown("""
    <div class="side-brand">
      <div class="side-mark">📦</div>
      <div>
        <div class="side-brand-t">Delly's Food Service</div>
        <div class="side-brand-s">Logística</div>
      </div>
    </div>
    <div class="side-cap">Navegação</div>
    """, unsafe_allow_html=True)

    pagina = st.radio("Navegação", PAGINAS, label_visibility="collapsed", key="nav")

    st.markdown(f"""
    <div class="side-foot">
      Devoluções carregadas: <b style="color:#38bdf8;">{len(df_raw)}</b><br>
      Reentregas carregadas: <b style="color:#34d399;">{_n_reent}</b><br>
      Cache: 60s
    </div>
    """, unsafe_allow_html=True)

pagina = pagina.split("  ", 1)[-1].strip()


# ═════════════════════════════════════════════════════════════════════════════
# FILTROS GLOBAIS (devoluções) — mesma lógica de filtragem do sistema atual
# ═════════════════════════════════════════════════════════════════════════════
PAGS_COM_FILTRO = {"Dashboard", "Campos", "Dados Completos", "Clientes", "Motivos", "Veículos", "Relatórios"}

usar_data = False
dt_sel = None
sel_dev = []
sel_motivo = []

if pagina in PAGS_COM_FILTRO:
    st.markdown('<div class="filters"><div class="filters-h"><span class="pip"></span>Filtros — devoluções</div>',
                unsafe_allow_html=True)
    fc1, fc2, fc3, fc4, fc5 = st.columns([3, 2.4, 2.4, 1.3, 1], gap="medium")

    with fc1:
        datas_ok = df_raw["_DTENTREGA_DT"].dropna()
        if len(datas_ok) > 0:
            datas_unicas = sorted(datas_ok.dt.date.unique())
            opcoes_data = ["— Todas as datas —"] + [d.strftime("%d/%m/%Y") for d in datas_unicas]
            sel_data_str = st.selectbox("Data", opcoes_data, key="g_dtsel")
            if sel_data_str != "— Todas as datas —":
                dt_sel = datetime.strptime(sel_data_str, "%d/%m/%Y").date()
                usar_data = True
        else:
            st.caption("Sem datas válidas na coluna de data.")

    with fc2:
        if COL_DEVOLUCION:
            devs_opts = sorted([x for x in df_raw[COL_DEVOLUCION].unique() if x not in ("", "N/D", "nan", "None")])
            sel_dev = st.multiselect("Devolucionista", devs_opts, default=[], key="g_dev", placeholder="Todos")

    with fc3:
        if COL_MOTIVO:
            mot_opts = sorted([x for x in df_raw[COL_MOTIVO].unique() if x not in ("", "N/D", "nan", "None")])
            sel_motivo = st.multiselect("Motivo", mot_opts, default=[], key="g_mot", placeholder="Todos")

    with fc4:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        if st.button("Atualizar dados", use_container_width=True, type="primary", key="btn_upd_main"):
            st.cache_data.clear()
            st.rerun()

    with fc5:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        if st.button("Limpar", use_container_width=True, key="btn_clear"):
            for k in ("g_dtsel", "g_dev", "g_mot"):
                st.session_state.pop(k, None)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ── Aplica filtros (lógica idêntica à original) ─────────────────────────────
df = df_raw.copy()
if usar_data and dt_sel:
    df = df[df["_DTENTREGA_DT"].dt.date == dt_sel]
if sel_dev and COL_DEVOLUCION:
    df = df[df[COL_DEVOLUCION].isin(sel_dev)]
if sel_motivo and COL_MOTIVO:
    df = df[df[COL_MOTIVO].isin(sel_motivo)]

total_val = df[VALOR_COL].sum()
total_notas = len(df)
total_clientes = df[COL_CLIENTE].nunique() if COL_CLIENTE else 0
ticket_medio = total_val / total_notas if total_notas > 0 else 0
total_placas = df[COL_PLACA].nunique() if COL_PLACA else 0

if pagina in PAGS_COM_FILTRO:
    filtros_info = []
    if usar_data and dt_sel:
        filtros_info.append(f"Data {dt_sel.strftime('%d/%m/%Y')}")
    if sel_dev:
        filtros_info.append(f"Devolucionista: {', '.join(sel_dev[:2])}{'…' if len(sel_dev) > 2 else ''}")
    if sel_motivo:
        filtros_info.append(f"{len(sel_motivo)} motivo(s)")
    if filtros_info:
        st.info(f"{' · '.join(filtros_info)} — **{total_notas} registros filtrados**")


# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE GRÁFICO
# ═════════════════════════════════════════════════════════════════════════════
def make_combo_chart(df_data, x_col, val_col, qtd_col, title, periodo="", bar_colors=None):
    """Barras = Valor (R$) · Linha = Quantidade. Mesmos dados, apresentação limpa."""
    n = len(df_data)
    if bar_colors is None:
        bar_colors = ramp(n)
    fig = go.Figure()

    max_val = df_data[val_col].max() if len(df_data) > 0 else 1
    max_qtd = df_data[qtd_col].max() if len(df_data) > 0 else 1

    # Evita colisão entre o rótulo da linha e o topo da barra
    qtd_labels = []
    for val, qtd in zip(df_data[val_col], df_data[qtd_col]):
        bar_pos = float(val) / (max_val * 1.45) if max_val > 0 else 0
        line_pos = float(qtd) / (max_qtd * 3.8) if max_qtd > 0 else 0
        if abs(bar_pos - line_pos) < 0.09:
            qtd_labels.append(f"<b>{qtd}</b><br> ")
        else:
            qtd_labels.append(f"<b>{qtd}</b>")

    fig.add_trace(go.Bar(
        x=df_data[x_col], y=df_data[val_col], name="Valor (R$)",
        marker=dict(color=bar_colors, opacity=0.92,
                    line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
        text=[fmt_brl0(v) for v in df_data[val_col]],
        textposition="outside",
        textfont=dict(size=13, color="#e8f1fb", family="JetBrains Mono"),
        hovertemplate="<b>%{x}</b><br>Valor: %{text}<extra></extra>", yaxis="y1",
    ))
    fig.add_trace(go.Scatter(
        x=df_data[x_col], y=df_data[qtd_col], name="Quantidade",
        mode="lines+markers+text",
        text=qtd_labels, textposition="top center",
        textfont=dict(color="#fcd34d", size=12, family="JetBrains Mono"),
        line=dict(color="#fbbf24", width=2, shape="spline"),
        marker=dict(color="#fde68a", size=7, line=dict(color="#fbbf24", width=1.5)),
        hovertemplate="<b>%{x}</b><br>Quantidade: %{y}<extra></extra>", yaxis="y2",
    ))
    h = max(500, min(n * 44, 760))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b9c8dc", family="Inter"),
        height=h, margin=dict(t=64, b=86, l=10, r=30),
        hoverlabel=HOVER,
        title=dict(text=f"<span style='font-size:12px;color:#7c8ea8'>{periodo}</span>",
                   x=0.5, xanchor="center", y=0.985),
        bargap=0.34,
        xaxis=dict(tickfont=dict(color="#a9bcd4", size=12, family="JetBrains Mono"),
                   gridcolor="rgba(0,0,0,0)", linecolor="rgba(120,170,225,0.10)",
                   zeroline=False, tickangle=-38, automargin=True),
        yaxis=dict(showticklabels=False, gridcolor=GRID, zeroline=False,
                   side="left", range=[0, max_val * 1.45]),
        yaxis2=dict(showticklabels=False, overlaying="y", side="right", showgrid=False,
                    zeroline=False, range=[0, max_qtd * 3.8]),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
                    font=dict(color="#8fa3bd", size=12),
                    orientation="h", x=1.0, xanchor="right", y=1.10),
    )
    return fig


def make_bar_simple(df_data, x_col, y_col, bar_colors, title_txt="", ylabel="Qtd"):
    """Barras verticais simples (quantidade)."""
    n = len(df_data)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_data[x_col], y=df_data[y_col],
        marker=dict(color=bar_colors[:n], opacity=0.92,
                    line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
        text=[str(v) for v in df_data[y_col]], textposition="outside",
        textfont=dict(size=12, color="#e8f1fb", family="JetBrains Mono"),
        hovertemplate="<b>%{x}</b><br>" + ylabel + ": %{y}<extra></extra>",
    ))
    h = max(400, min(n * 40, 600))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b9c8dc", family="Inter"),
        height=h, margin=dict(t=40 if title_txt else 16, b=96, l=10, r=16),
        hoverlabel=HOVER,
        title=dict(text=f"<span style='font-size:12px;color:#7c8ea8'>{title_txt}</span>",
                   x=0.5, xanchor="center") if title_txt else None,
        bargap=0.34,
        xaxis=dict(tickfont=dict(color="#a9bcd4", size=11, family="JetBrains Mono"),
                   gridcolor="rgba(0,0,0,0)", linecolor="rgba(120,170,225,0.10)",
                   zeroline=False, tickangle=-38, automargin=True),
        yaxis=dict(showticklabels=False, gridcolor=GRID, zeroline=False),
    )
    return fig


def make_hbar(df_data, x_col, y_col, color_scale, height=400, money=True):
    fig = px.bar(df_data, x=x_col, y=y_col, orientation="h",
                 color=x_col, color_continuous_scale=color_scale,
                 text=[fmt_brl0(v) if money else f"<b>{v}</b>" for v in df_data[x_col]],
                 labels={y_col: "", x_col: "R$" if money else "Qtd"})
    fig.update_traces(textposition="outside",
                      textfont=dict(size=12, color="#cfe0f2", family="JetBrains Mono"),
                      cliponaxis=False, marker_line_width=0,
                      hovertemplate="<b>%{y}</b><br>%{x}<extra></extra>")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b9c8dc", family="Inter"), coloraxis_showscale=False,
        height=height, margin=dict(t=8, b=26, l=6, r=96), hoverlabel=HOVER,
        xaxis=dict(tickfont=dict(color="#7c8ea8", size=11), gridcolor=GRID,
                   tickformat=",.0f", zeroline=False),
        yaxis=dict(tickfont=dict(color="#cfe0f2", size=12, family="Inter"),
                   gridcolor="rgba(0,0,0,0)", automargin=True),
    )
    return fig


def kpi(icon, label, value, sub, accent, delta=None):
    """delta: (texto, 'up'|'down'|'flat') — exibido apenas quando disponível."""
    d = ""
    if delta:
        d = f'<span class="kpi-delta kpi-{delta[1]}">{delta[0]}</span>'
    return (f'<div class="kpi" style="--acc:{accent};">'
            f'<div class="kpi-top"><div class="kpi-ico">{icon}</div>{d}</div>'
            f'<div class="kpi-val">{value}</div>'
            f'<div class="kpi-lab">{label}</div>'
            f'<div class="kpi-sub">{sub}</div></div>')


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
if pagina == "Dashboard":

    # Indicador de evolução: mesma comparação já usada na seção semanal
    delta_val = None
    if usar_data and dt_sel:
        _prev = dt_sel - pd.Timedelta(days=7)
        if hasattr(_prev, "date"):
            _prev = _prev.date()
        _tot_prev = df_raw[df_raw["_DTENTREGA_DT"].dt.date == _prev][VALOR_COL].sum()
        if _tot_prev > 0:
            _p = (total_val - _tot_prev) / _tot_prev * 100
            delta_val = (f"{_p:+.1f}%", "up" if _p > 0 else "down" if _p < 0 else "flat")

    st.markdown(
        '<div class="kpi-grid">'
        + kpi("💰", "Valor total devolvido", fmt_brl(total_val), "Soma de VLTOTAL no filtro", "#22d3ee", delta_val)
        + kpi("📄", "Devoluções", f"{total_notas}", "Notas no filtro atual", "#a78bfa")
        + kpi("👥", "Clientes únicos", f"{total_clientes}", "Clientes com devolução", "#34d399")
        + kpi("📈", "Ticket médio", fmt_brl(ticket_medio), "Valor por devolução", "#fbbf24")
        + kpi("🚚", "Veículos únicos", f"{total_placas}", "Placas envolvidas", "#fb923c")
        + '</div>', unsafe_allow_html=True)

    # ── ÁREA 1 — gráfico principal + acumulado ──────────────────────────────
    col_graf, col_acum = st.columns([3, 1.35], gap="medium")

    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    df_mes = pd.DataFrame()
    if "_DTENTREGA_DT" in df_raw.columns:
        df_mes = df_raw[
            (df_raw["_DTENTREGA_DT"].dt.date >= primeiro_dia_mes) &
            (df_raw["_DTENTREGA_DT"].dt.date <= hoje)
        ].copy()

    with col_graf:
        periodo = (f"DTENT: {dt_sel.strftime('%d/%m/%Y')}" if usar_data and dt_sel
                   else "Todos os períodos")
        panel_open("Devoluções por placa — valor e quantidade", tag=periodo, icon="🚚")
        if COL_PLACA:
            df_placa = (df[df[COL_PLACA].str.strip() != ""]
                        .groupby(COL_PLACA).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                        .reset_index().sort_values("Valor", ascending=False))
            if not df_placa.empty:
                st.plotly_chart(
                    make_combo_chart(df_placa, COL_PLACA, "Valor", "Qtd", "", periodo, ramp(len(df_placa))),
                    use_container_width=True)
                st.markdown(
                    '<div style="display:flex;gap:20px;flex-wrap:wrap;font-size:0.7rem;color:#4e5f78;'
                    'margin-top:-14px;padding-left:4px;">'
                    '<span>● Top 5 crítico</span><span>● 6–10 atenção</span>'
                    '<span>● Demais</span><span>● Linha: quantidade de notas</span></div>',
                    unsafe_allow_html=True)
            else:
                st.info("Nenhuma placa no filtro atual. Ajuste a data ou limpe os filtros.")
        else:
            st.warning("Coluna PLACA não encontrada na planilha.")
        panel_close()

    with col_acum:
        panel_open("Acumulado", tag=hoje.strftime("%m/%Y"), icon="📈")
        if not df_mes.empty:
            df_mes_dia = (df_mes.assign(_DIA=df_mes["_DTENTREGA_DT"].dt.date)
                          .groupby("_DIA").agg(Valor=(VALOR_COL, "sum")).reset_index()
                          .sort_values("_DIA"))
            df_mes_dia["Acumulado"] = df_mes_dia["Valor"].cumsum()
            total_mes = df_mes_dia["Acumulado"].iloc[-1] if len(df_mes_dia) > 0 else 0
            valor_hoje = df_mes_dia.loc[df_mes_dia["_DIA"] == hoje, "Valor"].sum()

            fig_acum = go.Figure()
            fig_acum.add_trace(go.Scatter(
                x=df_mes_dia["_DIA"], y=df_mes_dia["Acumulado"],
                mode="lines", fill="tozeroy",
                line=dict(color="#22d3ee", width=2, shape="spline"),
                fillcolor="rgba(34,211,238,0.10)",
                hovertemplate="<b>%{x}</b><br>Acumulado: R$ %{y:,.0f}<extra></extra>",
            ))
            fig_acum.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#b9c8dc", family="Inter", size=10),
                height=468, margin=dict(t=8, b=26, l=6, r=6), hoverlabel=HOVER,
                xaxis=dict(tickfont=dict(size=10, color="#7c8ea8"), showgrid=False,
                           linecolor="rgba(120,170,225,0.10)"),
                yaxis=dict(tickfont=dict(size=10, color="#7c8ea8"),
                           gridcolor=GRID, tickformat=",.0f", zeroline=False),
                showlegend=False,
            )
            st.plotly_chart(fig_acum, use_container_width=True)
            st.markdown(
                f'<p style="font-size:0.72rem;color:#7c8ea8;text-align:center;margin-top:-12px;">'
                f'Hoje <b class="num" style="color:#fbbf24;">{fmt_brl0(valor_hoje)}</b> &nbsp;·&nbsp; '
                f'Mês <b class="num" style="color:#34d399;">{fmt_brl0(total_mes)}</b></p>',
                unsafe_allow_html=True)
        else:
            st.info("Nenhum lançamento no mês corrente ainda.")
        panel_close()

    # ── ÁREA 2 — três painéis ───────────────────────────────────────────────
    a1, a2, a3 = st.columns(3, gap="medium")

    with a1:
        panel_open("Devoluções por motivo", tag="Valor", icon="❗")
        if COL_MOTIVO:
            df_m_top = (df[df[COL_MOTIVO].str.strip() != ""]
                        .groupby(COL_MOTIVO).agg(Valor=(VALOR_COL, "sum"))
                        .reset_index().sort_values("Valor", ascending=True).tail(8))
            if not df_m_top.empty:
                st.plotly_chart(make_hbar(df_m_top, "Valor", COL_MOTIVO, RED, 380), use_container_width=True)
            else:
                st.info("Sem motivos no filtro atual.")
        panel_close()

    with a2:
        panel_open("Devoluções por veículo", tag="Quantidade", icon="🚚")
        if COL_PLACA:
            df_v_top = (df[df[COL_PLACA].str.strip() != ""]
                        .groupby(COL_PLACA).agg(Qtd=(VALOR_COL, "count"))
                        .reset_index().sort_values("Qtd", ascending=True).tail(8))
            if not df_v_top.empty:
                st.plotly_chart(make_hbar(df_v_top, "Qtd", COL_PLACA, BLUE, 380, money=False),
                                use_container_width=True)
            else:
                st.info("Sem veículos no filtro atual.")
        panel_close()

    with a3:
        panel_open("Evolução diária", tag="Mês corrente", icon="📊")
        if not df_mes.empty:
            df_ev = (df_mes.assign(_DIA=df_mes["_DTENTREGA_DT"].dt.date)
                     .groupby("_DIA").agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                     .reset_index().sort_values("_DIA"))
            fig_ev = go.Figure()
            fig_ev.add_trace(go.Bar(
                x=df_ev["_DIA"], y=df_ev["Valor"], name="Valor",
                marker=dict(color="rgba(34,211,238,0.55)", line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>Valor: R$ %{y:,.0f}<extra></extra>"))
            fig_ev.add_trace(go.Scatter(
                x=df_ev["_DIA"], y=df_ev["Qtd"], name="Qtd", yaxis="y2",
                mode="lines", line=dict(color="#a78bfa", width=2, shape="spline"),
                hovertemplate="<b>%{x}</b><br>Notas: %{y}<extra></extra>"))
            fig_ev.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#b9c8dc", family="Inter", size=10),
                height=380, margin=dict(t=8, b=26, l=6, r=6), hoverlabel=HOVER,
                bargap=0.4,
                xaxis=dict(tickfont=dict(size=10, color="#7c8ea8"), showgrid=False,
                           linecolor="rgba(120,170,225,0.10)"),
                yaxis=dict(tickfont=dict(size=10, color="#7c8ea8"), gridcolor=GRID,
                           tickformat=",.0f", zeroline=False),
                yaxis2=dict(overlaying="y", side="right", showgrid=False,
                            tickfont=dict(size=10, color="#a78bfa"), zeroline=False),
                legend=dict(orientation="h", x=1, xanchor="right", y=1.16,
                            bgcolor="rgba(0,0,0,0)", font=dict(size=11, color="#7c8ea8")),
            )
            st.plotly_chart(fig_ev, use_container_width=True)
        else:
            st.info("Nenhum lançamento no mês corrente ainda.")
        panel_close()

    # ── Comparação semanal por placa (lógica original preservada) ───────────
    if COL_PLACA:
        dia_ref = dt_sel if (usar_data and dt_sel) else date.today()
        dia_sem_passada = dia_ref - pd.Timedelta(days=7)
        dias_semana_pt = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
                          "Sexta-feira", "Sábado", "Domingo"]
        nome_dia = dias_semana_pt[dia_ref.weekday()]

        if "_DTENTREGA_DT" in df_raw.columns:
            df_atual_dia = df_raw[
                (df_raw["_DTENTREGA_DT"].dt.date == dia_ref) & (df_raw[COL_PLACA].str.strip() != "")
            ].groupby(COL_PLACA).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count")).reset_index()
            df_semana_dia = df_raw[
                (df_raw["_DTENTREGA_DT"].dt.date == dia_sem_passada) & (df_raw[COL_PLACA].str.strip() != "")
            ].groupby(COL_PLACA).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count")).reset_index()
        else:
            df_atual_dia = pd.DataFrame(columns=[COL_PLACA, "Valor", "Qtd"])
            df_semana_dia = pd.DataFrame(columns=[COL_PLACA, "Valor", "Qtd"])

        todas_placas_comp = sorted(set(df_atual_dia[COL_PLACA]))

        if todas_placas_comp:
            df_comp = pd.DataFrame({COL_PLACA: todas_placas_comp})
            df_comp = df_comp.merge(df_atual_dia.rename(columns={"Valor": "Valor_Atual", "Qtd": "Qtd_Atual"}),
                                    on=COL_PLACA, how="left")
            df_comp = df_comp.merge(df_semana_dia.rename(columns={"Valor": "Valor_Semana", "Qtd": "Qtd_Semana"}),
                                    on=COL_PLACA, how="left")
            df_comp[["Valor_Atual", "Qtd_Atual", "Valor_Semana", "Qtd_Semana"]] = \
                df_comp[["Valor_Atual", "Qtd_Atual", "Valor_Semana", "Qtd_Semana"]].fillna(0)
            df_comp = df_comp.sort_values("Valor_Atual", ascending=False)

            # Totais e variação — mesmas fórmulas de antes, apenas calculadas
            # antes da renderização para alimentar o cabeçalho e o rodapé do card.
            total_atual = df_comp["Valor_Atual"].sum()
            total_semana = df_comp["Valor_Semana"].sum()
            var_pct = ((total_atual - total_semana) / total_semana * 100) if total_semana > 0 else 0

            _lbl_ref = dia_ref.strftime("%d/%m")
            _lbl_ant = dia_sem_passada.strftime("%d/%m")

            with st.container(border=True):
                # ── Cabeçalho do card ───────────────────────────────────────
                st.markdown(f"""
                <div class="cc-head">
                  <div class="cc-head-l">
                    <p class="cc-title">Devoluções por placa — valor e quantidade</p>
                    <p class="cc-sub">Comparativo: {_lbl_ref} (referência) vs {_lbl_ant} (semana passada) · {nome_dia}</p>
                  </div>
                  <div class="cc-head-r">
                    <div class="cc-mini">
                      <span class="cc-mini-lab">Total {_lbl_ref}</span>
                      <span class="cc-mini-val" style="color:#34d399;">{fmt_brl0(total_atual)}</span>
                      <span class="cc-mini-sub">valor devolvido</span>
                    </div>
                    <div class="cc-mini">
                      <span class="cc-mini-lab">Total {_lbl_ant}</span>
                      <span class="cc-mini-val" style="color:#60a5fa;">{fmt_brl0(total_semana)}</span>
                      <span class="cc-mini-sub">valor devolvido</span>
                    </div>
                    <div class="cc-ctrls">
                      <span class="cc-pick">Por placa ▾</span>
                      <span class="cc-dots">⋮</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Tooltip único por placa (mesmos números do gráfico) ─────
                cdata = [[fmt_brl0(va), fmt_brl0(vs), int(qa), int(qs)]
                         for va, vs, qa, qs in zip(df_comp["Valor_Atual"], df_comp["Valor_Semana"],
                                                   df_comp["Qtd_Atual"], df_comp["Qtd_Semana"])]
                htmpl = (f"<b>Placa %{{x}}</b><br>"
                         f"<span style='color:#34d399'>●</span> {_lbl_ref} — %{{customdata[0]}}<br>"
                         f"<span style='color:#60a5fa'>●</span> {_lbl_ant} — %{{customdata[1]}}<br>"
                         f"<span style='color:#fbbf24'>●</span> Notas {_lbl_ref} — %{{customdata[2]}}<br>"
                         f"<span style='color:#f87171'>●</span> Notas {_lbl_ant} — %{{customdata[3]}}"
                         f"<extra></extra>")

                n_comp = len(df_comp)
                max_qtd_comp = max(df_comp["Qtd_Atual"].max(), df_comp["Qtd_Semana"].max(), 1)
                max_val_comp = max(df_comp["Valor_Atual"].max(), df_comp["Valor_Semana"].max(), 1)

                # Rótulos da quantidade: afasta o texto quando ele encostaria
                # no topo da barra, evitando sobreposição.
                lab_ref, lab_ant = [], []
                for va, vs, qa, qs in zip(df_comp["Valor_Atual"], df_comp["Valor_Semana"],
                                          df_comp["Qtd_Atual"], df_comp["Qtd_Semana"]):
                    bar_ref = float(va) / (max_val_comp * 1.55)
                    bar_ant = float(vs) / (max_val_comp * 1.55)
                    ln_ref = float(qa) / (max_qtd_comp * 3.6)
                    ln_ant = float(qs) / (max_qtd_comp * 3.6)
                    lab_ref.append(f"<b>{int(qa)}</b><br> " if abs(bar_ref - ln_ref) < 0.08 else f"<b>{int(qa)}</b>")
                    lab_ant.append(f"<b>{int(qs)}</b><br> " if abs(bar_ant - ln_ant) < 0.08 else f"<b>{int(qs)}</b>")

                fig_comp = go.Figure()
                fig_comp.add_trace(go.Bar(
                    x=df_comp[COL_PLACA], y=df_comp["Valor_Semana"],
                    name=f"{_lbl_ant} — semana passada",
                    marker=dict(color="rgba(96,165,250,0.42)",
                                line=dict(color="rgba(96,165,250,0.55)", width=1)),
                    text=[fmt_brl0(v) for v in df_comp["Valor_Semana"]], textposition="outside",
                    textfont=dict(size=11, color="#9dc2f7", family="JetBrains Mono"),
                    customdata=cdata, hovertemplate=htmpl))
                fig_comp.add_trace(go.Bar(
                    x=df_comp[COL_PLACA], y=df_comp["Valor_Atual"],
                    name=f"{_lbl_ref} — referência",
                    marker=dict(color="rgba(52,211,153,0.72)",
                                line=dict(color="rgba(52,211,153,0.85)", width=1)),
                    text=[fmt_brl0(v) for v in df_comp["Valor_Atual"]], textposition="outside",
                    textfont=dict(size=12, color="#eaf6ff", family="JetBrains Mono"),
                    customdata=cdata, hovertemplate=htmpl))
                fig_comp.add_trace(go.Scatter(
                    x=df_comp[COL_PLACA], y=df_comp["Qtd_Semana"],
                    name="Semana passada", mode="lines+markers+text",
                    text=lab_ant, textposition="bottom center",
                    textfont=dict(color="#fca5a5", size=10, family="JetBrains Mono"),
                    line=dict(color="#f87171", width=1.5, dash="dot", shape="spline"),
                    marker=dict(color="#fca5a5", size=6, line=dict(color="rgba(4,7,15,0.9)", width=1)),
                    customdata=cdata, hovertemplate=htmpl, yaxis="y2"))
                fig_comp.add_trace(go.Scatter(
                    x=df_comp[COL_PLACA], y=df_comp["Qtd_Atual"],
                    name="Essa semana", mode="lines+markers+text",
                    text=lab_ref, textposition="top center",
                    textfont=dict(color="#fcd34d", size=11, family="JetBrains Mono"),
                    line=dict(color="#fbbf24", width=2, shape="spline"),
                    marker=dict(color="#fde68a", size=7, line=dict(color="rgba(4,7,15,0.9)", width=1)),
                    customdata=cdata, hovertemplate=htmpl, yaxis="y2"))

                fig_comp.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#b9c8dc", family="Inter"),
                    height=max(460, min(n_comp * 52, 700)),
                    margin=dict(t=58, b=86, l=8, r=8),
                    separators=",.",
                    hovermode="closest",
                    hoverlabel=dict(bgcolor="rgba(8,14,28,0.97)", bordercolor="rgba(56,189,248,0.35)",
                                    font=dict(color="#e8f4ff", family="Inter", size=12.5),
                                    align="left"),
                    barmode="group", bargap=0.40, bargroupgap=0.10,
                    xaxis=dict(tickfont=dict(color="#a9bcd4", size=11, family="JetBrains Mono"),
                               showgrid=False, linecolor="rgba(120,170,225,0.12)",
                               zeroline=False, tickangle=-38, automargin=True),
                    yaxis=dict(title=dict(text="Valor (R$)",
                                          font=dict(color="#6d8099", size=11, family="Inter")),
                               showticklabels=False,
                               gridcolor="rgba(120,170,225,0.055)", zeroline=False,
                               range=[0, max_val_comp * 1.55], nticks=5),
                    yaxis2=dict(title=dict(text="Quantidade (notas)",
                                           font=dict(color="#6d8099", size=11, family="Inter")),
                                overlaying="y", side="right", showgrid=False, zeroline=False,
                                showticklabels=False,
                                range=[0, max_qtd_comp * 3.6], nticks=4),
                    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
                                font=dict(color="#8fa3bd", size=11.5),
                                orientation="h", x=0.5, xanchor="center", y=1.11,
                                itemsizing="constant"),
                )
                st.plotly_chart(fig_comp, use_container_width=True,
                                config={"displayModeBar": False})

                # ── Rodapé do card ──────────────────────────────────────────
                _var_cor = "#f87171" if var_pct > 0 else "#34d399" if var_pct < 0 else "#8fa3bd"
                _var_seta = "▲" if var_pct > 0 else "▼" if var_pct < 0 else "■"
                st.markdown(f"""
                <div class="cc-foot">
                  <div class="cc-foot-i">
                    <span class="cc-foot-lab"><i class="d" style="background:#34d399;"></i>{_lbl_ref} — referência</span>
                    <span class="cc-foot-val" style="color:#34d399;">{fmt_brl0(total_atual)}</span>
                  </div>
                  <div class="cc-foot-sep"></div>
                  <div class="cc-foot-i">
                    <span class="cc-foot-lab"><i class="d" style="background:#60a5fa;"></i>{_lbl_ant} — semana passada</span>
                    <span class="cc-foot-val" style="color:#93c5fd;">{fmt_brl0(total_semana)}</span>
                  </div>
                  <div class="cc-foot-sep"></div>
                  <div class="cc-foot-i">
                    <span class="cc-foot-lab">Variação</span>
                    <span class="cc-foot-val" style="color:{_var_cor};">{_var_seta} {var_pct:+.1f}%</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            panel_open(f"Comparação por placa — {nome_dia}",
                       tag=f"{dia_ref.strftime('%d/%m')} × {dia_sem_passada.strftime('%d/%m')}", icon="📆")
            st.info("Sem registros de placa nas datas comparadas.")
            panel_close()

    # ── Ocorrências de retorno ──────────────────────────────────────────────
    if COL_MOTIVO:
        panel_open("Ocorrências de retorno", tag="Valor e quantidade", icon="❗")
        df_mot_v = (df[df[COL_MOTIVO].str.strip() != ""]
                    .groupby(COL_MOTIVO).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                    .reset_index().sort_values("Valor", ascending=False))
        if not df_mot_v.empty:
            n_m = len(df_mot_v)
            fig_mv = make_combo_chart(df_mot_v, COL_MOTIVO, "Valor", "Qtd", "", "", ramp(n_m, 3, 6))
            fig_mv.update_layout(height=max(430, min(n_m * 58, 660)), margin=dict(t=54, b=110, l=10, r=30))
            fig_mv.update_xaxes(tickangle=-35, automargin=True)
            st.plotly_chart(fig_mv, use_container_width=True)
            with st.expander("Ver tabela de motivos"):
                df_mt = df_mot_v.copy()
                df_mt["Valor (R$)"] = df_mt["Valor"].apply(fmt_brl)
                df_mt["% Total"] = (df_mt["Valor"] / total_val * 100).round(1).astype(str) + "%" if total_val > 0 else "0%"
                df_mt = df_mt.rename(columns={COL_MOTIVO: "Motivo", "Qtd": "Qtd."})
                html_table(df_mt[["Motivo", "Qtd.", "Valor (R$)", "% Total"]], max_rows=200, min_width=600)
        else:
            st.info("Sem ocorrências no filtro atual.")
        panel_close()

    # ── Rankings ────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        panel_open("Top motivos", tag="R$", icon="❗")
        if COL_MOTIVO:
            df_m2 = (df[df[COL_MOTIVO].str.strip() != ""]
                     .groupby(COL_MOTIVO).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                     .reset_index().sort_values("Valor", ascending=True).tail(8))
            if not df_m2.empty:
                st.plotly_chart(make_hbar(df_m2, "Valor", COL_MOTIVO, RED, 400), use_container_width=True)
                top = df_m2.iloc[-1]
                pct = top["Valor"] / total_val * 100 if total_val > 0 else 0
                st.markdown(f'<p style="font-size:0.73rem;color:#7c8ea8;padding:0 4px 10px;">'
                            f'{top[COL_MOTIVO]} — {pct:.1f}% ({fmt_brl0(top["Valor"])})</p>',
                            unsafe_allow_html=True)
        panel_close()
    with c2:
        panel_open("Top 10 clientes", tag="R$", icon="👥")
        if COL_CLIENTE:
            df_cl = (df[df[COL_CLIENTE].str.strip() != ""]
                     .groupby(COL_CLIENTE).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                     .reset_index().sort_values("Valor", ascending=True).tail(10))
            if not df_cl.empty:
                st.plotly_chart(make_hbar(df_cl, "Valor", COL_CLIENTE, MIXED, 400), use_container_width=True)
                top_c = df_cl.iloc[-1]
                st.markdown(f'<p style="font-size:0.73rem;color:#7c8ea8;padding:0 4px 10px;">'
                            f'{str(top_c[COL_CLIENTE])[:30]} — {fmt_brl0(top_c["Valor"])}</p>',
                            unsafe_allow_html=True)
        panel_close()
    with c3:
        panel_open("Top 10 vendedores", tag="NOMERCA", icon="🧑‍💼")
        if COL_VENDEDOR:
            df_vv = (df[df[COL_VENDEDOR].str.strip() != ""]
                     .groupby(COL_VENDEDOR).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                     .reset_index().sort_values("Valor", ascending=True).tail(10))
            if not df_vv.empty:
                st.plotly_chart(make_hbar(df_vv, "Valor", COL_VENDEDOR, BLUE, 400), use_container_width=True)
                top_v = df_vv.iloc[-1]
                st.markdown(f'<p style="font-size:0.73rem;color:#7c8ea8;padding:0 4px 10px;">'
                            f'{str(top_v[COL_VENDEDOR])[:30]} — {int(top_v["Qtd"])} devoluções</p>',
                            unsafe_allow_html=True)
        panel_close()

    c4, c5 = st.columns([1, 2], gap="medium")
    with c4:
        panel_open("Por destino", tag="Top 10", icon="🏙️")
        if COL_DESTINO:
            df_dd = (df[df[COL_DESTINO].str.strip() != ""]
                     .groupby(COL_DESTINO).agg(Valor=(VALOR_COL, "sum"))
                     .reset_index().sort_values("Valor", ascending=False).head(10))
            if not df_dd.empty:
                fig_dd = px.pie(df_dd, names=COL_DESTINO, values="Valor",
                                color_discrete_sequence=MIXED, hole=0.62)
                fig_dd.update_traces(textfont=dict(size=12, color="#e8f1fb"),
                                     marker=dict(line=dict(color="rgba(4,7,15,0.9)", width=2)))
                st.plotly_chart(plotly_dark(fig_dd, height=360), use_container_width=True)
        panel_close()
    with c5:
        panel_open("Ranking de motivos", tag="Consolidado", icon="📊")
        if COL_MOTIVO:
            df_rk = (df.groupby(COL_MOTIVO).agg(Qtd=(VALOR_COL, "count"), Total=(VALOR_COL, "sum"))
                     .reset_index().sort_values("Total", ascending=False))
            df_rk["Valor Total"] = df_rk["Total"].apply(fmt_brl)
            df_rk["% Total"] = (df_rk["Total"] / total_val * 100).round(1).astype(str) + "%" if total_val > 0 else "0%"
            html_table(df_rk.rename(columns={COL_MOTIVO: "Motivo"})[["Motivo", "Qtd", "Valor Total", "% Total"]],
                       max_rows=200, min_width=520)
        panel_close()


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: REENTREGAS
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Reentregas":
    if reent_load_error:
        st.error(f"Não foi possível carregar as reentregas: {reent_load_error}")
        st.markdown("""
**Como resolver**
1. Abra a planilha no Google Sheets.
2. Vá em **Arquivo → Compartilhar → Publicar na web**.
3. Selecione a aba **8261 - REENTREGAS 2026**.
4. Clique em **Publicar** e confirme.
5. Volte aqui e use **Atualizar dados**.
        """)
        with st.expander("URLs tentadas"):
            for u in REENTREGAS_URLS:
                st.code(u)
    elif df_reent is None or len(df_reent) == 0:
        st.warning("Nenhum dado encontrado na aba de reentregas.")
    else:
        st.markdown('<div class="filters"><div class="filters-h"><span class="pip"></span>'
                    'Filtros — reentregas</div>', unsafe_allow_html=True)
        rf1, rf2, rf3, rf4 = st.columns([3, 3, 1.3, 1], gap="medium")
        usar_data_reent = False
        dt_reent_sel = None

        with rf1:
            datas_reent_ok = df_reent["_DATATRANSF_DT"].dropna()
            dt_col_reent = reent_cols.get("DATATRANSF")
            col_label_reent = dt_col_reent if dt_col_reent else "DTRANSF"
            if len(datas_reent_ok) > 0:
                datas_reent_unicas = sorted(datas_reent_ok.dt.date.unique())
                opcoes_reent = ["— Todas as datas —"] + [d.strftime("%d/%m/%Y") for d in datas_reent_unicas]
                sel_reent_str = st.selectbox(f"Data ({col_label_reent})", opcoes_reent, key="r_dtsel")
                if sel_reent_str != "— Todas as datas —":
                    dt_reent_sel = datetime.strptime(sel_reent_str, "%d/%m/%Y").date()
                    usar_data_reent = True
            else:
                st.caption("Sem datas DTRANSF válidas.")

        with rf2:
            motivo_reent_col = reent_cols.get("MOTIVOTRANSF")
            if motivo_reent_col:
                mot_reent_opts = sorted([x for x in df_reent[motivo_reent_col].unique()
                                         if x not in ("", "N/D", "nan", "None")])
                sel_mot_reent = st.multiselect("Motivo da transferência", mot_reent_opts,
                                               default=[], key="r_mot", placeholder="Todos")
            else:
                sel_mot_reent = []

        with rf3:
            st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
            if st.button("Atualizar dados", use_container_width=True, type="primary", key="btn_reent"):
                st.cache_data.clear()
                st.rerun()
        with rf4:
            st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
            if st.button("Limpar", use_container_width=True, key="btn_clear_reent"):
                for k in ("r_dtsel", "r_mot"):
                    st.session_state.pop(k, None)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        df_r = df_reent.copy()
        if usar_data_reent and dt_reent_sel:
            df_r = df_r[df_r["_DATATRANSF_DT"].dt.date == dt_reent_sel]
        if sel_mot_reent and motivo_reent_col:
            df_r = df_r[df_r[motivo_reent_col].isin(sel_mot_reent)]

        if usar_data_reent and dt_reent_sel:
            st.info(f"Data {dt_reent_sel.strftime('%d/%m/%Y')} — **{len(df_r)} registros**")

        total_reent = len(df_r)
        total_reent_valor = df_r[REENT_VALOR_COL].sum() if REENT_VALOR_COL in df_r.columns else 0
        placaant_col = reent_cols.get("PLACAANT")
        cliente_r_col = reent_cols.get("CLIENTE")
        praca_r_col = reent_cols.get("PRACA")
        nome_r_col = reent_cols.get("NOME")
        motivo_r_col2 = reent_cols.get("MOTIVOTRANSF")
        total_placas_r = df_r[placaant_col].nunique() if placaant_col and placaant_col in df_r.columns else 0
        total_cli_r = df_r[cliente_r_col].nunique() if cliente_r_col and cliente_r_col in df_r.columns else 0
        ticket_r = total_reent_valor / total_reent if total_reent > 0 and total_reent_valor > 0 else 0
        total_pracas_r = df_r[praca_r_col].nunique() if praca_r_col and praca_r_col in df_r.columns else 0

        if total_reent_valor > 0:
            st.markdown(
                '<div class="kpi-grid">'
                + kpi("🔄", "Total de reentregas", f"{total_reent}", "Registros no filtro", "#fbbf24")
                + kpi("💰", "Valor total", fmt_brl(total_reent_valor), "Soma de VLTOTGER", "#22d3ee")
                + kpi("👥", "Clientes únicos", f"{total_cli_r}", "Clientes atendidos", "#34d399")
                + kpi("📈", "Ticket médio", fmt_brl(ticket_r), "Valor por reentrega", "#a78bfa")
                + kpi("🚚", "Placas anteriores", f"{total_placas_r}", "PLACAANT distintas", "#fb923c")
                + '</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="kpi-grid">'
                + kpi("🔄", "Total de reentregas", f"{total_reent}", "Registros no filtro", "#fbbf24")
                + kpi("👥", "Clientes únicos", f"{total_cli_r}", "Clientes atendidos", "#34d399")
                + kpi("🚚", "Placas anteriores", f"{total_placas_r}", "PLACAANT distintas", "#fb923c")
                + kpi("🗺️", "Praças", f"{total_pracas_r}", "Praças atendidas", "#a78bfa")
                + '</div>', unsafe_allow_html=True)

        g1, g2 = st.columns(2, gap="medium")
        with g1:
            panel_open("Reentregas por placa anterior", tag="PLACAANT", icon="🚚")
            if placaant_col and placaant_col in df_r.columns:
                df_pr = (df_r[df_r[placaant_col].str.strip() != ""]
                         .groupby(placaant_col).agg(Qtd=(placaant_col, "count"))
                         .reset_index().sort_values("Qtd", ascending=False))
                if not df_pr.empty:
                    st.plotly_chart(make_bar_simple(df_pr, placaant_col, "Qtd", ramp(len(df_pr), 3, 6, C_OK)),
                                    use_container_width=True)
                else:
                    st.info("Sem placas no filtro atual.")
            else:
                st.warning("Coluna PLACAANT não encontrada.")
            panel_close()

        with g2:
            panel_open("Reentregas por motivo", tag="MOTIVOTRANSF", icon="❗")
            if motivo_r_col2 and motivo_r_col2 in df_r.columns:
                df_mr = (df_r[df_r[motivo_r_col2].str.strip() != ""]
                         .groupby(motivo_r_col2).agg(Qtd=(motivo_r_col2, "count"))
                         .reset_index().sort_values("Qtd", ascending=False))
                if not df_mr.empty:
                    st.plotly_chart(make_bar_simple(df_mr, motivo_r_col2, "Qtd", ramp(len(df_mr), 3, 6)),
                                    use_container_width=True)
                else:
                    st.info("Sem motivos no filtro atual.")
            else:
                st.warning("Coluna MOTIVOTRANSF não encontrada.")
            panel_close()

        cr1, cr2, cr3 = st.columns(3, gap="medium")
        with cr1:
            panel_open("Principais motivos", tag="Qtd", icon="❗")
            if motivo_r_col2 and motivo_r_col2 in df_r.columns:
                df_mr2 = (df_r[df_r[motivo_r_col2].str.strip() != ""]
                          .groupby(motivo_r_col2).agg(Qtd=(motivo_r_col2, "count"))
                          .reset_index().sort_values("Qtd", ascending=True).tail(8))
                if not df_mr2.empty:
                    st.plotly_chart(make_hbar(df_mr2, "Qtd", motivo_r_col2, RED, 380, money=False),
                                    use_container_width=True)
            panel_close()
        with cr2:
            panel_open("Top 10 clientes", tag="Qtd", icon="👥")
            if cliente_r_col and cliente_r_col in df_r.columns:
                df_clr = (df_r[df_r[cliente_r_col].str.strip() != ""]
                          .groupby(cliente_r_col).agg(Qtd=(cliente_r_col, "count"))
                          .reset_index().sort_values("Qtd", ascending=True).tail(10))
                if not df_clr.empty:
                    st.plotly_chart(make_hbar(df_clr, "Qtd", cliente_r_col, MIXED, 380, money=False),
                                    use_container_width=True)
            panel_close()
        with cr3:
            panel_open("Top vendedores", tag="Qtd", icon="🧑‍💼")
            if nome_r_col and nome_r_col in df_r.columns:
                df_nomr = (df_r[df_r[nome_r_col].str.strip() != ""]
                           .groupby(nome_r_col).agg(Qtd=(nome_r_col, "count"))
                           .reset_index().sort_values("Qtd", ascending=True).tail(10))
                if not df_nomr.empty:
                    st.plotly_chart(make_hbar(df_nomr, "Qtd", nome_r_col, BLUE, 380, money=False),
                                    use_container_width=True)
            panel_close()

        cr4, cr5 = st.columns([1, 2], gap="medium")
        with cr4:
            panel_open("Por praça", tag="Top 10", icon="🏙️")
            if praca_r_col and praca_r_col in df_r.columns:
                df_praca_r = (df_r[df_r[praca_r_col].str.strip() != ""]
                              .groupby(praca_r_col).agg(Qtd=(praca_r_col, "count"))
                              .reset_index().sort_values("Qtd", ascending=False).head(10))
                if not df_praca_r.empty:
                    fig_pr = px.pie(df_praca_r, names=praca_r_col, values="Qtd",
                                    color_discrete_sequence=MIXED, hole=0.62)
                    fig_pr.update_traces(textfont=dict(size=12, color="#e8f1fb"),
                                         marker=dict(line=dict(color="rgba(4,7,15,0.9)", width=2)))
                    st.plotly_chart(plotly_dark(fig_pr, height=360), use_container_width=True)
            panel_close()
        with cr5:
            panel_open("Ranking de motivos de transferência", tag="Consolidado", icon="📊")
            if motivo_r_col2 and motivo_r_col2 in df_r.columns:
                df_rkr = (df_r.groupby(motivo_r_col2).agg(Qtd=(motivo_r_col2, "count"))
                          .reset_index().sort_values("Qtd", ascending=False))
                tot_r = df_rkr["Qtd"].sum()
                df_rkr["%"] = (df_rkr["Qtd"] / tot_r * 100).round(1).astype(str) + "%" if tot_r > 0 else "0%"
                html_table(df_rkr.rename(columns={motivo_r_col2: "Motivo"}), max_rows=200, min_width=480)
            panel_close()


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: DETALHES REENTREGAS
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Detalhes Reentregas":
    if df_reent is None or len(df_reent) == 0:
        st.warning("Nenhum dado de reentregas disponível.")
    else:
        st.markdown('<div class="filters"><div class="filters-h"><span class="pip"></span>'
                    'Pesquisa — reentregas</div>', unsafe_allow_html=True)
        det_f1, det_f2, det_f3 = st.columns([3, 1.3, 1], gap="medium")
        usar_data_det = False
        dt_det_sel = None
        with det_f1:
            datas_det_ok = df_reent["_DATATRANSF_DT"].dropna()
            dt_col_det = reent_cols.get("DATATRANSF")
            col_label_det = dt_col_det if dt_col_det else "DTRANSF"
            if len(datas_det_ok) > 0:
                datas_det_unicas = sorted(datas_det_ok.dt.date.unique())
                opcoes_det = ["— Todas as datas —"] + [d.strftime("%d/%m/%Y") for d in datas_det_unicas]
                sel_det_str = st.selectbox(f"Data ({col_label_det})", opcoes_det, key="det_dtsel")
                if sel_det_str != "— Todas as datas —":
                    dt_det_sel = datetime.strptime(sel_det_str, "%d/%m/%Y").date()
                    usar_data_det = True
        with det_f2:
            st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
            if st.button("Atualizar dados", use_container_width=True, type="primary", key="btn_det"):
                st.cache_data.clear()
                st.rerun()
        with det_f3:
            st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
            if st.button("Limpar", use_container_width=True, key="btn_clear_det"):
                for k in ("det_dtsel", "det_cli", "det_nf", "det_ped", "det_placa"):
                    st.session_state.pop(k, None)
                st.rerun()

        ds1, ds2, ds3, ds4 = st.columns(4, gap="medium")
        with ds1:
            s_cli_r = st.text_input("Cliente", placeholder="Nome", key="det_cli")
        with ds2:
            s_nf_r = st.text_input("Nota (NUMNOTA)", placeholder="Número", key="det_nf")
        with ds3:
            s_ped_r = st.text_input("Pedido (NUMPED)", placeholder="Número", key="det_ped")
        with ds4:
            s_placa_r = st.text_input("Placa", placeholder="PLACAANT ou PLACAATUAL", key="det_placa")
        st.markdown('</div>', unsafe_allow_html=True)

        df_det_base = df_reent.copy()
        if usar_data_det and dt_det_sel:
            df_det_base = df_det_base[df_det_base["_DATATRANSF_DT"].dt.date == dt_det_sel]
            st.info(f"Data {dt_det_sel.strftime('%d/%m/%Y')} — {len(df_det_base)} registros nos gráficos e na tabela")
        else:
            st.info(f"Todos os períodos — {len(df_det_base)} registros. Use o filtro de data para detalhar.")

        REENT_DISPLAY = [
            ("DATATRANSF", "DTRANSF"), ("NUMPED", "NUMPED"), ("NUMNOTA", "NUMNOTA"),
            ("DTFAT", "DTFAT"), ("DTSAIDA", "DTSAIDA"), ("CLIENTE", "CLIENTE"), ("CODCLI", "CODCLI"),
            ("BAIRROENT", "BAIRROENT"), ("CODPRACA", "CODPRACA"), ("PRACA", "PRACA"), ("ROTA", "ROTA"),
            ("NUMCARANTERIOR", "CAR.ANT"), ("PLACAANT", "PLACAANT"),
            ("NOME_MOT_ANTERIOR", "MOT.ANT"), ("NOME_AJU_ANTERIOR", "AJU.ANT"),
            ("NUMCARATUAL", "CAR.ATUAL"), ("PLACAATUAL", "PLACAATUAL"),
            ("NOME_MOT_ATUAL", "MOT.ATUAL"), ("NOME_AJU_ATUAL", "AJU.ATUAL"),
            ("CODMOTIVO", "COD.MOTIVO"), ("MOTIVOTRANSF", "MOTIVO"),
            ("VLTOTGER", "VLTOTGER"), ("TOTPESO", "PESO"), ("NOME", "VENDEDOR"), ("CODUSU", "CODUSU"),
        ]
        cols_det_ok = [(reent_cols.get(k), label) for k, label in REENT_DISPLAY if reent_cols.get(k) is not None]
        df_det = df_det_base[[o for o, _ in cols_det_ok]].copy()
        df_det.columns = [label for _, label in cols_det_ok]

        if s_cli_r.strip() and "CLIENTE" in df_det.columns:
            df_det = df_det[df_det["CLIENTE"].str.contains(s_cli_r.strip(), case=False, na=False)]
        if s_nf_r.strip() and "NUMNOTA" in df_det.columns:
            df_det = df_det[df_det["NUMNOTA"].str.contains(s_nf_r.strip(), case=False, na=False)]
        if s_ped_r.strip() and "NUMPED" in df_det.columns:
            df_det = df_det[df_det["NUMPED"].str.contains(s_ped_r.strip(), case=False, na=False)]
        if s_placa_r.strip():
            mask_p = pd.Series([False] * len(df_det), index=df_det.index)
            for cp in ["PLACAANT", "PLACAATUAL"]:
                if cp in df_det.columns:
                    mask_p = mask_p | df_det[cp].str.contains(s_placa_r.strip(), case=False, na=False)
            df_det = df_det[mask_p]

        _det_placa_col = reent_cols.get("PLACAATUAL")
        _det_motivo_col = reent_cols.get("MOTIVOTRANSF")
        if not _det_placa_col:
            for _c in ["PLACA_ATUAL", "PLACAATUAL", "PLACA_ATU"]:
                if _c in df_det_base.columns:
                    _det_placa_col = _c
                    break
        if not _det_motivo_col:
            for _c in ["MOTIVOTRANSF", "MOTIVO_TRANSF"]:
                if _c in df_det_base.columns:
                    _det_motivo_col = _c
                    break

        gcol1, gcol2 = st.columns(2, gap="medium")
        with gcol1:
            panel_open("Reentregas por placa atual", tag="PLACAATUAL", icon="🚚")
            if _det_placa_col and _det_placa_col in df_det_base.columns:
                df_gplaca = (df_det_base[df_det_base[_det_placa_col].str.strip() != ""]
                             .groupby(_det_placa_col).agg(Qtd=(_det_placa_col, "count"))
                             .reset_index().sort_values("Qtd", ascending=False))
                if not df_gplaca.empty:
                    st.plotly_chart(make_bar_simple(df_gplaca, _det_placa_col, "Qtd", ramp(len(df_gplaca), 3, 6)),
                                    use_container_width=True)
                else:
                    st.info("Sem placas para o filtro selecionado.")
            else:
                st.warning("Coluna PLACAATUAL não encontrada.")
            panel_close()
        with gcol2:
            panel_open("Reentregas por motivo", tag="MOTIVOTRANSF", icon="❗")
            if _det_motivo_col and _det_motivo_col in df_det_base.columns:
                df_gmot = (df_det_base[df_det_base[_det_motivo_col].str.strip() != ""]
                           .groupby(_det_motivo_col).agg(Qtd=(_det_motivo_col, "count"))
                           .reset_index().sort_values("Qtd", ascending=False))
                if not df_gmot.empty:
                    st.plotly_chart(make_bar_simple(df_gmot, _det_motivo_col, "Qtd", ramp(len(df_gmot), 3, 6, C_OK)),
                                    use_container_width=True)
                else:
                    st.info("Sem motivos para o filtro selecionado.")
            else:
                st.warning("Coluna MOTIVOTRANSF não encontrada.")
            panel_close()

        panel_open("Registros de reentrega", tag=f"{len(df_det)} linhas", icon="🔍")
        if len(df_det) == 0:
            st.warning("Nenhum registro encontrado. Ajuste a busca ou limpe os filtros.")
        else:
            html_table(df_det, min_width=1200)
            if len(df_det) > 500:
                st.caption(f"Exibindo as primeiras 500 de {len(df_det)} linhas.")
            csv_det = df_det.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            st.download_button("Exportar CSV", data=csv_det,
                               file_name=f"reentregas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                               mime="text/csv")
        panel_close()

        with st.expander("Diagnóstico — colunas da planilha de reentregas"):
            cols_real = list(df_reent_raw.columns)
            st.write(f"**URL usada:** `{reent_url_usada}`")
            st.write(f"**Linhas:** {len(df_reent_raw)} · **Colunas:** {len(cols_real)}")
            st.write(f"**Colunas encontradas:** `{cols_real}`")
            st.write(f"PLACA_ATUAL → `{reent_cols.get('PLACAATUAL')}`")
            st.write(f"MOTIVOTRANSF → `{reent_cols.get('MOTIVOTRANSF')}`")
            st.write(f"DTRANSF → `{reent_cols.get('DATATRANSF')}`")
            st.write(f"PLACAANT → `{reent_cols.get('PLACAANT')}`")


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: CAMPOS
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Campos":
    st.markdown('<div class="filters"><div class="filters-h"><span class="pip"></span>'
                'Pesquisa — devoluções</div>', unsafe_allow_html=True)
    sr1, sr2, sr3, sr4 = st.columns(4, gap="medium")
    with sr1:
        s_cli = st.text_input("Cliente", placeholder="Nome", key="sc_cli")
    with sr2:
        s_nf = st.text_input("Nota de venda", placeholder="Número", key="sc_nf")
    with sr3:
        s_ped = st.text_input("Código do cliente", placeholder="CODCLI", key="sc_ped")
    with sr4:
        s_placa2 = st.text_input("Placa", placeholder="Ex.: NPB1J08", key="sc_placa")
    st.markdown('</div>', unsafe_allow_html=True)

    CAMPOS = [
        (COL_DTENTREGA, "DTENT"), (COL_DTSAIDA, "DTSAIDA"), (COL_NF_VENDA, "NOTA_VENDA"),
        (COL_NOTA_DEV, "NOTA_DEVOLUCAO"), (COL_NUMCAR, "NUMCAR"), (COL_PLACA, "PLACA"),
        (COL_DESTINO, "DESTINO"), (COL_MOTIVO, "MOTIVO"), (COL_CODCLI, "CODCLI"),
        (COL_CLIENTE, "CLIENTE"), (COL_MOTORISTA, "MOTORISTA"), (COL_VENDEDOR, "NOMERCA"),
        (COL_DEVOLUCION, "NOMEFUNC"), (COL_SUPERVISOR, "SUPERVISOR"), (COL_TIPO_MERC, "TIPO_MERCADO"),
    ]
    cols_ok = [(o, a) for o, a in CAMPOS if o is not None]
    df_campos = df[[o for o, _ in cols_ok]].copy()
    df_campos.columns = [a for _, a in cols_ok]

    if s_cli.strip() and "CLIENTE" in df_campos.columns:
        df_campos = df_campos[df_campos["CLIENTE"].str.contains(s_cli.strip(), case=False, na=False)]
    if s_nf.strip() and "NOTA_VENDA" in df_campos.columns:
        df_campos = df_campos[df_campos["NOTA_VENDA"].str.contains(s_nf.strip(), case=False, na=False)]
    if s_ped.strip() and "CODCLI" in df_campos.columns:
        df_campos = df_campos[df_campos["CODCLI"].str.contains(s_ped.strip(), case=False, na=False)]
    if s_placa2.strip() and "PLACA" in df_campos.columns:
        df_campos = df_campos[df_campos["PLACA"].str.contains(s_placa2.strip(), case=False, na=False)]

    panel_open("Campos das devoluções", tag=f"{len(df_campos)} registros", icon="🗂️")
    if len(df_campos) == 0:
        st.warning("Nenhum registro encontrado. Ajuste a busca ou limpe os filtros.")
    else:
        html_table(df_campos, min_width=1000)
        if len(df_campos) > 500:
            st.caption(f"Exibindo as primeiras 500 de {len(df_campos)} linhas.")
        csv_c = df_campos.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        st.download_button("Exportar CSV", data=csv_c,
                           file_name=f"campos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
    panel_close()


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: DADOS COMPLETOS
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Dados Completos":
    display_cols = [c for c in actual_cols if not c.startswith("_")]

    st.markdown('<div class="filters"><div class="filters-h"><span class="pip"></span>'
                'Exibição da tabela</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3, gap="medium")
    sort_opts = [VALOR_COL] + [c for c in [COL_DTSAIDA, COL_DTENTREGA, COL_CLIENTE, COL_MOTIVO, COL_PLACA] if c]
    with d1:
        sort_col = st.selectbox("Ordenar por", sort_opts)
    with d2:
        sort_asc = st.radio("Direção", ["Crescente", "Decrescente"], horizontal=True) == "Crescente"
    with d3:
        n_rows = st.selectbox("Máximo de linhas", [50, 100, 250, 500, 1000, "Todos"])
    st.markdown('</div>', unsafe_allow_html=True)

    df_sorted = df.sort_values(sort_col, ascending=sort_asc)
    if n_rows != "Todos":
        df_sorted = df_sorted.head(int(n_rows))
    disp = df_sorted[display_cols]

    panel_open("Base completa de devoluções", tag=f"{len(df)} registros no filtro", icon="📑")
    html_table(disp, min_width=1000)
    st.caption(f"Exibindo {min(len(disp), 500)} de {len(df)} registros.")
    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    with e1:
        csv_all = df[display_cols].to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("Exportar filtrados (CSV)", data=csv_all,
                           file_name=f"devolucoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                           mime="text/csv", use_container_width=True)
    with e2:
        if st.button("Atualizar dados", use_container_width=True, type="primary", key="btn_upd_dados"):
            st.cache_data.clear()
            st.rerun()
    panel_close()


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: CLIENTES
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Clientes":
    if not COL_CLIENTE:
        st.warning("Coluna CLIENTE não encontrada na planilha.")
    else:
        df_cli_all = (df[df[COL_CLIENTE].str.strip() != ""]
                      .groupby(COL_CLIENTE).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                      .reset_index().sort_values("Valor", ascending=False))
        st.markdown(
            '<div class="kpi-grid">'
            + kpi("👥", "Clientes únicos", f"{total_clientes}", "Com devolução no filtro", "#34d399")
            + kpi("💰", "Valor total", fmt_brl(total_val), "Soma de VLTOTAL", "#22d3ee")
            + kpi("📄", "Devoluções", f"{total_notas}", "Notas no filtro", "#a78bfa")
            + kpi("📈", "Ticket médio", fmt_brl(ticket_medio), "Valor por devolução", "#fbbf24")
            + kpi("🏆", "Maior cliente",
                  fmt_brl0(df_cli_all["Valor"].iloc[0]) if not df_cli_all.empty else "R$ 0",
                  str(df_cli_all[COL_CLIENTE].iloc[0])[:26] if not df_cli_all.empty else "—", "#fb923c")
            + '</div>', unsafe_allow_html=True)

        cA, cB = st.columns([1.4, 1], gap="medium")
        with cA:
            panel_open("Clientes com maior valor devolvido", tag="Top 15", icon="👥")
            df_top15 = df_cli_all.sort_values("Valor", ascending=True).tail(15)
            if not df_top15.empty:
                st.plotly_chart(make_hbar(df_top15, "Valor", COL_CLIENTE, MIXED, 560), use_container_width=True)
            else:
                st.info("Sem clientes no filtro atual.")
            panel_close()
        with cB:
            panel_open("Clientes por quantidade de notas", tag="Top 15", icon="📄")
            df_topq = df_cli_all.sort_values("Qtd", ascending=True).tail(15)
            if not df_topq.empty:
                st.plotly_chart(make_hbar(df_topq, "Qtd", COL_CLIENTE, BLUE, 560, money=False),
                                use_container_width=True)
            panel_close()

        panel_open("Detalhamento por cliente", tag=f"{len(df_cli_all)} clientes", icon="📋")
        tb = df_cli_all.copy()
        tb["Valor total"] = tb["Valor"].apply(fmt_brl)
        tb["% do total"] = (tb["Valor"] / total_val * 100).round(1).astype(str) + "%" if total_val > 0 else "0%"
        tb["Ticket médio"] = (tb["Valor"] / tb["Qtd"]).apply(fmt_brl)
        tb = tb.rename(columns={COL_CLIENTE: "Cliente", "Qtd": "Notas"})
        html_table(tb[["Cliente", "Notas", "Valor total", "Ticket médio", "% do total"]], min_width=760)
        panel_close()


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: MOTIVOS
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Motivos":
    if not COL_MOTIVO:
        st.warning("Coluna MOTIVO não encontrada na planilha.")
    else:
        df_mot_all = (df[df[COL_MOTIVO].str.strip() != ""]
                      .groupby(COL_MOTIVO).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                      .reset_index().sort_values("Valor", ascending=False))
        st.markdown(
            '<div class="kpi-grid">'
            + kpi("❗", "Motivos distintos", f"{len(df_mot_all)}", "No filtro atual", "#f87171")
            + kpi("💰", "Valor total", fmt_brl(total_val), "Soma de VLTOTAL", "#22d3ee")
            + kpi("📄", "Devoluções", f"{total_notas}", "Notas no filtro", "#a78bfa")
            + kpi("🥇", "Motivo líder",
                  fmt_brl0(df_mot_all["Valor"].iloc[0]) if not df_mot_all.empty else "R$ 0",
                  str(df_mot_all[COL_MOTIVO].iloc[0])[:26] if not df_mot_all.empty else "—", "#fbbf24")
            + kpi("📈", "Ticket médio", fmt_brl(ticket_medio), "Valor por devolução", "#34d399")
            + '</div>', unsafe_allow_html=True)

        panel_open("Motivos — valor e quantidade", tag="Consolidado", icon="❗")
        if not df_mot_all.empty:
            fig_m = make_combo_chart(df_mot_all, COL_MOTIVO, "Valor", "Qtd", "", "", ramp(len(df_mot_all), 3, 6))
            fig_m.update_layout(height=max(440, min(len(df_mot_all) * 58, 680)),
                                margin=dict(t=54, b=120, l=10, r=30))
            fig_m.update_xaxes(tickangle=-35, automargin=True)
            st.plotly_chart(fig_m, use_container_width=True)
        else:
            st.info("Sem motivos no filtro atual.")
        panel_close()

        m1, m2 = st.columns([1, 1.4], gap="medium")
        with m1:
            panel_open("Participação por motivo", tag="Top 10", icon="🥧")
            df_pie = df_mot_all.head(10)
            if not df_pie.empty:
                fig_pm = px.pie(df_pie, names=COL_MOTIVO, values="Valor",
                                color_discrete_sequence=MIXED, hole=0.62)
                fig_pm.update_traces(textfont=dict(size=12, color="#e8f1fb"),
                                     marker=dict(line=dict(color="rgba(4,7,15,0.9)", width=2)))
                st.plotly_chart(plotly_dark(fig_pm, height=420), use_container_width=True)
            panel_close()
        with m2:
            panel_open("Ranking completo", tag=f"{len(df_mot_all)} motivos", icon="📊")
            tbm = df_mot_all.copy()
            tbm["Valor total"] = tbm["Valor"].apply(fmt_brl)
            tbm["% do total"] = (tbm["Valor"] / total_val * 100).round(1).astype(str) + "%" if total_val > 0 else "0%"
            tbm = tbm.rename(columns={COL_MOTIVO: "Motivo", "Qtd": "Ocorrências"})
            html_table(tbm[["Motivo", "Ocorrências", "Valor total", "% do total"]], min_width=620)
            panel_close()


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: VEÍCULOS
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Veículos":
    if not COL_PLACA:
        st.warning("Coluna PLACA não encontrada na planilha.")
    else:
        df_pl_all = (df[df[COL_PLACA].str.strip() != ""]
                     .groupby(COL_PLACA).agg(Valor=(VALOR_COL, "sum"), Qtd=(VALOR_COL, "count"))
                     .reset_index().sort_values("Valor", ascending=False))
        st.markdown(
            '<div class="kpi-grid">'
            + kpi("🚚", "Veículos únicos", f"{total_placas}", "Placas no filtro", "#fb923c")
            + kpi("💰", "Valor total", fmt_brl(total_val), "Soma de VLTOTAL", "#22d3ee")
            + kpi("📄", "Devoluções", f"{total_notas}", "Notas no filtro", "#a78bfa")
            + kpi("📊", "Média por veículo",
                  fmt_brl(total_val / total_placas) if total_placas > 0 else "R$ 0,00",
                  "Valor médio por placa", "#34d399")
            + kpi("🥇", "Maior valor",
                  fmt_brl0(df_pl_all["Valor"].iloc[0]) if not df_pl_all.empty else "R$ 0",
                  str(df_pl_all[COL_PLACA].iloc[0]) if not df_pl_all.empty else "—", "#f87171")
            + '</div>', unsafe_allow_html=True)

        panel_open("Devoluções por veículo — valor e quantidade", tag="Consolidado", icon="🚚")
        if not df_pl_all.empty:
            st.plotly_chart(make_combo_chart(df_pl_all, COL_PLACA, "Valor", "Qtd", "", "", ramp(len(df_pl_all))),
                            use_container_width=True)
        else:
            st.info("Sem veículos no filtro atual.")
        panel_close()

        v1, v2 = st.columns([1, 1.4], gap="medium")
        with v1:
            panel_open("Veículos por quantidade de notas", tag="Top 12", icon="📄")
            df_pq = df_pl_all.sort_values("Qtd", ascending=True).tail(12)
            if not df_pq.empty:
                st.plotly_chart(make_hbar(df_pq, "Qtd", COL_PLACA, BLUE, 460, money=False),
                                use_container_width=True)
            panel_close()
        with v2:
            panel_open("Detalhamento por veículo", tag=f"{len(df_pl_all)} placas", icon="📋")
            tbv = df_pl_all.copy()
            tbv["Valor total"] = tbv["Valor"].apply(fmt_brl)
            tbv["Ticket médio"] = (tbv["Valor"] / tbv["Qtd"]).apply(fmt_brl)
            tbv["% do total"] = (tbv["Valor"] / total_val * 100).round(1).astype(str) + "%" if total_val > 0 else "0%"
            tbv = tbv.rename(columns={COL_PLACA: "Placa", "Qtd": "Notas"})
            html_table(tbv[["Placa", "Notas", "Valor total", "Ticket médio", "% do total"]], min_width=680)
            panel_close()


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: RELATÓRIOS
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Relatórios":
    st.markdown(
        '<div class="kpi-grid">'
        + kpi("📄", "Devoluções no filtro", f"{total_notas}", "Prontas para exportar", "#22d3ee")
        + kpi("💰", "Valor total", fmt_brl(total_val), "Soma de VLTOTAL", "#34d399")
        + kpi("🔄", "Reentregas", f"{len(df_reent) if df_reent is not None else 0}", "Registros carregados", "#fbbf24")
        + kpi("👥", "Clientes únicos", f"{total_clientes}", "No filtro atual", "#a78bfa")
        + kpi("🚚", "Veículos únicos", f"{total_placas}", "No filtro atual", "#fb923c")
        + '</div>', unsafe_allow_html=True)

    panel_open("Exportações", tag="CSV separado por ponto e vírgula", icon="📤")
    st.markdown('<p style="font-size:0.82rem;color:#7c8ea8;margin-bottom:14px;">'
                'Os arquivos respeitam os filtros aplicados no topo da página.</p>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3, gap="medium")
    display_cols_rel = [c for c in actual_cols if not c.startswith("_")]
    with r1:
        st.download_button("Devoluções filtradas",
                           data=df[display_cols_rel].to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                           file_name=f"devolucoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                           mime="text/csv", use_container_width=True)
    with r2:
        if COL_MOTIVO:
            _rm = (df.groupby(COL_MOTIVO).agg(Qtd=(VALOR_COL, "count"), Valor=(VALOR_COL, "sum"))
                   .reset_index().sort_values("Valor", ascending=False))
            st.download_button("Resumo por motivo",
                               data=_rm.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                               file_name=f"resumo_motivos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                               mime="text/csv", use_container_width=True)
    with r3:
        if df_reent is not None and len(df_reent) > 0:
            _cols_r = [c for c in df_reent.columns if not c.startswith("_")]
            st.download_button("Reentregas completas",
                               data=df_reent[_cols_r].to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                               file_name=f"reentregas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                               mime="text/csv", use_container_width=True)
        else:
            st.caption("Reentregas indisponíveis no momento.")
    panel_close()

    panel_open("Resumo consolidado", tag="Visão do filtro atual", icon="📋")
    linhas = []
    if COL_MOTIVO:
        _t = (df.groupby(COL_MOTIVO).agg(Qtd=(VALOR_COL, "count"), Valor=(VALOR_COL, "sum"))
              .reset_index().sort_values("Valor", ascending=False).head(10))
        for _, r in _t.iterrows():
            linhas.append({"Dimensão": "Motivo", "Item": r[COL_MOTIVO], "Qtd": r["Qtd"],
                           "Valor": fmt_brl(r["Valor"])})
    if COL_PLACA:
        _t = (df[df[COL_PLACA].str.strip() != ""].groupby(COL_PLACA)
              .agg(Qtd=(VALOR_COL, "count"), Valor=(VALOR_COL, "sum"))
              .reset_index().sort_values("Valor", ascending=False).head(10))
        for _, r in _t.iterrows():
            linhas.append({"Dimensão": "Veículo", "Item": r[COL_PLACA], "Qtd": r["Qtd"],
                           "Valor": fmt_brl(r["Valor"])})
    if linhas:
        html_table(pd.DataFrame(linhas), min_width=560)
    else:
        st.info("Nada a resumir com os filtros atuais.")
    panel_close()


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA: CONFIGURAÇÕES
# ═════════════════════════════════════════════════════════════════════════════
elif pagina == "Configurações":
    panel_open("Fonte de dados", tag="Google Sheets", icon="🔌")
    st.markdown(f'<p style="font-size:0.82rem;color:#b9c8dc;">Planilha: <code>{SHEET_ID}</code><br>'
                f'Cache: 60 segundos · Última sincronização: {_sync}</p>', unsafe_allow_html=True)
    cfg1, cfg2 = st.columns([1, 3])
    with cfg1:
        if st.button("Atualizar dados", use_container_width=True, type="primary", key="btn_cfg"):
            st.cache_data.clear()
            st.rerun()
    panel_close()

    panel_open("Colunas detectadas — devoluções", tag=f"{len(actual_cols)} colunas", icon="🧩")
    st.write(f"**Colunas:** `{actual_cols}`")
    st.write(f"Valor = `{VALOR_COL}` · Placa = `{COL_PLACA}` · Motivo = `{COL_MOTIVO}`")
    st.write(f"Cliente = `{COL_CLIENTE}` · Devolucionista = `{COL_DEVOLUCION}`")
    st.write(f"Data de entrada (DTENT) = `{COL_DTENTREGA}` · Data de saída = `{COL_DTSAIDA}`")
    st.write(f"Supervisor = `{COL_SUPERVISOR}` · Destino = `{COL_DESTINO}` · Nota de devolução = `{COL_NOTA_DEV}`")
    st.write(f"Registros com valor maior que zero: {(df_raw[VALOR_COL] > 0).sum()}")
    panel_close()

    panel_open("Colunas detectadas — reentregas", tag="Diagnóstico", icon="🧩")
    if df_reent is not None:
        st.write(f"**URL usada:** `{reent_url_usada}`")
        st.write(f"**Colunas:** `{list(df_reent_raw.columns)}`")
        st.write(f"Valor = `{REENT_VALOR_COL}` · PLACAANT = `{reent_cols.get('PLACAANT')}` · "
                 f"PLACAATUAL = `{reent_cols.get('PLACAATUAL')}` · MOTIVOTRANSF = `{reent_cols.get('MOTIVOTRANSF')}`")
    else:
        st.warning("Reentregas não carregadas nesta sessão.")
        if reent_load_error:
            st.caption(reent_load_error)
    panel_close()

    panel_open("Sobre esta versão", tag="Interface v2", icon="ℹ️")
    st.markdown(
        '<p style="font-size:0.82rem;color:#7c8ea8;line-height:1.8;">'
        'Redesign visual: menu lateral fixo, cabeçalho com status de sincronização, painel de filtros compacto, '
        'cards de indicadores redesenhados e gráficos com eixos discretos.<br>'
        'Nenhuma regra de cálculo, consulta, filtro ou fonte de dados foi alterada em relação à versão anterior.</p>',
        unsafe_allow_html=True)
    panel_close()
