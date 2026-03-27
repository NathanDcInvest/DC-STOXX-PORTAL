import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. CONFIG & SESSION STATE ---
BRAND_GOLD = "#B89B5E"
BRAND_NAVY = "#0A1B2E"
BOX_BG = "#131722" 

st.set_page_config(page_title="DC STOXX Portal", layout="wide", initial_sidebar_state="expanded")

if 'page' not in st.session_state:
    st.session_state.page = "📈 Equities"

# --- 2. HET VISUELE STYLING BLOK (Met Mobile Optimizations!) ---
st.markdown(f"""
    <style>
    /* 2A. Verwijder ELKE vorm van witte balk boven het logo definitief */
    header[data-testid="stHeader"], .st-emotion-cache-18ni73i, .st-emotion-cache-v698uo {{
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
    }}
    
    .stApp {{
        background-color: #FFFFFF;
        color: {BRAND_NAVY};
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

    /* 2C. Sidebar Knoppen */
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
        transform: scale(1.05) !important; 
        background-color: white !important; 
        color: {BRAND_NAVY} !important;    
        border-color: {BRAND_GOLD} !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* 2D. De Witte Top Header */
    .white-top-header {{
        background-color: #FFFFFF;
        width: 100%;
        padding: 15px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 3px solid {BRAND_GOLD};
        margin-top: -120px; 
        position: relative;
        z-index: 999;
    }}

    .main .block-container {{
        padding-top: 0rem !important;
        margin-top: 0rem !important;
        max-width: 95%;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {BRAND_NAVY} !important;
    }}

    /* --- DE NIEUWE MOBILE CSS LOGICA (Media Queries) --- */
    .smart-tab {{
        flex: 1;
        text-align: center;
        line-height: 45px;
        cursor: pointer;
        font-family: sans-serif;
        font-weight: bold;
        font-size: 14px;
        transition: 0.3s;
    }}

    @media (max-width: 768px) {{
        .white-top-header {{
            margin-top: -60px !important; /* Voorkomt dat het logo buiten het iPhone scherm valt */
            padding: 10px 0 !important;
        }}
        .smart-tab {{
            font-size: 10.5px !important; /* Verkleint de tabtekst voor smalle touchscreens */
        }}
        .main .block-container {{
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }}
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

# Ticker Tape 
components.html("""
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?locale=en&colorTheme=dark&isTransparent=false&displayMode=adaptive" 
    width="100%" height="60" frameborder="0" style="display:block; margin:0;"></iframe>
""", height=60)

# --- 5. MAIN CONTENT AREA ---
st.title(f"{st.session_state.page}")
st.markdown(f"*{datetime.now().strftime('%d %B %Y')} - Institutional Intelligence*")

def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        # Streamlit regelt de mobiele val naar 1 kolom automatisch voor de loop!
        with cols[i % 3]:
            card_html = f"""
            <div style="background:{BOX_BG}; border:1px solid {BRAND_GOLD}; border-radius:12px; height:600px; overflow:hidden; margin-bottom:25px; display:flex; flex-direction:column; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                
                <div style="height:160px; width:100%;">
                    <iframe src="https://www.tradingview.com/embed-widget/symbol-info/?symbol={asset['s']}&colorTheme=dark&isTransparent=true" width="100%" height="160" frameborder="0" scrolling="no"></iframe>
                </div>
                
                <div style="display:flex; height:45px; border-top:1px solid {BRAND_GOLD}; border-bottom:1px solid {BRAND_GOLD}; background:{BRAND_NAVY}; z-index: 10;">
                    <div id="tab_chart_{i}" class="smart-tab" onclick="loadChart_{i}()" style="color:{BRAND_GOLD}; background:{BOX_BG}; border-right:1px solid {BRAND_GOLD};">
                        📊 CHART
                    </div>
                    <div id="tab_meter_{i}" class="smart-tab" onclick="loadMeter_{i}()" style="color:#8892B0; background:{BRAND_NAVY};">
                        ⏱️ TECHNICAL METER
                    </div>
                </div>
                
                <div style="position:relative; flex:1; width:100%;">
                    <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:#8892B0; font-family:sans-serif; font-size:12px; z-index:0;">
                        Loading Data...
                    </div>
                    <iframe id="dynamic_frame_{i}" src="https://s.tradingview.com/widgetembed/?symbol={asset['s']}&interval=D&theme=dark&style=1&hidesidetoolbar=0&withdateranges=1&symboledit=0&toolbarbg=131722&hideideas=1" width="100%" height="100%" frameborder="0" scrolling="no" style="position:relative; z-index:1; background:{BOX_BG};"></iframe>
                </div>

                <script>
                    var urlChart_{i} = "https://s.tradingview.com/widgetembed/?symbol={asset['s']}&interval=D&theme=dark&style=1&hidesidetoolbar=0&withdateranges=1&symboledit=0&toolbarbg=131722&hideideas=1";
                    var urlMeter_{i} = "https://www.tradingview.com/embed-widget/technical-analysis/?symbol={asset['s']}&colorTheme=dark&isTransparent=true&interval=1D";
                    
                    var currentTab_{i} = 'chart';

                    function loadChart_{i}() {{
                        if (currentTab_{i} !== 'chart') {{
                            document.getElementById('dynamic_frame_{i}').src = urlChart_{i};
                            currentTab_{i} = 'chart';
                        }}
                        document.getElementById('tab_chart_{i}').style.background = '{BOX_BG}';
                        document.getElementById('tab_chart_{i}').style.color = '{BRAND_GOLD}';
                        document.getElementById('tab_meter_{i}').style.background = '{BRAND_NAVY}';
                        document.getElementById('tab_meter_{i}').style.color = '#8892B0';
                    }}

                    function loadMeter_{i}() {{
                        if (currentTab_{i} !== 'meter') {{
                            document.getElementById('dynamic_frame_{i}').src = urlMeter_{i};
                            currentTab_{i} = 'meter';
                        }}
                        document.getElementById('tab_meter_{i}').style.background = '{BOX_BG}';
                        document.getElementById('tab_meter_{i}').style.color = '{BRAND_GOLD}';
                        document.getElementById('tab_chart_{i}').style.background = '{BRAND_NAVY}';
                        document.getElementById('tab_chart_{i}').style.color = '#8892B0';
                    }}
                </script>
            </div>
            """
            components.html(card_html, height=620)

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
    # MOBILE FIX: CSS Container gebruikt in plaats van de st.columns([1, 5, 1]) logica die mobiel breekt.
    components.html("""
    <div style="max-width: 1100px; margin: 0 auto; border: 1px solid #B89B5E; border-radius: 12px; overflow: hidden; background: #131722;">
        <iframe src="https://www.tradingview.com/embed-widget/stock-heatmap/?colorTheme=dark&isTransparent=true&index=SPX500" width="100%" height="850" frameborder="0" style="display: block;"></iframe>
    </div>
    """, height=870)
