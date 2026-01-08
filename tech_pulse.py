import streamlit as st
import requests
from groq import Groq
import tweepy
import streamlit.components.v1 as components

# --- 1. إعدادات SEO (ما نسينا والو) ---
SITE_URL = "https://techpulse-global.streamlit.app/"
params = st.query_params

if "google8c04de4f0fa47f61" in str(params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html"); st.stop()
if "robots.txt" in str(params):
    st.text("User-agent: *\nDisallow: /_stcore/\nSitemap: " + SITE_URL + "sitemap.xml"); st.stop()
if "sitemap.xml" in str(params):
    st.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE_URL}</loc></url></urlset>', unsafe_allow_html=True); st.stop()

# --- 2. الستايل النيوني (The Beast UI) ---
st.set_page_config(page_title="TechPulse AI", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
    .stApp { background-color: #010409; color: #ffffff; }
    .main-title { font-family: 'Orbitron', sans-serif; background: linear-gradient(90deg, #00CCFF, #d2a8ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 45px; text-align: center; font-weight: 900; padding: 20px; }
    .news-box { border-bottom: 1px solid #1f2937; padding: 20px 0; margin-bottom: 10px; }
    .stButton>button { background: linear-gradient(45deg, #00CCFF, #0066FF); color: white; border-radius: 8px; font-weight: bold; width: 100%; border: none; height: 45px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. المحرك (The Engine) ---
@st.cache_data(ttl=3600)
def fetch_intel():
    try:
        api_key = st.secrets["NEWS_API_KEY"].strip()
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={api_key}'
        r = requests.get(url).json()
        return r.get('articles', []) if r.get("status") == "ok" else []
    except: return []

def post_to_x(title):
    try:
        client = tweepy.Client(
            consumer_key=st.secrets["X_API_KEY"].strip(), consumer_secret=st.secrets["X_API_SECRET"].strip(),
            access_token=st.secrets["X_ACCESS_TOKEN"].strip(), access_token_secret=st.secrets["X_ACCESS_SECRET"].strip()
        )
        client.create_tweet(text=f"⚡ NEW INTEL: {title[:160]}...\n\n🔗 Analysis: {SITE_URL}\n\n#AI #Tech")
        return True
    except: return False

# --- 4. العرض (The Delivery) ---
st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

# الإعلان العلوي
components.html('<div style="text-align:center;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

articles = fetch_intel()

# الأتمتة
if "auto_post" in str(params) and articles:
    post_to_x(articles[0]['title'])

if not articles:
    st.warning("📡 Scanning quantum frequencies... News will appear here shortly.")
else:
    for i, art in enumerate(articles):
        # عرض العنوان بوضوح كبير
        st.markdown(f"### 🛡️ {art['title']}")
        st.write(f"🌐 {art['source']['name']} | 📅 {art['publishedAt'][:10]}")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                st.info("Analyzing this trend for investors...")
        with c2:
            if st.button(f"🚀 SHARE ON X", key=f"x_{i}"):
                if post_to_x(art['title']): st.success("Shared!")
        st.markdown("---")

# الإعلان السفلي
components.html('<div style="text-align:center; margin-top:20px;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)
