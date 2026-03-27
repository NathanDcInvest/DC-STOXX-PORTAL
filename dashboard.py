import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. CONFIG & SESSION STATE ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"

st.set_page_config(page_title="DC STOXX Portal", layout="wide", initial_sidebar_state="expanded")

if 'page' not in st.session_state:
    st.session_state.page = "📈 Equities"

# --- 2. HET VISUELE STYLING BLOK (Agressieve Schoonmaak) ---
st.markdown(f"""
    <style>
    /* 2A. Verwijder ELKE vorm van witte balk boven het logo */
    [data-testid="stHeader"], .st-emotion-cache-18ni73i, .st-emotion-cache-v698uo {{
        display: none !important;
        height: 0px !important;
    }}
    
    .stApp {{
        background-color: {BRAND_NAVY};
        color: white;
    }}
    
    /* 2B. Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 2px solid {BRAND_GOLD};
        min-width: 320px !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {{
        color: {BRAND_NAVY} !important;
    }}

    /* 2C. Sidebar Knoppen: GEEN KLEURVERANDERING, ALLEEN ENLARGE */
    div.stButton > button {{
        width: 100% !important;
        background-color: white !important;
        color: {BRAND_NAVY} !important;
        border: 2px solid {BRAND_NAVY} !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 12px 15px !important;
        transition: transform 0.2s ease-in-out !important;
        display: block !important;
    }}

    div.stButton > button:hover, div.stButton > button:focus, div.stButton > button:active {{
        transform: scale(1.05) !important; /* Vergroot de box */
        background-color: white !important; /* Blijft wit */
        color: {BRAND_NAVY} !important;    /* Blijft navy */
        border-color: {BRAND_GOLD} !important;
        box-shadow: none !important;
    }}

    /* 2D. De Witte Top Header (Echt tegen de bovenkant) */
    .white-top-header {{
        background-color: #FFFFFF;
        width: 100%;
        padding: 15px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 3px solid {BRAND_GOLD};
        margin-top: -100px; /* Forceert de balk over de lege ruimte */
    }}

    .main .block-container {{
        padding-top: 0rem !important;
        max-width: 95%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (WIT MENU) ---
with st.sidebar:
    st.markdown(f"<h1 style='text-align:center; color:{BRAND_NAVY}; margin-bottom: 0;'>DC STOXX</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{BRAND_GOLD}; font-weight:bold; letter-spacing: 2px;'>MASTER TERMINAL</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("📈 Equities"): st.session_state.page = "📈 Equities"
    if st.button("₿ Crypto"): st.session_state.page = "₿ Crypto"
    if st.button("🛢️ Commodities"): st.session_state.page = "🛢️ Commodities & Oil"
    if st.button("📊 Heat Map"): st.session_state.page = "📊 Heat Map"
    
    st.markdown("---")
    components.html("""
        <iframe src="https://www.tradingview.com/embed-widget/timeline/?colorTheme=light&isTransparent=true&displayMode=adaptive" 
        width="100%" height="800" frameborder="0"></iframe>
    """, height=800)

# --- 4. TOP HEADER & TICKER ---
st.markdown('<div class="white-top-header">', unsafe_allow_html=True)
c1, c_logo, c2 = st.columns([1, 0.7, 1])
with c_logo:
    try:
        st.image("Logo.png", use_container_width=True)
    except:
        st.markdown(f"<h2 style='color:{BRAND_NAVY}; text-align:center;'>STOXX</h2>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Ticker Tape (Hoogte op 60px: de perfecte balans voor leesbaarheid)
components.html("""
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?locale=en&colorTheme=dark&isTransparent=true&displayMode=adaptive" 
    width="100%" height="60" frameborder="0" style="display:block; margin:0;"></iframe>
""", height=60)

# --- 5. MAIN CONTENT AREA ---
st.title(f"{st.session_state.page}")
st.markdown(f"*{datetime.now().strftime('%d %B %Y')} - Institutional Intelligence*")

def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        unique_id = f"{prefix}_{i}"
        with cols[i % 3]:
            # DE "PRE-LOAD & SAFE-ZONE" HOVER LOGICA
            card_html = f"""
            <style>
                .asset-box {{
                    background:#131722; border:1px solid {BRAND_GOLD}44; border-radius:12px; 
                    height:520px; overflow:hidden; margin-bottom:25px; position:relative;
                }}
                .layer {{
                    position: absolute; width: 100%; height: 100%; top: 0; left: 0;
                    transition: opacity 0.3s ease;
                }}
                /* Chart laadt altijd op de achtergrond (Pre-load) */
                .chart-layer {{ z-index: 1; opacity: 1; }} 
                .gauge-layer {{ z-index: 2; opacity: 1; pointer-events: auto; }}
                
                /* Trigger zone: Alleen de bovenste 170px (Price info) wisselt naar de chart */
                .trigger-zone {{
                    position: absolute; top: 0; left: 0; width: 100%; height: 170px;
                    z-index: 10; cursor: pointer;
                }}
                
                .trigger-zone:hover ~ .gauge-layer {{
                    opacity: 0; pointer-events: none;
                }}
            </style>
            
            <div class="asset-box">
                <div class="trigger-zone"></div>
                
                <div class="chart-layer">
                    <iframe src="https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol={asset['s']}&colorTheme=dark&width=100%&height=100%&dateRange=12M" width="100%" height="100%" frameborder="0"></iframe>
                </div>
                
                <div class="gauge-layer">
                    <iframe src="https://www.tradingview.com/embed-widget/symbol-info/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="160" frameborder="0"></iframe>
                    <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol={asset['s']}&colorTheme=dark&isTransparent=true&interval=1D" width="100%" height="360" frameborder="0"></iframe>
                </div>
            </div>
            """
            components.html(card_html, height=530)

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
    components.html('<iframe src="https://www.tradingview.com/embed-widget/stock-heatmap/?colorTheme=dark&isTransparent=true&index=SPX500" width="100%" height="650" frameborder="0"></iframe>', height=670)
