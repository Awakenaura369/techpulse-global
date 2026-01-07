import streamlit as st
import requests
from groq import Groq
import streamlit.components.v1 as components
from textblob import TextBlob
import os
from datetime import datetime
import urllib.parse

# الرابط الجديد ديالك
SITE_URL = "https://techpulse-global.streamlit.app/"

# ==========================================
# 1. نظام التحقق والسيت ماب بالرابط الصحيح
# ==========================================
query_params = st.query_params
if "google8c04de4f0fa47f61" in str(query_params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html")
    st.stop()

if "sitemap.xml" in str(query_params):
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>{SITE_URL}</loc><priority>1.0</priority></url>
    </urlset>"""
    st.text(sitemap)
    st.stop()

# ==========================================
# 2. إعدادات الصفحة والسيو (الـ Meta Tag الجديد)
# ==========================================
st.set_page_config(page_title="TechPulse AI | USA Tech Intelligence", page_icon="⚡", layout="wide")

st.markdown(f"""
    <head>
        <meta name="google-site-verification" content="Zx7FhZjS-T4dZqBjfiCy-ejzeh779QxVNByWsTRDmNc" />
        <meta name="description" content="AI-Powered Strategic Tech Market Intelligence.">
        <link rel="canonical" href="{SITE_URL}" />
    </head>
""", unsafe_allow_html=True)

# ==========================================
# 3. الستايل النيون (The UI Design)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 55px; font-weight: 900; color: #00CCFF; text-align: center; text-shadow: 0 0 25px #00CCFF; }
    .sentiment-box { background: #111111; padding: 25px; border-radius: 20px; border: 1px solid #333; text-align: center; margin-bottom: 30px; }
    .news-card { background: #111111; padding: 20px; border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 25px; }
    .share-btn {
        display: inline-flex; align-items: center; background: #1f2937; color: #00CCFF;
        padding: 5px 12px; border-radius: 8px; text-decoration: none; font-size: 11px; margin-right: 8px; border: 1px solid #00CCFF;
    }
    .ad-slot { text-align: center; margin: 20px 0; overflow: hidden; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. إعلان Adsterra
# ==========================================
st.markdown('<div class="ad-slot">', unsafe_allow_html=True)
components.html("""
    <div style="display: flex; justify-content: center;">
        <script type="text/javascript">
            atOptions = {'key' : '5f66cec17e51208142b62c4800c4705d','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};
        </script>
        <script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script>
    </div>
""", height=100)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. جلب الأخبار والذكاء الاصطناعي
# ==========================================
def fetch_tech_news():
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&country=us&apiKey={api_key}'
        res = requests.get(url).json()
        return res.get('articles', [])[:10]
    except: return []

def get_ai_insight(title, context):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Analyze: {title}. Context: {context}."}]
        )
        return res.choices[0].message.content
    except: return "AI Analysis offline."

articles = fetch_tech_news()

# ==========================================
# 6. الـ Sidebar
# ==========================================
with st.sidebar:
    st.markdown('<div style="background: linear-gradient(45deg, #00CCFF, #0055ff); padding: 15px; border-radius: 15px; text-align: center;"><h3>🔥 AI HOT PICKS</h3></div>', unsafe_allow_html=True)
    st.info("📈 **Trending:** AI Semiconductors")
    st.success("💎 **Watch:** NVIDIA (NVDA)")
    st.markdown("---")
    st.markdown("📢 **Sponsored**")
    components.html("""<div style='background:#111; height:100px; border:1px solid #333;'></div>""", height=120)

# ==========================================
# 7. المحتوى الرئيسي
# ==========================================
st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

if articles:
    all_titles = " ".join([a['title'] for a in articles])
    score = TextBlob(all_titles).sentiment.polarity
    st.markdown('<div class="sentiment-box">', unsafe_allow_html=True)
    mood = "🚀 BULLISH" if score > 0.05 else "⚠️ BEARISH" if score < -0.05 else "⚖️ NEUTRAL"
    color = "#00ff88" if score > 0.05 else "#ff4444" if score < -0.05 else "#00CCFF"
    st.markdown(f"<h2 style='color:{color};'>Market Mood: {mood}</h2>", unsafe_allow_html=True)
    st.progress(min(max((score + 1) / 2, 0.0), 1.0))
    st.markdown('</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'): st.image(art['urlToImage'], use_container_width=True)
            st.subheader(art['title'])
            
            share_text = urllib.parse.quote(f"News: {art['title']}")
            st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <a href="https://api.whatsapp.com/send?text={share_text}" target="_blank" class="share-btn">WhatsApp 🟢</a>
                    <a href="https://twitter.com/intent/tweet?text={share_text}" target="_blank" class="share-btn">Twitter 🔵</a>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🧠 AI VERDICT", key=f"btn_{i}"):
                with st.spinner('Analysing...'):
                    st.info(get_ai_insight(art['title'], art['description']))
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<center style='color:#444;'>© 2026 TechPulse Global | USA Tech Intelligence</center>", unsafe_allow_html=True)
