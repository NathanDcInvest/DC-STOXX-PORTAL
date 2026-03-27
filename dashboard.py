import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import time

# --- 1. CONFIG & BRANDING ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"

st.set_page_config(page_title="DC STOXX Portal", layout="wide", initial_sidebar_state="expanded")

# Geavanceerde CSS voor de "Clean Header" look
st.markdown(f"""
    <style>
    /* Algemene achtergrond */
    .stApp {{ background-color: {BRAND_NAVY}; color: white; }}
    [data-testid="stSidebar"] {{ background-color: {BRAND_NAVY}; border-right: 2px solid {BRAND_GOLD}; }}
    
    /* Verwijder alle Streamlit witruimte bovenaan */
    [data-testid="stHeader"] {{ display: none; }}
    .main .block-container {{ padding-top: 0rem !important; padding-bottom: 0rem !important; max-width: 98%; }}
    
    /* De Ticker Tape Container (Absolute Top) */
    .ticker-wrapper {{
        width: 100%;
        height: 50px;
        background-color: {BRAND_NAVY};
    }}

    /* De Witte Logo Balk (Direct onder Ticker) */
    .corporate-header {{
        background-color: #FFFFFF;
        width: 100%;
        padding: 5px 0;
        border-bottom: 3px solid {BRAND_GOLD};
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; padding-top: 15px; }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px; color: #8892B0; font-weight: 600; font-size: 16px;
    }}
    .stTabs [aria-selected="true"] {{ 
        border-bottom: 3px solid {BRAND_GOLD} !important; color: {BRAND_GOLD} !important; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DE ABSOLUTE BOVENKANT: TICKER TAPE ---
# We zetten deze in een container zonder marges
components.html("""
    <div style="margin: -8px -8px 0 -8px;">
        <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?locale=en&colorTheme=dark&isTransparent=false&backgroundColor=%230A1B2E&displayMode=adaptive" 
        width="100%" height="46" frameborder="0"></iframe>
    </div>
""", height=46)

# --- 3. DE WITTE HEADER MET LOGO (Direct eronder) ---
st.markdown('<div style="background-color: white; border-bottom: 3px solid #B89B5E; padding: 8px 0; margin-top: -10px;">', unsafe_allow_html=True)
col_l, col_logo, col_r = st.columns([1, 0.5, 1])
with col_logo:
    try:
        # We laden het logo centraal
        st.image("Logo.png", use_container_width=True)
    except:
        st.markdown("<h2 style='color:black; text-align:center; margin:0;'>DC STOXX</h2>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SIDEBAR (News Feed) ---
with st.sidebar:
    st.markdown(f"<h3 style='text-align:center; color:{BRAND_GOLD}; letter-spacing:3px; font-weight:bold; margin-top:10px;'>INTELLIGENCE</h3>", unsafe_allow_html=True)
    st.markdown("---")
    components.html(f"""
        <iframe src="https://www.tradingview.com/embed-widget/timeline/?locale=en&colorTheme=dark&isTransparent=true&displayMode=adaptive" 
        width="100%" height="1000" frameborder="0"></iframe>
    """, height=1000)

# --- 5. SUB-HEADER (Status & Welkom) ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown(f"<p style='color:{BRAND_GOLD}; font-size:1rem; margin-top:10px;'>Institutional Portfolio Interface | {datetime.now().strftime('%d %b %Y')}</p>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='text-align:right;'><p style='color:#00ff88; margin-top:10px;'>● TERMINAL LIVE</p></div>", unsafe_allow_html=True)

# --- 6. DATASET ---
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
others = [
    {"n": "Bitcoin", "s": "BINANCE:BTCUSDT"}, {"n": "Ethereum", "s": "BINANCE:ETHUSDT"},
    {"n": "Solana", "s": "BINANCE:SOLUSDT"}, {"n": "Gold", "s": "TVC:GOLD"},
    {"n": "Crude Oil", "s": "TVC:USOIL"}
]

# --- 7. TABS ---
tab_equities, tab_overview, tab_crypto, tab_screener = st.tabs([
    "📈 Equities", "📊 Market Overview", "₿ Crypto & Commodities", "🔍 Pro Screener"
])

def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        unique_id = f"{prefix}_{i}"
        with cols[i % 3]:
            card_html = f"""
            <style>
                body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; overflow: hidden; }}
                .container {{ 
                    position: relative; width: 98%; height: 550px; 
                    border: 1px solid {BRAND_GOLD}33; border-radius: 12px; 
                    background: #131722; cursor: pointer; transition: 0.3s;
                }}
                .container:hover {{ border-color: {BRAND_GOLD}; box-shadow: 0 0 15px {BRAND_GOLD}44; }}
                .static, .chart {{ position: absolute; width: 100%; height: 100%; transition: opacity 0.3s; }}
                .chart {{ opacity: 0; visibility: hidden; }}
                .container:hover .static {{ opacity: 0; }}
                .container:hover .chart {{ opacity: 1; visibility: visible; }}
            </style>
            <div class="container">
                <div class="static">
                    <iframe src="https://www.tradingview.com/embed-widget/symbol-info/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="180" frameborder="0"></iframe>
                    <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol={asset['s']}&colorTheme=dark&isTransparent=true&interval=1D" width="100%" height="360" frameborder="0"></iframe>
                </div>
                <div class="chart">
                    <div id="tv_{unique_id}" style="height:100%;"></div>
                    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                    <script>
                    new TradingView.widget({{
                        "autosize": true, "symbol": "{asset['s']}", "interval": "D", "timezone": "Etc/UTC", "theme": "dark", "style": "3", "locale": "en", "range": "12M", "container_id": "tv_{unique_id}"
                    }});
                    </script>
                </div>
            </div>
            """
            components.html(card_html, height=560)

with tab_equities:
    render_portal_grid(equities, "eq")

with tab_overview:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("S&P 500 Heatmap")
        components.html('<iframe src="https://www.tradingview.com/embed-widget/stock-heatmap/?colorTheme=dark&isTransparent=true&index=SPX500" width="100%" height="600" frameborder="0"></iframe>', height=620)
    with col_r:
        st.subheader("Global Indices")
        components.html('<iframe src="https://www.tradingview.com/embed-widget/markets/?colorTheme=dark&isTransparent=true" width="100%" height="600" frameborder="0"></iframe>', height=620)

with tab_crypto:
    render_portal_grid(others, "cry")

with tab_screener:
    st.subheader("Professional Stock Screener")
    components.html('<iframe src="https://www.tradingview.com/embed-widget/screener/?colorTheme=dark&isTransparent=true" width="100%" height="800" frameborder="0"></iframe>', height=820)
