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
        background-color: white !important; /* Altijd wit */
        color: {BRAND_NAVY} !important;    /* Altijd navy tekst */
        border: 2px solid {BRAND_NAVY} !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 12px 15px !important;
        transition: transform 0.2s ease-in-out, border-color 0.2s !important; /* Voor het enlarge effect */
        display: block !important;
    }}

    /* Hover effect: Box enlargen, kleur blijft wit */
    div.stButton > button:hover {{
        transform: scale(1.05) !important; /* Maakt de knop 5% groter */
        background-color: white !important;
        color: {BRAND_NAVY} !important;
        border-color: {BRAND_GOLD} !important; /* Alleen de rand wordt goud voor feedback */
    }}

    /* Voorkom Streamlit Blauw bij focus/klik */
    div.stButton > button:focus, div.stButton > button:active, div.stButton > button:focus-visible {{
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
        margin-top: -65px; /* Schuift het logo-blok over de lege header ruimte */
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
    
    # Knoppen met de nieuwe 'enlarge' styling
    if st.button("📈 Equities"): st.session_state.page = "📈 Equities"
    if st.button("₿ Crypto"): st.session_state.page = "₿ Crypto"
    if st.button("🛢️ Commodities"): st.session_state.page = "🛢️ Commodities & Oil"
    if st.button("📊 Heat Map"): st.session_state.page = "📊 Heat Map"
    
    st.markdown("---")
    st.markdown(f"<p style='font-weight:bold; color:{BRAND_NAVY};'>MARKET INTELLIGENCE</p>", unsafe_allow_html=True)
    
    components.html("""
        <iframe src="https://www.tradingview.com/embed-widget/timeline/?colorTheme=light&isTransparent=true&displayMode=adaptive" 
        width="100%" height="800" frameborder="0"></iframe>
    """, height=800)

# --- 4. TOP HEADER & TICKER ---
# Witte balk met Logo
st.markdown('<div class="white-top-header">', unsafe_allow_html=True)
c1, c_logo, c2 = st.columns([1, 0.7, 1])
with c_logo:
    try:
        st.image("Logo.png", use_container_width=True)
    except:
        st.markdown(f"<h2 style='color:{BRAND_NAVY}; text-align:center;'>STOXX</h2>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Ticker Tape (Hoogte op 62px: ideaal voor leesbaarheid zonder bulk)
components.html("""
    <iframe src="https://www.tradingview.com/embed-widget/ticker-tape/?locale=en&colorTheme=dark&isTransparent=true&displayMode=adaptive" 
    width="100%" height="62" frameborder="0" style="display:block; margin:0;"></iframe>
""", height=62)

# --- 5. MAIN CONTENT ---
st.title(f"{st.session_state.page}")
st.markdown(f"*{datetime.now().strftime('%d %B %Y')} - Institutional Data Feed*")

def render_portal_grid(asset_list, prefix):
    cols = st.columns(3)
    for i, asset in enumerate(asset_list):
        unique_id = f"{prefix}_{i}"
        with cols[i % 3]:
            card_html = f"""
            <div style="background:#131722; border:1px solid {BRAND_GOLD}44; border-radius:12px; height:520px; overflow:hidden; margin-bottom:25px; position:relative; cursor:pointer;"
                 onmouseover="this.querySelector('.static').style.display='none'; this.querySelector('.chart').style.display='block';"
                 onmouseout="this.querySelector('.static').style.display='block'; this.querySelector('.chart').style.display='none';">
                
                <div class="static" style="display:block; height:100%;">
                    <iframe src="https
