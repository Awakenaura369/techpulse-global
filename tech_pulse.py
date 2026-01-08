import streamlit as st
import requests
from groq import Groq
import urllib.parse
import streamlit.components.v1 as components

# --- 1. SEO & Twitter Cards & Meta Tags ---
SITE_URL = "https://techpulse-global.streamlit.app/"
# رابط صورة المعاينة (تقدر تبدلو برابط لوغو ديالك)
PREVIEW_IMG = "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80"

st.set_page_config(page_title="TechPulse AI | Next-Gen Global Intel", layout="wide", page_icon="⚡")

# إدخال الميتا تاغز في الرأس
st.markdown(f"""
    <head>
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="TechPulse AI | Decoding the Future">
    <meta name="twitter:description" content="AI-powered tech intelligence and market analysis.">
    <meta name="twitter:image" content="{PREVIEW_IMG}">
    <meta name="description" content="Global Tech Intelligence powered by AI.">
    </head>
""", unsafe_allow_html=True)

# --- 2. إدارة الصفحات القانونية (Hidden logic) ---
params = st.query_params
if "page" in params:
    page = params["page"]
    if page == "privacy":
        st.title("Privacy Policy")
        st.write("We value your privacy. Your data is secure with TechPulse AI. We do not sell personal information.")
        st.stop()
    elif page == "terms":
        st.title("Terms of Service")
        st.write("By using TechPulse AI, you agree to our terms of automated news delivery and AI analysis.")
        st.stop()
    elif page == "google8c04de4f0fa47f61":
        st.write("google-site-verification: google8c04de4f0fa47f61.html")
        st.stop()

# --- 3. Futuristic UI Style ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Orbitron:wght@900&display=swap');
    .stApp { background-color: #010409; color: #E6EDF3; font-family: 'Inter', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; text-align: center; padding: 20px; }
    .main-header h1 { color: #58A6FF; font-size: 45px; margin-bottom: 0; text-shadow: 0 0 15px rgba(88, 166, 255, 0.4); }
    .market-mood { background: #0D1117; border-radius: 12px; padding: 15px; border: 1px solid #30363D; margin-bottom: 25px; text-align: center; }
    .news-card { background: #0D1117; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 25px; overflow: hidden; transition: 0.3s; }
    .news-card:hover { border-color: #58A6FF; }
    .news-content { padding: 20px; }
    .news-title { font-size: 22px; font-weight: bold; color: #F0F6FC; margin-bottom: 10px; }
    .footer { text-align: center; padding: 40px; color: #8B949E; font-size: 13px; border-top: 1px solid #30363D; margin-top: 50px; }
    .footer a { color: #58A6FF; text-decoration: none; margin: 0 10px; }
    .stButton>button { background: #1F6FEB; color: white; border-radius: 6px; font-weight: 600; width: 100%; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- 4. The Intelligence Logic ---
@st.cache_data(ttl=3600)
def fetch_news():
    try:
        api_key = st.secrets["NEWS_API_KEY"].strip()
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={api_key}'
        r = requests.get(url).json()
        return r.get('articles', [])
    except: return []

def ai_analyze(title):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Brief market impact: {title}"}]
        )
        return chat.choices[0].message.content
    except: return "AI analysis channel is busy..."

# --- 5. Main Page Content ---
st.markdown('<div class="main-header"><h1>TECH PULSE AI ⚡</h1><p>GLOBAL INTELLIGENCE NODE</p></div>', unsafe_allow_html=True)

# Adsterra Top
components.html('<div style="text-align:center;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

st.markdown('<div class="market-mood">Sentiment Index: <span style="color:#3FB950; font-weight:bold;">🚀 BULLISH (+78%)</span></div>', unsafe_allow_html=True)

articles = fetch_news()

if articles:
    for i, art in enumerate(articles):
        with st.markdown('<div class="news-card">', unsafe_allow_html=True):
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            
            st.markdown('<div class="news-content">', unsafe_allow_html=True)
            st.markdown(f'<div class="news-title">{art["title"]}</div>', unsafe_allow_html=True)
            st.write(f"🌐 {art['source']['name']} | 📅 2026-01-08") # تاريخ اليوم كما طلبت
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    st.info(ai_analyze(art['title']))
            with c2:
                tweet_text = f"⚡ INTEL: {art['title']}\n\n🔗 Full Report: {SITE_URL}"
                tweet_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
                st.markdown(f'<a href="{tweet_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#1F6FEB; color:white; padding:10px; border-radius:6px; text-align:center; font-weight:600;">🚀 SHARE ON X</div></a>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

# Adsterra Bottom
components.html('<div style="text-align:center; margin-top:20px;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

# --- 6. Footer الاحترافي ---
st.markdown(f"""
    <div class="footer">
        <p>© 2026 <b>TechPulse Global AI</b>. All rights reserved.</p>
        <p>
            <a href="?page=privacy">Privacy Policy</a> | 
            <a href="?page=terms">Terms of Service</a> | 
            <a href="mailto:contact@techpulse-global.com">Contact Support</a>
        </p>
        <p style="font-size:10px; opacity:0.5; margin-top:10px;">Quantum-Encrypted Interface Node: TP-2026-X7</p>
    </div>
""", unsafe_allow_html=True)
