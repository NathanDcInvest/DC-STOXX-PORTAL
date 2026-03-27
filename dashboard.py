import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import time

# --- 1. CONFIG & BRANDING ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"

st.set_page_config(page_title="DC STOXX Portal", layout="wide", initial_sidebar_state="expanded")

# Geavanceerde CSS om alle Streamlit-marges te killen
st.markdown(f"""
    <style>
    /* Achtergrond & Sidebar */
    .stApp {{ background-color: {BRAND_NAVY}; color: white; }}
    [data-testid="stSidebar"] {{ background-color: {BRAND_NAVY}; border-right: 2px solid {BRAND_GOLD}; }}
    
    /* Verwijder de standaard Streamlit Header en witruimtes */
    [data-testid="stHeader"] {{ display: none; }}
    .main .block-container {{ 
        padding-top: 0rem !important; 
        padding-left: 0rem !important; 
        padding-right: 0rem !important; 
        max-width: 100%; 
    }}
    
    /* Zorg dat de content onder de header wel padding heeft */
    .content-wrapper {{ padding: 0 2rem; }}

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; padding: 10px 2rem; }}
    .stTabs [data-baseweb="tab"] {{ color: #8892B0; font-weight: 600; }}
    .stTabs [aria-selected="true"] {{ border-bottom: 3px solid {BRAND_GOLD} !important; color: {BRAND_GOLD} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DE MASTER HEADER (TICKER + LOGO IN ÉÉN) ---
# We gebruiken een base64 truc om het logo in de HTML te krijgen zonder externe links
import base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    logo_base64 = get_base64("Logo.png")
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height: 60px;">'
except:
    logo_html = '<h1 style="color:black; margin:0; font-family:sans-serif;">DC STOXX</h1>'

header_html = f"""
<div style="width:100%; background-color:{BRAND_NAVY}; margin:0; padding:0;">
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?locale=en&colorTheme=dark&isTransparent=false&backgroundColor=%230A1B2E&displayMode=adaptive" 
    width="100%" height="46" frameborder="0" style="display:block; margin:0;"></iframe>
    
    <div style="background-color: white; border-bottom: 4px solid {BRAND_GOLD}; padding: 10px 0; display: flex; justify-content: center; align-items: center; width: 100%;">
        {logo_html}
    </div>
</div>
"""
components.html(header_html, height=130)

# --- 3. CONTENT START ---
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Sidebar News
with st.sidebar:
    st.markdown(f"<h3 style='text-align:center; color:{BRAND_GOLD}; letter-spacing:3px; font-weight:bold;'>INTELLIGENCE</h3>", unsafe_allow_html=True)
    st.markdown("---")
    components.html('<iframe src="https://www.tradingview.com/embed-widget/timeline/?colorTheme=dark&isTransparent=true" width="100%" height="900" frameborder="0"></iframe>', height=900)

# Status Balk
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown(f"<p style='color:{BRAND_GOLD}; margin-top:10px;'>Institutional Portfolio Interface | {datetime.now().strftime('%d %M %Y')}</p>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<p style='text-align:right; color:#00ff88; margin-top:10px;'>● TERMINAL LIVE</p>", unsafe_allow_html=True)

# --- 4. TABS & GRID ---
tab_equities, tab_overview, tab_crypto = st.tabs(["📈 Equities", "📊 Market Overview", "₿ Assets"])

def render_grid(assets, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(assets):
        with cols[i % 3]:
            card = f"""
            <div style="background:#131722; border:1px solid {BRAND_GOLD}33; border-radius:12px; height:540px; margin-bottom:20px; position:relative; overflow:hidden; cursor:pointer;"
                 onmouseover="this.querySelector('.static').style.opacity='0'; this.querySelector('.chart').style.opacity='1'; this.querySelector('.chart').style.visibility='visible';"
                 onmouseout="this.querySelector('.static').style.opacity='1'; this.querySelector('.chart').style.opacity='0'; this.querySelector('.chart').style.visibility='hidden';">
                <div class="static" style="position:absolute; width:100%; transition:0.3s;">
                    <iframe src="https://www.tradingview.com/embed-widget/symbol-info/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="180" frameborder="0"></iframe>
                    <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="350" frameborder="0"></iframe>
                </div>
                <div class="chart" style="position:absolute; width:100%; height:100%; opacity:0; visibility:hidden; transition:0.3s;">
                    <iframe src="https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol={asset['s']}&colorTheme=dark&width=100%&height=100%&dateRange=12M" width="100%" height="100%" frameborder="0"></iframe>
                </div>
            </div>
            """
            st.components.v1.html(card, height=550)

# Data (Equities ingekort voor voorbeeld)
equities = [{"n": "Apple", "s": "NASDAQ:AAPL"}, {"n": "Nvidia", "s": "NASDAQ:NVDA"}, {"n": "Microsoft", "s": "NASDAQ:MSFT"}]
others = [{"n": "Bitcoin", "s": "BINANCE:BTCUSDT"}, {"n": "Gold", "s": "TVC:GOLD"}]

with tab_equities: render_grid(equities, "eq")
with tab_overview: components.html('<iframe src="https://www.tradingview.com/embed-widget/stock-heatmap/?colorTheme=dark&isTransparent=true&index=SPX500" width="100%" height="600" frameborder="0"></iframe>', height=620)
with tab_crypto: render_grid(others, "cry")

st.markdown('</div>', unsafe_allow_html=True) # Sluit content-wrapper
