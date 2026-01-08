import streamlit as st
import requests
from groq import Groq
import tweepy
import streamlit.components.v1 as components

# --- 1. الإعدادات والتحقق (SEO & Meta) ---
SITE_URL = "https://techpulse-global.streamlit.app/"

# نظام التحقق التلقائي
params = st.query_params
if "google8c04de4f0fa47f61" in str(params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html")
    st.stop()
if "robots.txt" in str(params):
    st.text("User-agent: *\nDisallow: /_stcore/\nSitemap: " + SITE_URL + "sitemap.xml")
    st.stop()
if "sitemap.xml" in str(params):
    st.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE_URL}</loc></url></urlset>', unsafe_allow_html=True)
    st.stop()

# --- 2. واجهة المستخدم (The Beast UI Style) ---
st.set_page_config(page_title="TechPulse AI | Next-Gen Intelligence", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
    .stApp { background: radial-gradient(circle at top, #0d1117 0%, #010409 100%); color: #e6edf3; }
    .main-title { font-family: 'Orbitron', sans-serif; background: linear-gradient(90deg, #00CCFF, #d2a8ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; text-align: center; font-weight: 900; filter: drop-shadow(0 0 10px #00CCFF); padding: 20px; }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 25px; margin-bottom: 25px; transition: 0.4s; }
    .glass-card:hover { border-color: #00CCFF; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0, 204, 255, 0.2); }
    .stButton>button { background: linear-gradient(45deg, #00CCFF, #0066FF); color: white; border: none; border-radius: 10px; font-weight: bold; width: 100%; height: 45px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00CCFF; }
    .news-title { color: #ffffff; font-family: 'Orbitron', sans-serif; font-size: 20px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الدوال البرمجية (The Engine) ---
@st.cache_data(ttl=600)
def fetch_news():
    try:
        api_key = st.secrets["NEWS_API_KEY"].strip()
        # استعمال everything لضمان تدفق الأخبار باستمرار
        url = f'https://newsapi.org/v2/everything?q=technology%20OR%20AI&sortBy=publishedAt&language=en&apiKey={api_key}'
        r = requests.get(url).json()
        if r.get("status") == "ok":
            return r.get('articles', [])[:10]
        else:
            st.error(f"API Log: {r.get('message')}")
            return []
    except Exception as e:
        st.error(f"System Error: {e}")
        return []

def post_to_x(title):
    try:
        client = tweepy.Client(
            consumer_key=st.secrets["X_API_KEY"].strip(),
            consumer_secret=st.secrets["X_API_SECRET"].strip(),
            access_token=st.secrets["X_ACCESS_TOKEN"].strip(),
            access_token_secret=st.secrets["X_ACCESS_SECRET"].strip()
        )
        content = f"⚡ NEW INTEL: {title[:160]}...\n\n🔗 Deep Dive: {SITE_URL}\n\n#TechPulse #AI #Future"
        client.create_tweet(text=content)
        return True
    except Exception as e:
        st.error(f"X API Error: {e}")
        return False

def ai_analyze(title):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Briefly explain the market impact of this: {title}. Focus on investors."}]
        )
        return chat.choices[0].message.content
    except: return "Intelligence update in progress..."

# --- 4. العرض وتوزيع المحتوى ---
st.markdown('<div class="main-title">TECH PULSE AI</div>', unsafe_allow_html=True)

# إعلان Adsterra العلوي
components.html('<div style="text-align:center;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

articles = fetch_news()

# تفعيل الأتمتة لـ Cron-job
if "auto_post" in str(params) and articles:
    post_to_x(articles[0]['title'])

if not articles:
    st.warning("📡 Scanning the deep web for signals... Please wait.")
else:
    for i, art in enumerate(articles):
        with st.markdown(f'<div class="glass-card">', unsafe_allow_html=True):
            st.markdown(f'<div class="news-title">🛡️ {art["title"]}</div>', unsafe_allow_html=True)
            st.caption(f"Source: {art['source']['name']} | {art['publishedAt'][:10]}")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    st.info(ai_analyze(art['title']))
            with c2:
                if st.button(f"🚀 SHARE ON X", key=f"x_{i}"):
                    if post_to_x(art['title']):
                        st.success("Dispatched to X!")
        st.markdown('</div>', unsafe_allow_html=True)

# إعلان Adsterra السفلي
components.html('<div style="text-align:center; margin-top:30px;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

st.markdown('<p style="text-align:center; opacity:0.4; font-size:12px;">© 2026 TechPulse Global | Quantum-Secure Interface</p>', unsafe_allow_html=True)
