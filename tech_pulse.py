import streamlit as st
import requests
from groq import Groq
import streamlit.components.v1 as components
from textblob import TextBlob
import os

# ==========================================
# 1. حل مشكلة جوجل (الضربة القاضية)
# ==========================================
# هاد الكود كيخلي جوجل يلقى كود التحقق كيفما بغا
if st.query_params.get("google") or "google8c04de4f0fa47f61" in str(st.query_params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html")
    st.stop()

# صناعة الملف فالسيرفر للاحتياط
with open("google8c04de4f0fa47f61.html", "w") as f:
    f.write("google-site-verification: google8c04de4f0fa47f61.html")

# ==========================================
# 2. إعدادات الصفحة والسيو (SEO)
# ==========================================
st.set_page_config(
    page_title="TechPulse AI | Strategic Tech Intelligence",
    page_icon="⚡",
    layout="wide"
)

# إضافة Meta Tags لـ Google Search Console
st.markdown("""
    <head>
        <meta name="google-site-verification" content="google8c04de4f0fa47f61" />
        <meta name="description" content="AI-driven strategic analysis of global tech markets. Silicon Valley insights delivered in real-time.">
        <meta name="keywords" content="AI, Technology, Market Analysis, Groq, Tech News USA">
    </head>
""", unsafe_allow_html=True)

# ==========================================
# 3. الستايل النيون (The UI Design)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { 
        font-size: clamp(30px, 8vw, 60px); font-weight: 900; color: #00CCFF; 
        text-align: center; text-shadow: 0 0 25px #00CCFF; margin-bottom: 0px; 
    }
    .sentiment-meter { 
        background: #111111; padding: 20px; border-radius: 20px; 
        border: 1px solid #333; text-align: center; margin: 20px 0;
    }
    .news-card {
        background: #111111; padding: 25px; border-radius: 15px; 
        border: 1px solid #1f2937; margin-bottom: 25px; transition: 0.4s ease;
    }
    .news-card:hover { border-color: #00CCFF; box-shadow: 0 0 20px rgba(0,204,255,0.15); transform: translateY(-5px); }
    .insight-box {
        background: rgba(0, 204, 255, 0.07); border-left: 5px solid #00CCFF;
        padding: 15px; margin-top: 15px; border-radius: 0 10px 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. منطق البيانات (Logic)
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
        prompt = f"Analyze as a Silicon Valley Senior Consultant: Title: {title}. Context: {context}. Give a Strategic Verdict."
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
        return res.choices[0].message.content
    except: return "Intelligence engine calibrating..."

# ==========================================
# 5. عرض الواجهة (UI Layout)
# ==========================================
st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#8892b0; font-style:italic;">GLOBAL STRATEGIC INTELLIGENCE UNIT</p>', unsafe_allow_html=True)

articles = fetch_tech_news()

# عداد مشاعر السوق
if articles:
    all_titles = " ".join([a['title'] for a in articles])
    sentiment_score = TextBlob(all_titles).sentiment.polarity
    
    st.markdown('<div class="sentiment-meter">', unsafe_allow_html=True)
    if sentiment_score > 0.1:
        st.markdown("<h3>Market Mood: <span style='color:#00ff88;'>🚀 BULLISH</span></h3>", unsafe_allow_html=True)
    elif sentiment_score < -0.1:
        st.markdown("<h3>Market Mood: <span style='color:#ff4444;'>⚠️ BEARISH</span></h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3>Market Mood: <span style='color:#00CCFF;'>⚖️ NEUTRAL</span></h3>", unsafe_allow_html=True)
    st.progress(min(max((sentiment_score + 1) / 2, 0.0), 1.0))
    st.markdown('</div>', unsafe_allow_html=True)

# عرض الأخبار
if articles:
    cols = st.columns(2)
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            
            st.subheader(art['title'])
            st.caption(f"Source: {art['source']['name']} | 🇺🇸 USA Market")
            
            if st.button(f"🧠 ANALYZE IMPACT", key=f"btn_{i}"):
                with st.spinner('AI analyzing market trends...'):
                    insight = get_ai_insight(art['title'], art['description'])
                    st.markdown(f'<div class="insight-box"><b>⚡ VERDICT:</b><br>{insight}</div>', unsafe_allow_html=True)
            
            st.markdown(f"[Unlock Source Intelligence]({art['url']})")
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<center>© 2026 TechPulse Global Intelligence</center>", unsafe_allow_html=True)
