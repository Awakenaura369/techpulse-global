import streamlit as st
import requests
from groq import Groq
import streamlit.components.v1 as components
from textblob import TextBlob
import os
from datetime import datetime
import urllib.parse

# 1. صناعة ملفات التحقق والسيت ماب (للسيو وجوجل)
def generate_static_files():
    with open("google8c04de4f0fa47f61.html", "w") as f:
        f.write("google-site-verification: google8c04de4f0fa47f61.html")
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://global.streamlit.app/</loc><priority>1.0</priority></url>
    </urlset>"""
    with open("sitemap.xml", "w") as f: f.write(sitemap)

generate_static_files()

# معالجة طلبات جوجل
if st.query_params.get("sitemap.xml"):
    with open("sitemap.xml", "r") as f: st.text(f.read()); st.stop()
if "google8c04de4f0fa47f61" in str(st.query_params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html"); st.stop()

# 2. إعدادات الصفحة
st.set_page_config(page_title="TechPulse AI | Market Intelligence", page_icon="⚡", layout="wide")

# 3. الستايل النيون وأزرار الشير
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 50px; font-weight: 900; color: #00CCFF; text-align: center; text-shadow: 0 0 20px #00CCFF; }
    .news-card { background: #111111; padding: 20px; border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 20px; }
    .share-btn {
        display: inline-flex; align-items: center; background: #1f2937; color: #00CCFF;
        padding: 6px 15px; border-radius: 8px; text-decoration: none; font-size: 13px; margin-right: 10px; transition: 0.3s;
    }
    .share-btn:hover { background: #00CCFF; color: #000; }
    .ad-slot { text-align: center; margin: 20px 0; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# 4. إعلان Adsterra العلوي (Header)
st.markdown('<div class="ad-slot">', unsafe_allow_html=True)
components.html("""
    <div style="display: flex; justify-content: center;">
        <script type="text/javascript">
            atOptions = {
                'key' : '5f66cec17e51208142b62c4800c4705d',
                'format' : 'iframe',
                'height' : 90,
                'width' : 728,
                'params' : {}
            };
        </script>
        <script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script>
    </div>
""", height=100)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

# 5. دوال جلب البيانات
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
            messages=[{"role": "user", "content": f"Analyze: {title}. Impact on US tech market?"}]
        )
        return res.choices[0].message.content
    except: return "AI Insight unavailable."

articles = fetch_tech_news()

# 6. عداد المشاعر (Sentiment)
if articles:
    all_titles = " ".join([a['title'] for a in articles])
    score = TextBlob(all_titles).sentiment.polarity
    mood = "🚀 BULLISH" if score > 0.1 else "⚠️ BEARISH" if score < -0.1 else "⚖️ NEUTRAL"
    st.markdown(f"<h3 style='text-align:center;'>Sentiment Score: {mood}</h3>", unsafe_allow_html=True)

# 7. عرض الأخبار
if articles:
    cols = st.columns(2)
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'): st.image(art['urlToImage'], use_container_width=True)
            st.subheader(art['title'])
            
            # أزرار الشير
            share_text = urllib.parse.quote(f"Breaking News: {art['title']} via TechPulse AI")
            st.markdown(f"""
                <a href="https://api.whatsapp.com/send?text={share_text}" target="_blank" class="share-btn">WhatsApp</a>
                <a href="https://twitter.com/intent/tweet?text={share_text}" target="_blank" class="share-btn">Twitter</a>
            """, unsafe_allow_html=True)
            
            if st.button(f"🧠 AI ANALYSIS", key=f"btn_{i}"):
                with st.spinner('AI analyzing...'):
                    st.info(get_ai_insight(art['title'], art['description']))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # تكرار الإعلان تحت الخبر الثالث (اختياري لرفع الأرباح)
            if i == 2:
                st.markdown('<div class="ad-slot">', unsafe_allow_html=True)
                components.html('<script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script>', height=100)
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center>© 2026 TechPulse Global</center>", unsafe_allow_html=True)
