import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- CONFIG & STYLING ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"

st.set_page_config(page_title="DC STOXX Elite", layout="wide", initial_sidebar_state="expanded")

# Eén centraal blok voor alle visuele aanpassingen
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BRAND_NAVY}; color: white; }}
    [data-testid="stSidebar"] {{ background-color: {BRAND_NAVY}; border-right: 2px solid {BRAND_GOLD}; }}
    
    /* Maak de sidebar knoppen "Premium" */
    .stButton>button {{
        width: 100%;
        background-color: transparent;
        color: {BRAND_GOLD};
        border: 1px solid {BRAND_GOLD};
        border-radius: 5px;
        transition: 0.3s;
        text-align: left;
    }}
    .stButton>button:hover {{
        background-color: {BRAND_GOLD};
        color: {BRAND_NAVY};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIES VOOR WIDGETS ---
def tradingview_ticker():
    components.html('<iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?colorTheme=dark&isTransparent=true" width="100%" height="50" frameborder="0"></iframe>', height=50)

def render_asset_card(symbol):
    # De "Hover" logica blijft in HTML, maar de data komt uit Python
    card_html = f"""
    <div style="background:#131722; border:1px solid {BRAND_GOLD}33; border-radius:12px; height:500px; overflow:hidden;">
        <iframe src="https://www.tradingview.com/embed-widget/symbol-info/?symbol={symbol}&colorTheme=dark&isTransparent=true" width="100%" height="150" frameborder="0"></iframe>
        <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol={symbol}&colorTheme=dark&isTransparent=true" width="100%" height="350" frameborder="0"></iframe>
    </div>
    """
    components.html(card_html, height=510)

# --- SIDEBAR NAVIGATIE ---
with st.sidebar:
    st.image("Logo.png")
    st.markdown(f"<h2 style='text-align:center; color:{BRAND_GOLD};'>NAVIGATION</h2>", unsafe_allow_html=True)
    
    # Hier maken we de snelkoppelingen
    page = "Equities" # Standaard pagina
    if st.button("📈 Equities"): page = "Equities"
    if st.button("₿ Crypto"): page = "Crypto"
    if st.button("🛢️ Commodities"): page = "Commodities"
    
    st.markdown("---")
    # Newsfeed onder de knoppen
    components.html('<iframe src="https://www.tradingview.com/embed-widget/timeline/?colorTheme=dark&isTransparent=true" width="100%" height="600" frameborder="0"></iframe>', height=600)

# --- MAIN CONTENT ---
tradingview_ticker()

# Dynamische Header op basis van selectie
st.title(f"DC STOXX | {page}")
st.markdown(f"*{datetime.now().strftime('%d %B %Y')} - Institutional Intelligence*")

# Content laden op basis van de gekozen 'page'
if page == "Equities":
    cols = st.columns(3)
    tickers = ["NASDAQ:AAPL", "NASDAQ:MSFT", "NASDAQ:NVDA", "NASDAQ:TSLA", "NASDAQ:AMZN", "NASDAQ:GOOGL"]
    for i, t in enumerate(tickers):
        with cols[i % 3]:
            render_asset_card(t)

elif page == "Crypto":
    cols = st.columns(3)
    tickers = ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT"]
    for i, t in enumerate(tickers):
        with cols[i % 3]:
            render_asset_card(t)

elif page == "Commodities":
    st.write("Commodities data coming soon...")
