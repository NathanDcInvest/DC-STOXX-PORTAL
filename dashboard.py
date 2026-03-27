import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. CONFIG & SESSION STATE ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"

# Pagina instellingen
st.set_page_config(page_title="DC STOXX Portal", layout="wide", initial_sidebar_state="expanded")

if 'page' not in st.session_state:
    st.session_state.page = "📈 Equities"

# --- 2. HET VISUELE STYLING BLOK (Gecorrigeerd) ---
st.markdown(f"""
    <style>
    /* 2A. Achtergronden */
    .stApp {{
        background-color: {BRAND_NAVY};
        color: white;
    }}
    
    /* 2B. De Grote Witte Sidebar Fix */
    [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 2px solid {BRAND_GOLD};
        min-width: 300px !important;
        max-width: 300px !important;
    }}
    
    /* Zorg dat alle tekst in de sidebar zwart/navy is */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1 {{
        color: {BRAND_NAVY} !important;
    }}

    /* 2C. Sidebar Knoppen */
    div.stButton > button {{
        width: 100%;
        background-color: transparent !important;
        color: {BRAND_NAVY} !important;
        border: 2px solid {BRAND_NAVY} !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: 0.3s !important;
        text-align: left !important;
        padding-left: 15px !important;
        margin-bottom: 5px;
    }}
    div.stButton > button:hover {{
        background-color: {BRAND_NAVY} !important;
        color: {BRAND_GOLD} !important;
        border-color: {BRAND_GOLD} !important;
    }}

    /* 2D. De Witte Top Header */
    .white-top-header {{
        background-color: #FFFFFF;
        width: 100%;
        padding: 10px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 3px solid {BRAND_GOLD};
        margin-top: -50px; /* Compenseert de ruimte van de header */
    }}

    /* 2E. HEADER FIX (Hier zat de fout) */
    /* Maak de balk transparant, maar laat de KNOPPEN staan */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0) !important;
        color: {BRAND_NAVY} !important;
    }}
    
    /* Maak de sidebar-open-dicht knop specifiek zichtbaar en donker */
    button[data-testid="stSidebarCollapseButton"] {{
        background-color: white !important;
        color: {BRAND_NAVY} !important;
        border: 1px solid {BRAND_GOLD} !important;
        border-radius: 50% !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.2) !important;
        z-index: 999999;
    }}

    .main .block-container {{
        padding-top: 0rem !important;
        max-width: 95%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (WIT MENU) ---
with st.sidebar:
    st.markdown(f"<h1 style='text-align:center; margin-top:10px;'>DC STOXX</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{BRAND_GOLD} !important; font-weight:bold; margin-top:-20px;'>MASTER TERMINAL</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigatie
    if st.button("📈 Equities"): st.session_state.page = "📈 Equities"
    if st.button("₿ Crypto"): st.session_state.page = "₿ Crypto"
    if st.button("🛢️ Commodities & Oil"): st.session_state.page = "🛢️ Commodities & Oil"
    if st.button("📊 Heat Map"): st.session_state.page = "📊 Heat Map"
    
    st.markdown("---")
    st.markdown(f"<p style='font-weight:bold; padding-left:10px;'>WORLD NEWS INTEL</p>", unsafe_allow_html=True)
    
    components.html("""
        <iframe src="https://www.tradingview.com/embed-widget/timeline/?colorTheme=light&isTransparent=true&displayMode=adaptive" 
        width="100%" height="800" frameborder="0"></iframe>
    """, height=800)

# --- 4. TOP HEADER & TICKER ---
with st.container():
    st.markdown('<div class="white-top-header">', unsafe_allow_html=True)
    col_l, col_logo, col_r = st.columns([1, 0.7, 1])
    with col_logo:
        try:
            st.image("Logo.png", use_container_width=True)
        except:
            st.markdown(f"<h1 style='color:{BRAND_NAVY}; text-align:center; margin:0;'>STOXX</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

components.html("""
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?colorTheme=dark&isTransparent=true" 
    width="100%" height="50" frameborder="0" style="display:block; margin:0;"></iframe>
""", height=50)

# --- 5. MAIN CONTENT ---
st.title(f"{st.session_state.page} Intelligence")
st.markdown(f"*{datetime.now().strftime('%d %B %Y')} - Institutional Interface*")

def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        unique_id = f"{prefix}_{i}"
        with cols[i % 3]:
            card_html = f"""
            <div style="background:#131722; border:1px solid {BRAND_GOLD}33; border-radius:12px; height:500px; overflow:hidden; margin-bottom:20px; cursor:pointer;"
                 onmouseover="this.querySelector('.static').style.opacity='0'; this.querySelector('.chart').style.opacity='1'; this.querySelector('.chart').style.visibility='visible';"
                 onmouseout="this.querySelector('.static').style.opacity='1'; this.querySelector('.chart').style.opacity='0'; this.querySelector('.chart').style.visibility='hidden';">
                
                <div class="static" style="position:absolute; width:100%; transition: opacity 0.3s ease;">
                    <iframe src="https://www.tradingview.com/embed-widget/symbol-info/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="150" frameborder="0"></iframe>
                    <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="350" frameborder="0"></iframe>
                </div>
                
                <div class="chart" style="position:absolute; width:100%; height:100%; opacity:0; visibility:hidden; transition: opacity 0.3s ease;">
                    <iframe src="https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol={asset['s']}&colorTheme=dark&width=100%&height=100%&dateRange=12M" width="100%" height="100%" frameborder="0"></iframe>
                </div>
            </div>
            """
            components.html(card_html, height=510)

# Assets
equities_list = [
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

if st.session_state.page == "📈 Equities":
    render_portal_grid(equities_list, "eq")

elif st.session_state.page == "₿ Crypto":
    crypto_list = [{"n": "Bitcoin", "s": "BINANCE:BTCUSDT"}, {"n": "Ethereum", "s": "BINANCE:ETHUSDT"}, {"n": "Solana", "s": "BINANCE:SOLUSDT"}]
    render_portal_grid(crypto_list, "cry")

elif st.session_state.page == "🛢️ Commodities & Oil":
    commodities_list = [{"n": "Gold", "s": "TVC:GOLD"}, {"n": "Crude Oil", "s": "TVC:USOIL"}]
    render_portal_grid(commodities_list, "com")

elif st.session_state.page == "📊 Heat Map":
    components.html('<iframe src="https://www.tradingview.com/embed-widget/stock-heatmap/?colorTheme=dark&isTransparent=true&index=SPX500" width="100%" height="600" frameborder="0"></iframe>', height=620)
