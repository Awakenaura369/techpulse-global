import streamlit as st
import requests
from groq import Groq
import urllib.parse
import streamlit.components.v1 as components

# --- 1. إعدادات SEO (ما نسينا والو) ---
SITE_URL = "https://techpulse-global.streamlit.app/"
params = st.query_params

if "google8c04de4f0fa47f61" in str(params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html"); st.stop()
if "robots.txt" in str(params):
    st.text("User-agent: *\nDisallow: /_stcore/\nSitemap: " + SITE_URL + "sitemap.xml"); st.stop()

# --- 2. الستايل الاحترافي (نفس اللي عجبك) ---
st.set_page_config(page_title="TechPulse AI | Pro Intel", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Orbitron:wght@900&display=swap');
    .stApp { background-color: #010409; color: #E6EDF3; font-family: 'Inter', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; text-align: center; padding: 20px; }
    .main-header h1 { color: #58A6FF; font-size: 48px; margin-bottom: 0; text-shadow: 0 0 15px rgba(88, 166, 255, 0.5); }
    .market-mood { background: #0D1117; border-radius: 15px; padding: 20px; border: 1px solid #30363D; margin-bottom: 30px; }
    .mood-bullish { color: #3FB950; font-weight: bold; }
    .news-card { background: #0D1117; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 25px; overflow: hidden; }
    .news-content { padding: 20px; }
    .news-title { font-size: 22px; font-weight: bold; color: #F0F6FC; margin-bottom: 10px; }
    .risk-alert { display: inline-block; background: rgba(248, 81, 73, 0.1); color: #F85149; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid #F85149; margin-bottom: 10px; }
    .stButton>button { background: #1F6FEB; color: white; border-radius: 6px; font-weight: 600; width: 100%; border: none; height: 45px; }
    .stButton>button:hover { background: #388BFD; }
    </style>
""", unsafe_allow_html=True)

# --- 3. المحرك ---
@st.cache_data(ttl=3600)
def fetch_pro_news():
    try:
        api_key = st.secrets["NEWS_API_KEY"].strip()
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={api_key}'
        r = requests.get(url).json()
        return r.get('articles', []) if r.get("status") == "ok" else []
    except: return []

def ai_analysis(title):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Analyze impact for investors: {title}"}]
        )
        return chat.choices[0].message.content
    except: return "Analysis stream stabilizing..."

# --- 4. العرض ---
st.markdown('<div class="main-header"><h1>TECH PULSE AI ⚡</h1><p>ADVANCED BI-DIRECTIONAL TECH INTELLIGENCE</p></div>', unsafe_allow_html=True)

# Adsterra Top
components.html('<div style="text-align:center;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

st.markdown('<div class="market-mood"><div style="font-size:20px;">Market Mood: <span class="mood-bullish">🚀 BULLISH (High Interest)</span></div></div>', unsafe_allow_html=True)

articles = fetch_pro_news()

if articles:
    for i, art in enumerate(articles):
        with st.container():
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            
            st.markdown('<div class="news-content">', unsafe_allow_html=True)
            st.markdown('<div class="risk-alert">INTEL UPDATE</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="news-title">{art["title"]}</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    st.info(ai_analysis(art['title']))
            with c2:
                # --- الرابط السحري لنشر تويتر بدون الحاجة لـ API Key مدفوع ---
                tweet_text = f"⚡ NEW INTEL: {art['title']}\n\n🔗 Deep Dive: {SITE_URL}"
                tweet_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
                st.markdown(f'<a href="{tweet_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#1F6FEB; color:white; padding:10px; border-radius:6px; text-align:center; font-weight:600; height:25px;">🚀 SHARE ON X</div></a>', unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)

# Adsterra Bottom
components.html('<div style="text-align:center; margin-top:20px;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)
