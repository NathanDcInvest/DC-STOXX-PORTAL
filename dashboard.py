import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import time
import base64

# --- 1. CONFIG & BRANDING (Uit jouw HTML) ---
BRAND_GOLD = "#B89B5E"  # Messing/Goud kleur
BRAND_NAVY = "#0A1B2E"  # Diep Navy Blauw

st.set_page_config(page_title="DC STOXX Master Terminal", layout="wide", initial_sidebar_state="expanded")

# Geavanceerde CSS voor de Corporate Header, Sidebar Navigatie en Full Dark Look
st.markdown(f"""
    <style>
    /* Algemene achtergrond */
    .stApp {{ background-color: {BRAND_NAVY}; color: white; }}
    [data-testid="stSidebar"] {{ background-color: {BRAND_NAVY}; border-right: 2px solid {BRAND_GOLD}; }}
    
    /* Verwijder alle Streamlit witruimte bovenaan */
    [data-testid="stHeader"] {{ visibility: hidden; }}
    .main .block-container {{ 
        padding-top: 0rem !important; 
        padding-left: 0rem !important; 
        padding-right: 0rem !important; 
        max-width: 100%; 
    }}
    
    /* De "DC STOXX" sidebar navigatie knoppen */
    div[data-testid="stVerticalBlock"] > div.stButton {{ margin-bottom: 10px; }}
    .stButton>button {{
        color: {BRAND_GOLD} !important;
        border: 1px solid {BRAND_GOLD} !important;
        border-radius: 8px;
        background-color: {BRAND_NAVY};
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        text-align: left;
        padding-left: 15px;
        width: 100%;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {BRAND_GOLD};
        color: {BRAND_NAVY} !important;
    }}
    
    /* Zorg dat de content onder de header wel padding heeft */
    .content-wrapper {{ padding: 0 2rem; }}

    </style>
    """, unsafe_allow_html=True)

# Function to read Logo.png and convert to base64 for embedding
def get_base64_image(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- 2. DE VOLLEDIGE DATASET (27 Assets) ---
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
    {"n": "Bitcoin", "s": "BINANCE:BTCUSDT"}, 
    {"n": "Ethereum", "s": "BINANCE:ETHUSDT"},
    {"n": "Solana", "s": "BINANCE:SOLUSDT"},
    {"n": "Gold", "s": "TVC:GOLD"}, 
    {"n": "Crude Oil", "s": "TVC:USOIL"}
]

# --- 3. SIDEBAR (Logo & Lange Nieuwsfeed) ---
with st.sidebar:
    st.markdown(f"<h3 style='text-align:center; color:{BRAND_GOLD}; letter-spacing: 2px;'>INTELLIGENCE</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- JOUW LOGO IN SIDEBAR ---
    try:
        # We laden je lokale Logo.png
        st.image("Logo.png", use_container_width=True)
    except:
        # Als het bestand niet gevonden wordt, tonen we een tekst-titel
        st.title("DC STOXX")
    
    # Verlengde News Feed om deadspace te voorkomen (Height naar 1200px)
    news_html = f"""
    <iframe src="https://www.tradingview.com/embed-widget/timeline/?locale=en&colorTheme=dark&isTransparent=true&displayMode=adaptive" 
    width="100%" height="900" frameborder="0"></iframe>
    """
    components.html(news_html, height=910)

# --- 4. TOP: LIVE TICKER TAPE & WITTE CORPORATE HEADER (Het "Zero Mess" Blok) ---
# We gebruiken een base64 truc om het logo in de HTML te krijgen zonder externe links
try:
    logo_base64 = get_base64_image("Logo.png")
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height: 60px;">'
except:
    logo_html = f'<h1 style="color:{BRAND_NAVY}; margin:0; font-family:sans-serif;">DC STOXX</h1>'

# Ticker Tape en Witte Balk in één strak HTML-blok
header_html = f"""
<div style="width:100%; background-color:{BRAND_NAVY}; margin:0; padding:0; position: relative; z-index: 10;">
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?locale=en&colorTheme=dark&isTransparent=true&backgroundColor=%230A1B2E" 
    width="100%" height="46" frameborder="0" style="display:block; margin:0; margin-top: -10px;"></iframe>
    
    <div style="background-color: white; border-bottom: 4px solid {BRAND_GOLD}; padding: 10px 0; display: flex; justify-content: center; align-items: center; width: 100%;">
        {logo_html}
    </div>
</div>
"""
# We geven dit een vaste hoogte om de pagina direct te vullen
components.html(header_html, height=130)

# --- 5. CONTENT START (Binnen content-wrapper) ---
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# --- SUB-HEADER (Naam & Status - Opgekuist) ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown(f"<p style='color:{BRAND_GOLD}; font-size:1.1rem; margin-top:20px;'>Premium Institutional Investment Interface</p>", unsafe_allow_html=True)
with c2:
    # Datum wordt automatisch gegenereerd
    st.markdown(f"<div style='text-align:right;'><h2>{datetime.now().strftime('%d %b %Y')}</h2><p style='color:#00ff88;'>● GLOBAL MARKETS LIVE</p></div>", unsafe_allow_html=True)

# --- 6. HET GRID (Hover Magic - Nu met Technical Gauge om boxen te vullen!) ---
# Tabs zijn verwijderd, we tonen gewoon de hele lijst.

# Functie voor de Hover Cards (Boxen volledig gevuld met Gauge en Chart)
def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        unique_id = f"{prefix}_{i}"
        with cols[i % 3]:
            # De Static view bevat nu Symbol Info + Technical Gauge (Vult de box!)
            card_html = f"""
            <style>
                body {{ background: transparent; margin: 0; font-family: sans-serif; overflow: hidden; }}
                .container {{ 
                    position: relative; width: 98%; height: 550px; /* Groot genoeg gemaakt om boxen te vullen */
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
                    
                    <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol={asset['s']}&colorTheme=dark&isTransparent=true&interval=1D&showIntervalTabs=true" width="100%" height="360" frameborder="0"></iframe>
                </div>
                
                <div class="chart">
                    <div id="tv_{unique_id}" style="height:100%;"></div>
                    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                    <script>
                    new TradingView.widget({{
                        "autosize": true, "symbol": "{asset['s']}", 
                        "interval": "D", "timezone": "Etc/UTC", 
                        "theme": "dark", "style": "3", "locale": "en", 
                        "enable_publishing": false, "range": "12M", 
                        "container_id": "tv_{unique_id}"
                    }});
                    </script>
                </div>
            </div>
            """
            components.html(card_html, height=560)

st.markdown(f"<h2 style='border-left: 5px solid {BRAND_GOLD}; padding-left:15px; margin-top:30px;'>Investment Portfolio Overview</h2>", unsafe_allow_html=True)
# We tonen alle assets in één groot overzicht
render_portal_grid(equities + others, "eq")

# --- 7. HEATMAP ONDERAAN ---
st.markdown("---")
st.subheader("Global S&P 500 Market Heatmap")
heatmap_html = """
<iframe src="https://www.tradingview.com/embed-widget/stock-heatmap/?locale=en&colorTheme=dark&isTransparent=true&displayMode=adaptive&index=SPX500" 
width="100%" height="600" frameborder="0"></iframe>
"""
components.html(heatmap_html, height=620)

st.markdown('</div>', unsafe_allow_html=True) # Sluit content-wrapper
