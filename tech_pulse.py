import streamlit as st
import requests
from groq import Groq
import streamlit.components.v1 as components
from textblob import TextBlob
import os
from datetime import datetime
import urllib.parse

# 1. نظام التحقق والسيت ماب أوتوماتيكياً
def generate_static_files():
    with open("google8c04de4f0fa47f61.html", "w") as f:
        f.write("google-site-verification: google8c04de4f0fa47f61.html")
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://global.streamlit.app/</loc><priority>1.0</priority></url>
    </urlset>"""
    with open("sitemap.xml", "w") as f: f.write(sitemap)

generate_static_files()

# معالجة طلبات جوجل (للسيو)
if st.query_params.get("sitemap.xml"):
    with open("sitemap.xml", "r") as f: st.text(f.read()); st.stop()
if "google8c04de4f0fa47f61" in str(st.query_params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html"); st.stop()

# 2. إعدادات الصفحة
st.set_page_config(page_title="TechPulse AI | Market Intelligence", page_icon="⚡", layout="wide")

# 3. الستايل النيون المتطور
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 55px; font-weight: 900; color: #00CCFF; text-align: center; text-shadow: 0 0 25px #00CCFF; margin-bottom: 5px; }
    .sentiment-box { 
        background: #111111; padding: 25px; border-radius: 20px; 
        border: 1px solid #333; text-align: center; margin-bottom: 30px;
    }
    .news-card { background: #111111; padding: 20px; border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 25px; transition: 0.3s; }
    .news-card:hover { border-color: #00CCFF; transform: translateY(-5px); }
    .share-btn {
        display: inline-flex; align-items: center; background: #1f2937; color: #00CCFF;
        padding: 5px 12px; border-radius: 8px; text-decoration: none; font-size: 12px; margin-right: 8px; border: 1px solid #00CCFF;
    }
    .ad-slot { text-align: center; margin: 20px 0; overflow: hidden; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 4. الإعلان العلوي (Adsterra 728x90)
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

st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

# 5. دوال جلب البيانات والذكاء الاصطناعي
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
            messages=[{"role": "user", "content": f"Briefly analyze as Wall Street expert: {title}. Context: {context}."}]
        )
        return res.choices[0].message.content
    except: return "Analysis temporarily offline."

articles = fetch_tech_news()

# 6. عداد المشاعر (برجوع البار الزرقاء)
if articles:
    all_titles = " ".join([a['title'] for a in articles])
    score = TextBlob(all_titles).sentiment.polarity
    
    st.markdown('<div class="sentiment-box">', unsafe_allow_html=True)
    mood = "🚀 BULLISH (Positive)" if score > 0.05 else "⚠️ BEARISH (Caution)" if score < -0.05 else "⚖️ NEUTRAL"
    color = "#00ff88" if score > 0.05 else "#ff4444" if score < -0.05 else "#00CCFF"
    st.markdown(f"<h2 style='color:{color}; margin-bottom:15px;'>Market Mood: {mood}</h2>", unsafe_allow_html=True)
    st.progress(min(max((score + 1) / 2, 0.0), 1.0)) # هادي هي البار الزرقاء اللي طلبتي
    st.markdown('</div>', unsafe_allow_html=True)

# 7. عرض الأخبار مع أزرار الشير والإعلانات
if articles:
    cols = st.columns(2)
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'): st.image(art['urlToImage'], use_container_width=True)
            st.subheader(art['title'])
            
            # أزرار الشير الاحترافية
            share_text = urllib.parse.quote(f"Check out this AI Analysis: {art['title']}")
            st.markdown(f"""
                <div style="margin-bottom:15px;">
                    <a href="https://api.whatsapp.com/send?text={share_text}" target="_blank" class="share-btn">WhatsApp 🟢</a>
                    <a href="https://twitter.com/intent/tweet?text={share_text}" target="_blank" class="share-btn">Twitter 🔵</a>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🧠 AI VERDICT", key=f"btn_{i}"):
                with st.spinner('Analyzing market data...'):
                    st.info(get_ai_insight(art['title'], art['description']))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # إعلان Adsterra إضافي لرفع CPM (بعد الخبر الثاني)
            if i == 1:
                st.markdown('<div class="ad-slot">', unsafe_allow_html=True)
                components.html('<script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script>', height=100)
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='color:#444; margin-top:50px;'>© 2026 TechPulse Global | USA Intelligence Unit</center>", unsafe_allow_html=True)
