import streamlit as st
import requests
from groq import Groq
import urllib.parse
import streamlit.components.v1 as components

# --- 1. SEO & Twitter Cards ---
SITE_URL = "https://techpulse-global.streamlit.app/"
PREVIEW_IMG = "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80"

st.set_page_config(page_title="TechPulse AI | Global Node", layout="wide", page_icon="⚡")

st.markdown(f"""
    <head>
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="TechPulse AI | Global Node">
    <meta name="twitter:image" content="{PREVIEW_IMG}">
    </head>
""", unsafe_allow_html=True)

# --- 2. Futuristic UI Style ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Orbitron:wght@900&display=swap');
    .stApp { background-color: #010409; color: #E6EDF3; font-family: 'Inter', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; text-align: center; padding: 20px; }
    .main-header h1 { color: #58A6FF; font-size: 45px; margin-bottom: 0; }
    .market-mood { background: #0D1117; border-radius: 12px; padding: 15px; border: 1px solid #30363D; margin-bottom: 25px; text-align: center; }
    .news-card { background: #0D1117; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 25px; overflow: hidden; }
    .news-content { padding: 20px; }
    .news-title { font-size: 22px; font-weight: bold; color: #F0F6FC; margin-bottom: 10px; }
    .footer { text-align: center; padding: 40px; color: #8B949E; font-size: 13px; border-top: 1px solid #30363D; margin-top: 50px; }
    .footer a { color: #58A6FF; text-decoration: none; margin: 0 10px; }
    /* بوطونات شير و AI */
    .stButton>button { background: #1F6FEB !important; color: white !important; border-radius: 6px !important; border: none !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة الصفحات القانونية (Logic Fixed) ---
params = st.query_params
show_main_content = True

if "page" in params:
    p = params["page"]
    if p in ["privacy", "terms"]:
        show_main_content = False
        if p == "privacy":
            st.title("Privacy Policy")
            st.write("Privacy is our priority. Your data is never shared.")
        else:
            st.title("Terms of Service")
            st.write("Usage of TechPulse AI is subject to international digital laws.")
        if st.button("← Back to News"):
            st.query_params.clear()
            st.rerun()

# --- 4. المحرك الرئيسي (Engine) ---
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
            messages=[{"role": "user", "content": f"Quick analysis for investors: {title}"}]
        )
        return chat.choices[0].message.content
    except: return "AI Link Stable. Try again."

# --- 5. العرض الرئيسي (Main Logic) ---
if show_main_content:
    st.markdown('<div class="main-header"><h1>TECH PULSE AI ⚡</h1><p>2026 GLOBAL INTELLIGENCE</p></div>', unsafe_allow_html=True)
    
    # Adsterra Top
    components.html('<div style="text-align:center;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

    st.markdown('<div class="market-mood">Sentiment Index: <span style="color:#3FB950; font-weight:bold;">🚀 BULLISH (+78%)</span></div>', unsafe_allow_html=True)

    articles = fetch_news()
    if articles:
        for i, art in enumerate(articles):
            with st.container():
                st.markdown('<div class="news-card">', unsafe_allow_html=True)
                if art.get('urlToImage'):
                    st.image(art['urlToImage'], use_container_width=True)
                
                st.markdown('<div class="news-content">', unsafe_allow_html=True)
                st.markdown(f'<div class="news-title">{art["title"]}</div>', unsafe_allow_html=True)
                st.write(f"🌐 {art['source']['name']} | 📅 2026-01-08")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                        st.info(ai_analyze(art['title']))
                with c2:
                    t_text = f"⚡ INTEL: {art['title']}\n\n🔗 Report: {SITE_URL}"
                    t_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(t_text)}"
                    st.markdown(f'<a href="{t_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#1F6FEB; color:white; padding:10px; border-radius:6px; text-align:center; font-weight:600;">🚀 SHARE ON X</div></a>', unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True)

    # Adsterra Bottom
    components.html('<div style="text-align:center; margin-top:20px;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

# --- 6. Footer ---
st.markdown(f"""
    <div class="footer">
        <p>© 2026 <b>TechPulse Global AI</b>. All rights reserved.</p>
        <p>
            <a href="?page=privacy" target="_self">Privacy Policy</a> | 
            <a href="?page=terms" target="_self">Terms of Service</a> | 
            <a href="mailto:contact@techpulse-global.com">Contact Support</a>
        </p>
    </div>
""", unsafe_allow_html=True)
