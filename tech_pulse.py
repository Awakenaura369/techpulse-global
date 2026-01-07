import streamlit as st
import requests
from groq import Groq
import streamlit.components.v1 as components
from textblob import TextBlob
import os
from datetime import datetime
import urllib.parse

# 1. صناعة ملفات التحقق والسيت ماب أوتوماتيكياً
def generate_static_files():
    with open("google8c04de4f0fa47f61.html", "w") as f:
        f.write("google-site-verification: google8c04de4f0fa47f61.html")
    
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://global.streamlit.app/</loc><priority>1.0</priority></url>
    </urlset>"""
    with open("sitemap.xml", "w") as f:
        f.write(sitemap_content)

generate_static_files()

# معالجة طلبات جوجل (الخريطة والتحقق)
if st.query_params.get("sitemap.xml"):
    with open("sitemap.xml", "r") as f: st.text(f.read())
    st.stop()
if "google8c04de4f0fa47f61" in str(st.query_params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html")
    st.stop()

# 2. إعدادات الصفحة والسيو
st.set_page_config(page_title="TechPulse AI | Market Intelligence", page_icon="⚡", layout="wide")

# 3. الستايل النيون + ستايل أزرار الشير (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 50px; font-weight: 900; color: #00CCFF; text-align: center; text-shadow: 0 0 20px #00CCFF; }
    .news-card { background: #111111; padding: 20px; border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 20px; }
    .share-btn {
        display: inline-flex; align-items: center; background: #1f2937; color: #00CCFF;
        padding: 5px 12px; border-radius: 8px; text-decoration: none; font-size: 13px; transition: 0.3s;
    }
    .share-btn:hover { background: #00CCFF; color: #000; }
    .ad-container { text-align: center; margin: 20px 0; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 4. مكان إعلان Adsterra العلوي (Banner 728x90 أو Native) - CPM عالي هنا
st.markdown('<div class="ad-container">', unsafe_allow_html=True)
st.markdown("", unsafe_allow_html=True)
components.html("""
    <div style="color:#444; font-size:12px; border:1px dashed #444; padding:10px;">Premium Partner Ad Space</div>
""", height=90)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

# 5. دوال جلب الأخبار والذكاء الاصطناعي
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
            messages=[{"role": "user", "content": f"Analyze: {title}. Verdict and impact?"}]
        )
        return res.choices[0].message.content
    except: return "AI Engine processing..."

articles = fetch_tech_news()

# 6. عداد مشاعر السوق
if articles:
    all_titles = " ".join([a['title'] for a in articles])
    score = TextBlob(all_titles).sentiment.polarity
    mood = "🚀 BULLISH" if score > 0.1 else "⚠️ BEARISH" if score < -0.1 else "⚖️ NEUTRAL"
    st.markdown(f"<h3 style='text-align:center;'>Market Sentiment: <span style='color:#00CCFF;'>{mood}</span></h3>", unsafe_allow_html=True)

# 7. عرض الأخبار + أزرار الشير
if articles:
    cols = st.columns(2)
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'): st.image(art['urlToImage'], use_container_width=True)
            st.subheader(art['title'])
            
            # بوتون الشير (WhatsApp & Twitter)
            share_text = urllib.parse.quote(f"Check this AI Analysis: {art['title']} - https://global.streamlit.app")
            whatsapp_url = f"https://api.whatsapp.com/send?text={share_text}"
            twitter_url = f"https://twitter.com/intent/tweet?text={share_text}"
            
            st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank" class="share-btn">🟢 Share on WhatsApp</a>
                <a href="{twitter_url}" target="_blank" class="share-btn">🔵 Tweet</a>
            """, unsafe_allow_html=True)
            
            if st.button(f"🧠 ANALYZE IMPACT", key=f"btn_{i}"):
                with st.spinner('AI Thinking...'):
                    insight = get_ai_insight(art['title'], art['description'])
                    st.info(insight)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # إعلان Adsterra وسط المقالات (Native Ad) - أحسن CPM
            if i == 1:
                 st.markdown('<div class="ad-container">', unsafe_allow_html=True)
                 components.html("""<div style='color:#333;'>Sponsored Content</div>""", height=250)
                 st.markdown('</div>', unsafe_allow_html=True)

# 8. Sidebar لإعلانات الـ Social Bar (Adsterra)
with st.sidebar:
    st.markdown("### 📊 Market Stats")
    st.write("Target: US Global")
    st.markdown("---")
    # مكان إعلان Social Bar (Adsterra) - كيجيب نقرات خيالية
    st.markdown("📢 **Recommended for you**")
    components.html("""<div style='background:#111; height:100px;'></div>""", height=120)

st.markdown("<center>© 2026 TechPulse Intelligence</center>", unsafe_allow_html=True)
