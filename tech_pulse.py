import streamlit as st
import requests
from groq import Groq
import tweepy
import streamlit.components.v1 as components

# --- 1. SEO & Core Settings ---
SITE_URL = "https://techpulse-global.streamlit.app/"
params = st.query_params

if "google8c04de4f0fa47f61" in str(params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html"); st.stop()
if "robots.txt" in str(params):
    st.text("User-agent: *\nDisallow: /_stcore/\nSitemap: " + SITE_URL + "sitemap.xml"); st.stop()

# --- 2. Advanced UI Style (The Pro Look) ---
st.set_page_config(page_title="TechPulse AI | Pro Intel", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Orbitron:wght@900&display=swap');
    
    .stApp { background-color: #010409; color: #E6EDF3; font-family: 'Inter', sans-serif; }
    
    .main-header { font-family: 'Orbitron', sans-serif; text-align: center; padding: 20px; }
    .main-header h1 { color: #58A6FF; font-size: 48px; margin-bottom: 0; text-shadow: 0 0 15px rgba(88, 166, 255, 0.5); }
    .main-header p { color: #8B949E; font-size: 14px; letter-spacing: 2px; }
    
    .market-mood { background: #0D1117; border-radius: 15px; padding: 20px; border: 1px solid #30363D; margin-bottom: 30px; }
    .mood-title { font-size: 24px; font-weight: bold; }
    .mood-bullish { color: #3FB950; }
    
    .news-card { background: #0D1117; border: 1px solid #30363D; border-radius: 12px; padding: 0; margin-bottom: 25px; overflow: hidden; }
    .news-content { padding: 20px; }
    .news-title { font-size: 22px; font-weight: bold; color: #F0F6FC; margin-bottom: 10px; line-height: 1.3; }
    .news-meta { color: #8B949E; font-size: 13px; margin-bottom: 15px; }
    
    .risk-alert { display: inline-block; background: rgba(248, 81, 73, 0.1); color: #F85149; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid #F85149; margin-bottom: 10px; }
    
    img { border-bottom: 1px solid #30363D; transition: 0.3s; }
    img:hover { opacity: 0.8; }
    
    .stButton>button { background: #1F6FEB; color: white; border: none; border-radius: 6px; font-weight: 600; width: 100%; transition: 0.2s; }
    .stButton>button:hover { background: #388BFD; border-color: #8B949E; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Intelligence Logic ---
@st.cache_data(ttl=3600)
def fetch_pro_news():
    try:
        api_key = st.secrets["NEWS_API_KEY"].strip()
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={api_key}'
        r = requests.get(url).json()
        return r.get('articles', []) if r.get("status") == "ok" else []
    except: return []

def ai_market_analysis(title):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Analyze financial impact: {title}"}]
        )
        return chat.choices[0].message.content
    except: return "Analysis pending..."

# --- 4. The Professional Experience ---

# Header
st.markdown('<div class="main-header"><h1>TECH PULSE AI ⚡</h1><p>ADVANCED BI-DIRECTIONAL TECH INTELLIGENCE</p></div>', unsafe_allow_html=True)

# Adsterra Top
components.html('<div style="text-align:center;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

# Market Mood Section (كما في الصورة الواعرة)
st.markdown("""
<div class="market-mood">
    <div class="mood-title">Market Mood: <span class="mood-bullish">🚀 BULLISH (Positive)</span></div>
    <div style="background: #30363D; height: 8px; border-radius: 10px; margin-top: 15px;">
        <div style="background: #1F6FEB; width: 75%; height: 100%; border-radius: 10px;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

articles = fetch_pro_news()

if not articles:
    st.info("📡 Scanning secure channels...")
else:
    for i, art in enumerate(articles):
        with st.container():
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            
            # عرض الصورة بشكل احترافي
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            
            st.markdown('<div class="news-content">', unsafe_allow_html=True)
            st.markdown('<div class="risk-alert">RISK ALERT</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="news-title">{art["title"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="news-meta">🌐 {art["source"]["name"]} | 📅 {art['publishedAt'][:10]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    st.info(ai_market_analysis(art['title']))
            with col2:
                # بوطون تويتر المقتصد
                if st.button(f"🚀 SHARE ON X", key=f"x_{i}"):
                    st.success("Redirecting to X...")
            
            st.markdown('</div></div>', unsafe_allow_html=True)

# Adsterra Bottom
components.html('<div style="text-align:center; margin-top:30px;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)
