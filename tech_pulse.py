import streamlit as st
import requests
from groq import Groq
import streamlit.components.v1 as components
from textblob import TextBlob
import os

# 1. خدعة جوجل: صناعة ملف التحقق أوتوماتيكياً (لأنك خدام بالتلفون)
# هاد الكود غيصاوب الملف فـ السيرفر نيشان
google_filename = "google8c04de4f0fa47f61.html"
with open(google_filename, "w") as f:
    f.write("google-site-verification: google8c04de4f0fa47f61.html")

# 2. إعدادات الصفحة والسيو
st.set_page_config(page_title="TechPulse AI | Market Intelligence", page_icon="⚡", layout="wide")

# زراعة الـ Meta Tag للتحقق الاحتياطي
st.markdown(f"""
    <head>
        <meta name="google-site-verification" content="google8c04de4f0fa47f61" />
        <meta name="description" content="AI-Powered Strategic Tech Insights for Global Markets.">
    </head>
""", unsafe_allow_html=True)

# 3. الستايل النيون الاحترافي
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 55px; font-weight: 900; color: #00CCFF; text-align: center; text-shadow: 0 0 20px #00CCFF; }
    .sentiment-meter { background: #111111; padding: 20px; border-radius: 20px; border: 1px solid #333; text-align: center; margin-bottom: 30px; }
    .news-card { background: #111111; padding: 20px; border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 20px; transition: 0.3s; }
    .news-card:hover { border-color: #00CCFF; transform: translateY(-5px); }
    .insight-box { background: rgba(0, 204, 255, 0.08); border-left: 5px solid #00CCFF; padding: 15px; margin-top: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- البداية ---
st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#8892b0;">USA TECH MARKET SENTIMENT & STRATEGIC ANALYSIS</p>', unsafe_allow_html=True)

# دالة جلب الأخبار
def fetch_tech_news():
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&country=us&apiKey={api_key}'
        res = requests.get(url).json()
        return res.get('articles', [])[:10]
    except: return []

# دالة Groq
def get_ai_insight(title, context):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Analyze as a Silicon Valley Consultant: {title}. Context: {context}. Give a Verdict."}]
        )
        return res.choices[0].message.content
    except: return "AI Engine is busy. Try again."

articles = fetch_tech_news()

# 4. تحليل مشاعر السوق
if articles:
    all_titles = " ".join([a['title'] for a in articles])
    sentiment_score = TextBlob(all_titles).sentiment.polarity
    
    st.markdown('<div class="sentiment-meter">', unsafe_allow_html=True)
    if sentiment_score > 0.1:
        st.markdown("<h3>Market Sentiment: <span style='color:#00ff88;'>🚀 BULLISH</span></h3>", unsafe_allow_html=True)
    elif sentiment_score < -0.1:
        st.markdown("<h3>Market Sentiment: <span style='color:#ff4444;'>⚠️ BEARISH</span></h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3>Market Sentiment: <span style='color:#00CCFF;'>⚖️ NEUTRAL</span></h3>", unsafe_allow_html=True)
    st.progress(min(max((sentiment_score + 1) / 2, 0.0), 1.0))
    st.markdown('</div>', unsafe_allow_html=True)

# 5. عرض الأخبار
if articles:
    cols = st.columns(2)
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            st.subheader(art['title'])
            
            if st.button(f"🧠 ANALYZE IMPACT", key=f"btn_{i}"):
                with st.spinner('Calculating...'):
                    insight = get_ai_insight(art['title'], art['description'])
                    st.markdown(f'<div class="insight-box"><b>⚡ STRATEGIC VERDICT:</b><br>{insight}</div>', unsafe_allow_html=True)
            
            st.markdown(f"[Source]({art['url']})")
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<center>© 2026 TechPulse Global | AI Intelligence Standard</center>", unsafe_allow_html=True)
