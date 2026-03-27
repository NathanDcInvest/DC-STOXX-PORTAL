import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. CONFIG & SESSION STATE ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"

st.set_page_config(page_title="DC STOXX Portal", layout="wide", initial_sidebar_state="expanded")

if 'page' not in st.session_state:
    st.session_state.page = "📈 Equities"

# --- 2. HET VISUELE STYLING BLOK ---
st.markdown(f"""
    <style>
    /* 2A. Verwijder de Streamlit Header volledig */
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    
    .stApp {{
        background-color: {BRAND_NAVY};
        color: white;
    }}
    
    /* 2B. Sidebar Styling (De witte balk links) */
    [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 2px solid {BRAND_GOLD};
        min-width: 320px !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {{
        color: {BRAND_NAVY} !important;
    }}

    /* 2C. Sidebar Knoppen: ALTIJD WIT + ENLARGE EFFECT */
    div.stButton > button {{
        width: 100% !important;
        background-color: white !important;
        color: {BRAND_NAVY} !important;
        border: 2px solid {BRAND_NAVY} !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 12px 15px !important;
        transition: transform 0.2s ease-in-out, border-color 0.2s !important;
        display: block !important;
    }}

    /* Hover effect: Subtiel enlargen (1.03), kleur blijft wit */
    div.stButton > button:hover {{
        transform: scale(1.03) !important;
        background-color: white !important;
        color: {BRAND_NAVY} !important;
        border-color: {BRAND_GOLD} !important;
    }}

    /* Blokkeer Streamlit Blauw bij klik */
    div.stButton > button:focus, div.stButton > button:active {{
        background-color: white !important;
        color: {BRAND_NAVY} !important;
        border-color: {BRAND_GOLD} !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* 2D. De Witte Top Header (Strak tegen de rand) */
    .white-top-header {{
        background-color: #FFFFFF;
        width: 100%;
        padding: 15px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 3px solid {BRAND_GOLD};
        margin-top: -85px; /* Schuift de balk volledig over de verborgen header */
    }}

    .main .block-container {{
        padding-top: 0rem !important;
        max-width: 95%;
    }}

    /* Sidebar toggle knop styling */
    button[data-testid="stSidebarCollapseButton"] {{
        color: {BRAND_NAVY} !important;
        background-color: white !important;
        border: 1px solid {BRAND_GOLD} !important;
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

# Ticker Tape (Gereduceerd naar 58px: perfecte balans)
components.html("""
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?locale=en&colorTheme=dark&isTransparent=true&displayMode=adaptive" 
    width="100%" height="58" frameborder="0" style="display:block; margin:0;"></iframe>
""", height=58)

# --- 5. MAIN CONTENT ---
st.title(f"{st.session_state.page}")
st.markdown(f"*{datetime.now().strftime('%d %B %Y')} - Institutional Data Feed*")

def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        unique_id = f"{prefix}_{i}"
        with cols[i % 3]:
            # FIX: We gebruiken opacity in plaats van display:none zodat de chart op de achtergrond laadt
            card_html = f"""
            <style>
                .asset-container {{
                    background:#131722; border:1px solid {BRAND_GOLD}44; border-radius:12px; 
                    height:520px; overflow:hidden; margin-bottom:25px; position:relative; cursor:pointer;
                }}
                .static-view, .chart-view {{
                    position: absolute; width: 100%; height: 100%; 
                    top: 0; left: 0; transition: opacity 0.4s ease;
                }}
                .chart-view {{ opacity: 0; pointer-events: none; }}
                .asset-container:hover .static-view {{ opacity: 0; pointer-events: none; }}
                .asset-container:hover .chart-view {{ opacity: 1; pointer-events: auto; }}
            </style>
            
            <div class="asset-container">
                <div class="static-view">
                    <iframe src="https://www.tradingview.com/embed-widget/symbol-info/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="160" frameborder="0"></iframe>
                    <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol={asset['s']}&colorTheme=dark&isTransparent=true&interval=1D" width="100%" height="360" frameborder="0"></iframe>
                </div>
                <div class="chart-view">
                    <iframe src="https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol={asset['s']}&colorTheme=dark&width=100%&height=100%&dateRange=12M" width="100%" height="100%" frameborder="0"></iframe>
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
