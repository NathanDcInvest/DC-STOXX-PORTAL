import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import base64

# --- 1. CONFIG & SESSION STATE (Navigatie Fix) ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"

st.set_page_config(page_title="DC STOXX Portal", layout="wide", initial_sidebar_state="expanded")

if 'page' not in st.session_state:
    st.session_state.page = "📈 Equities"

# --- 2. CSS VOOR DE "ZERO MESS" LOOK ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BRAND_NAVY}; color: white; }}
    [data-testid="stSidebar"] {{ background-color: {BRAND_NAVY}; border-right: 2px solid {BRAND_GOLD}; }}
    
    /* Witte Header Balk */
    .logo-bar {{
        background-color: white;
        width: 100%;
        padding: 10px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 4px solid {BRAND_GOLD};
    }}
    
    /* Sidebar Knoppen Styling */
    .stButton>button {{
        width: 100%;
        background-color: transparent;
        color: {BRAND_GOLD} !important;
        border: 1px solid {BRAND_GOLD} !important;
        text-align: left;
        padding: 10px 15px;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: {BRAND_GOLD};
        color: {BRAND_NAVY} !important;
    }}
    
    /* Verwijder Streamlit Padding */
    .main .block-container {{ padding-top: 0rem !important; max-width: 95%; }}
    [data-testid="stHeader"] {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Navigatie & Lange Newsfeed) ---
with st.sidebar:
    st.markdown(f"<h3 style='text-align:center; color:{BRAND_GOLD};'>NAVIGATION</h3>", unsafe_allow_html=True)
    
    if st.button("📊 Market Overview"): st.session_state.page = "📊 Market Overview"
    if st.button("📈 Equities"): st.session_state.page = "📈 Equities"
    if st.button("₿ Crypto"): st.session_state.page = "₿ Crypto"
    if st.button("🛢️ Oil & Commodities"): st.session_state.page = "🛢️ Oil & Commodities"
    
    st.markdown("---")
    st.markdown(f"<p style='color:{BRAND_GOLD}; text-align:center;'>WORLD NEWS</p>", unsafe_allow_html=True)
    
    # Newsfeed langer gemaakt (1200px) om dead space te voorkomen
    components.html("""
        <iframe src="https://www.tradingview.com/embed-widget/timeline/?colorTheme=dark&isTransparent=true&displayMode=adaptive" 
        width="100%" height="1100" frameborder="0"></iframe>
    """, height=1100)

# --- 4. HEADER SECTIE (Ticker + Centered Logo) ---

# Ticker Tape helemaal bovenaan
components.html("""
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?colorTheme=dark&isTransparent=true" 
    width="100%" height="50" frameborder="0"></iframe>
""", height=50)

# Witte Balk met Logo (Centered)
# Tip: Zorg dat Logo.png in de map staat
col_l, col_logo, col_r = st.columns([1, 0.6, 1])
with col_logo:
    try:
        st.image("Logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='color:black; text-align:center;'>DC STOXX</h1>", unsafe_allow_html=True)

st.markdown(f"<div style='border-bottom: 4px solid {BRAND_GOLD}; width:100%; margin-top:-15px; margin-bottom:20px;'></div>", unsafe_allow_html=True)

# --- 5. DATASET & FUNCTIES ---
def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        unique_id = f"{prefix}_{i}"
        with cols[i % 3]:
            card_html = f"""
            <div style="background:#131722; border:1px solid {BRAND_GOLD}33; border-radius:12px; height:550px; overflow:hidden; margin-bottom:20px;">
                <iframe src="https://www.tradingview.com/embed-widget/symbol-info/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="180" frameborder="0"></iframe>
                <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol={asset['s']}&colorTheme=dark&isTransparent=true&interval=1D" width="100%" height="360" frameborder="0"></iframe>
            </div>
            """
            components.html(card_html, height=560)

# --- 6. PAGINA CONTENT LOGICA ---

if st.session_state.page == "📊 Market Overview":
    st.title("Market Intelligence Overview")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Global S&P 500 Heatmap")
        components.html('<iframe src="https://www.tradingview.com/embed-widget/stock-heatmap/?colorTheme=dark&isTransparent=true&index=SPX500" width="100%" height="600" frameborder="0"></iframe>', height=620)
    with col2:
        st.subheader("Indices")
        components.html('<iframe src="https://www.tradingview.com/embed-widget/markets/?colorTheme=dark&isTransparent=true" width="100%" height="600" frameborder="0"></iframe>', height=620)

elif st.session_state.page == "📈 Equities":
    st.title("Institutional Equities")
    equities = [
        {"n": "Apple", "s": "NASDAQ:AAPL"}, {"n": "Microsoft", "s": "NASDAQ:MSFT"},
        {"n": "Nvidia", "s": "NASDAQ:NVDA"}, {"n": "Alphabet", "s": "NASDAQ:GOOGL"},
        {"n": "Amazon", "s": "NASDAQ:AMZN"}, {"n": "Meta", "s": "NASDAQ:META"},
        {"n": "Tesla", "s": "NASDAQ:TSLA"}, {"n": "Berkshire", "s": "NYSE:BRK.B"},
        {"n": "Eli Lilly", "s": "NYSE:LLY"}, {"n": "Visa", "s": "NYSE:V"},
        {"n": "JPMorgan", "s": "NYSE:JPM"}, {"n": "TSMC", "s": "NYSE:TSM"},
        {"n": "UnitedHealth", "s": "NYSE:UNH"}, {"n": "Mastercard", "s": "NYSE:MA"},
        {"n": "Broadcom", "s": "NASDAQ:AVGO"}, {"n": "Home Depot", "s": "NYSE:HD"},
        {"n": "P&G", "s": "NYSE:PG"}, {"n": "Costco", "s": "NASDAQ:COST"},
        {"n": "J&J", "s": "NYSE:JNJ"}, {"n": "Salesforce", "s": "NYSE:CRM"},
        {"n": "AMD", "s": "NASDAQ:AMD"}, {"n": "Netflix", "s": "NASDAQ:NFLX"}
    ]
    render_portal_grid(equities, "eq")

elif st.session_state.page == "₿ Crypto":
    st.title("Digital Assets")
    crypto = [
        {"n": "Bitcoin", "s": "BINANCE:BTCUSDT"}, {"n": "Ethereum", "s": "BINANCE:ETHUSDT"},
        {"n": "Solana", "s": "BINANCE:SOLUSDT"}, {"n": "Cardano", "s": "BINANCE:ADAUSDT"}
    ]
    render_portal_grid(crypto, "cry")

elif st.session_state.page == "🛢️ Oil & Commodities":
    st.title("Hard Commodities")
    commodities = [
        {"n": "Gold", "s": "TVC:GOLD"}, {"n": "Crude Oil", "s": "TVC:USOIL"},
        {"n": "Silver", "s": "TVC:SILVER"}, {"n": "Natural Gas", "s": "TVC:NATGAS"}
    ]
    render_portal_grid(commodities, "com")
    
