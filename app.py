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
.kpi-
