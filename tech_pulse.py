import streamlit as st
import requests
from groq import Groq
import tweepy
import streamlit.components.v1 as components

# --- 1. SEO & Legal ---
SITE_URL = "https://techpulse-global.streamlit.app/"
params = st.query_params

if "google8c04de4f0fa47f61" in str(params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html"); st.stop()
if "robots.txt" in str(params):
    st.text("User-agent: *\nSitemap: " + SITE_URL + "sitemap.xml"); st.stop()

# --- 2. Futuristic UI ---
st.set_page_config(page_title="TechPulse AI", layout="wide", page_icon="⚡")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #010409; color: #e6edf3; }
    .main-title { font-family: 'Orbitron', sans-serif; background: linear-gradient(90deg, #00CCFF, #d2a8ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 45px; text-align: center; font-weight: 900; padding: 15px; }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Optimized Engine ---
@st.cache_data(ttl=3600) # كاش لمدة ساعة كاملة باش تحافظ على الساروت
def fetch_news_limited():
    try:
        api_key = st.secrets["NEWS_API_KEY"].strip()
        # طلبنا 5 ديال الأخبار فقط
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={api_key}'
        r = requests.get(url).json()
        if r.get("status") == "ok": return r.get('articles', [])
        return []
    except: return []

def post_to_x_safe(title):
    try:
        client = tweepy.Client(
            consumer_key=st.secrets["X_API_KEY"].strip(),
            consumer_secret=st.secrets["X_API_SECRET"].strip(),
            access_token=st.secrets["X_ACCESS_TOKEN"].strip(),
            access_token_secret=st.secrets["X_ACCESS_SECRET"].strip()
        )
        content = f"⚡ INTEL: {title[:150]}...\n\n🔗 Deep Dive: {SITE_URL}\n\n#AI #Tech"
        client.create_tweet(text=content)
        return True
    except: return False

# --- 4. Content Delivery ---
st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

# Adsterra Top
components.html('<div style="text-align:center;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

articles = fetch_news_limited()

# أتمتة ذكية: تنشر فقط إذا كان الرابط يحتوي على auto_post
if "auto_post" in str(params) and articles:
    post_to_x_safe(articles[0]['title'])
    st.toast("Auto-Post Dispatched!")

if not articles:
    st.info("📡 Scanning for signals... (Check back in 1 hour or update API Key)")
else:
    for i, art in enumerate(articles):
        with st.markdown(f'<div class="glass-card">', unsafe_allow_html=True):
            st.markdown(f"### 🛡️ {art['title']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    st.info("AI is analyzing this trend...")
            with col2:
                if st.button(f"🚀 SHARE ON X", key=f"x_{i}"):
                    if post_to_x_safe(art['title']): st.success("Shared!")
        st.markdown('</div>', unsafe_allow_html=True)

# Adsterra Bottom
components.html('<div style="text-align:center; margin-top:20px;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)
