import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. CONFIG & SESSION STATE ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"

# Pagina instellingen (MOET de eerste streamlit regel zijn)
st.set_page_config(page_title="DC STOXX Portal", layout="wide", initial_sidebar_state="expanded")

# Navigatie default instellen op Equities (Front Page)
if 'page' not in st.session_state:
    st.session_state.page = "📈 Equities"

# --- 2. HET GROTE VISUELE STYLING BLOK (CSS Injection) ---
# We forceren de website in de nieuwe "institutionele" lay-out
st.markdown(f"""
    <style>
    /* 2A. Algemene Pagina & Hoofdpagina Achtergrond (Navy) */
    .stApp {{
        background-color: {BRAND_NAVY};
        color: white;
    }}
    [data-testid="stSidebar"] {{
        border-right: 2px solid {BRAND_GOLD};
    }}
    
    /* 2B. De Grote Witte Sidebar (Links) */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: #FFFFFF !important;
        width: 300px !important; /* Lekker dik */
        color: black !important;
    }}
    [data-testid="stSidebar"] * {{
        color: black !important;
    }}
    
    /* 2C. Sidebar Knoppen (Visually Pleasing Contrast) */
    div.stButton > button {{
        width: 100%;
        background-color: transparent !important;
        color: {BRAND_NAVY} !important; /* Marineblauw tekst */
        border: 2px solid {BRAND_NAVY} !important; /* Marineblauw rand */
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: 0.3s !important;
        text-align: left !important;
        padding-left: 15px !important;
    }}
    div.stButton > button:hover {{
        background-color: {BRAND_NAVY} !important; /* Vul marineblauw */
        color: {BRAND_GOLD} !important; /* Goud tekst bij hover */
        border-color: {BRAND_GOLD} !important;
    }}
    
    /* 2D. De Prominente Witte Top Header (Logo Balk) */
    .white-top-header {{
        background-color: #FFFFFF;
        width: 100%;
        padding: 10px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 3px solid {BRAND_GOLD};
        margin-bottom: 0px;
    }}
    
    /* 2E. Streamlit UI Schoonmaak */
    /* Verberg de standaard Streamlit header balk */
    [data-testid="stHeader"] {{
        visibility: hidden;
    }}
    /* Verwijder standaard padding bovenaan de pagina */
    .main .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 95%; /* Iets smaller voor een terminal gevoel */
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (HET WITTE MENU LINKS) ---
with st.sidebar:
    st.markdown(f"<h1 style='text-align:center; color:{BRAND_NAVY} !important; margin-top:20px;'>DC STOXX</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{BRAND_GOLD} !important; font-weight:bold;'>MASTER TERMINAL</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Hier maken we de snelkoppelingen in de gevraagde volgorde
    if st.button("📈 Equities"): st.session_state.page = "📈 Equities"
    if st.button("₿ Crypto"): st.session_state.page = "₿ Crypto"
    if st.button("🛢️ Commodities & Oil"): st.session_state.page = "🛢️ Commodities & Oil"
    
    # Heat Map is de LAATSTE knop
    if st.button("📊 Heat Map"): st.session_state.page = "📊 Heat Map"
    
    st.markdown("---")
    st.markdown(f"<p style='color:{BRAND_NAVY} !important; font-weight:bold; padding-left:10px;'>WORLD NEWS INTEL</p>", unsafe_allow_html=True)
    
    # News Feed langer gemaakt om deadspace te voorkomen
    components.html("""
        <iframe src="https://www.tradingview.com/embed-widget/timeline/?colorTheme=light&isTransparent=true&displayMode=adaptive" 
        width="100%" height="900" frameborder="0"></iframe>
    """, height=900)

# --- 4. TOP: HET WITTE HEADER & TICKER BLOK (Zero Mess) ---

# 4A. Witte Balk met Centraal Logo (Volgens de Paint schets)
# We gebruiken st.columns om het logo te centreren binnen deze balk
with st.container():
    # De CSS die we bovenaan hebben gezet zorgt voor de witte balk
    st.markdown('<div class="white-top-header">', unsafe_allow_html=True)
    col_l, col_logo, col_r = st.columns([1, 0.7, 1])
    with col_logo:
        try:
            st.image("Logo.png", use_container_width=True)
        except:
            st.markdown(f"<h1 style='color:{BRAND_NAVY}; text-align:center; margin:0;'>STOXX</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4B. Ticker Tape DIRECT ONDER de witte balk (Zoals gevraagd)
components.html("""
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?colorTheme=dark&isTransparent=true" 
    width="100%" height="50" frameborder="0" style="display:block; margin:0;"></iframe>
""", height=50)

# --- 5. MAIN CONTENT AREA ---
st.title(f"{st.session_state.page} Intelligence Dashboard")
st.markdown(f"*{datetime.now().strftime('%d %B %Y')} - Institutional Intelligence Interface*")

# --- DATASET & FUNCTIES (v7.1 look behouden) ---
def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        unique_id = f"{prefix}_{i}"
        with cols[i % 3]:
            # De "Hover" logica blijft in HTML
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

# De Volledige Dataset (Alle 22 uit v7.1)
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

# --- CONTENT LOGICA (if/elif) ---

if st.session_state.page == "📈 Equities":
    # 22 Boxen met de v7.1 Hover Magic
    render_portal_grid(equities_list, "eq")

elif st.session_state.page == "₿ Crypto":
    crypto_list = [
        {"n": "Bitcoin", "s": "BINANCE:BTCUSDT"}, {"n": "Ethereum", "s": "BINANCE:ETHUSDT"},
        {"n": "Solana", "s": "BINANCE:SOLUSDT"}, {"n": "Cardano", "s": "BINANCE:ADAUSDT"}
    ]
    render_portal_grid(crypto_list, "cry")

elif st.session_state.page == "🛢️ Commodities & Oil":
    commodities_list = [
        {"n": "Gold", "s": "TVC:GOLD"}, {"n": "Crude Oil", "s": "TVC:USOIL"},
        {"n": "Silver", "s": "TVC:SILVER"}, {"n": "Natural Gas", "s": "TVC:NATGAS"}
    ]
    render_portal_grid(commodities_list, "com")

elif st.session_state.page == "📊 Heat Map":
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("Global S&P 500 Heatmap")
        components.html('<iframe src="https://www.tradingview.com/embed-widget/stock-heatmap/?colorTheme=dark&isTransparent=true&index=SPX500" width="100%" height="600" frameborder="0"></iframe>', height=620)
    with col_r:
        st.subheader("Indices Overview")
        components.html('<iframe src="https://www.tradingview.com/embed-widget/markets/?colorTheme=dark&isTransparent=true" width="100%" height="600" frameborder="0"></iframe>', height=620)
