import streamlit as st
import requests
from groq import Groq
import streamlit.components.v1 as components
from textblob import TextBlob # مكتبة تحليل المشاعر

# 1. إعدادات السيو والصفحة
st.set_page_config(page_title="TechPulse AI | Global Market Intel", page_icon="⚡", layout="wide")

# كود التحقق من جوجل (مخفي)
components.html("""<div style="display:none;"><meta name="google-site-verification" content="Zx7FhZjS-T4dZqBjfiCy-ejzeh779QxVNByWsTRDmNc" /></div>""", height=0)

# 2. الستايل النيون المتطور
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 60px; font-weight: 900; color: #00CCFF; text-align: center; text-shadow: 0 0 25px #00CCFF; }
    .sentiment-meter { background: #111111; padding: 20px; border-radius: 20px; border: 1px solid #333; text-align: center; margin-bottom: 30px; }
    .news-card { background: #111111; padding: 25px; border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 25px; transition: 0.4s; }
    .news-card:hover { border-color: #00CCFF; box-shadow: 0 0 20px rgba(0,204,255,0.2); transform: translateY(-5px); }
    .badge { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .positive { background-color: #00ff8822; color: #00ff88; border: 1px solid #00ff88; }
    .negative { background-color: #ff444422; color: #ff4444; border: 1px solid #ff4444; }
    </style>
""", unsafe_allow_html=True)

# 3. دوال الذكاء الاصطناعي والبيانات
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
            messages=[{"role": "user", "content": f"Analyze as a Wall Street Expert: {title}. Context: {context}. Give a sharp Strategic Verdict."}]
        )
        return res.choices[0].message.content
    except: return "AI processing error."

# --- البداية ---
st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#8892b0;">ADVANCED BI-DIRECTIONAL TECH INTELLIGENCE</p>', unsafe_allow_html=True)

articles = fetch_tech_news()

# 4. عداد مشاعر السوق (Market Sentiment Meter)
if articles:
    all_titles = " ".join([a['title'] for a in articles])
    sentiment_score = TextBlob(all_titles).sentiment.polarity
    
    st.markdown('<div class="sentiment-meter">', unsafe_allow_html=True)
    if sentiment_score > 0.1:
        st.markdown("<h3>Market Mood: <span style='color:#00ff88;'>🚀 BULLISH (Positive)</span></h3>", unsafe_allow_html=True)
    elif sentiment_score < -0.1:
        st.markdown("<h3>Market Mood: <span style='color:#ff4444;'>⚠️ BEARISH (Caution)</span></h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3>Market Mood: <span style='color:#00CCFF;'>⚖️ NEUTRAL</span></h3>", unsafe_allow_html=True)
    st.progress(min(max((sentiment_score + 1) / 2, 0.0), 1.0))
    st.markdown('</div>', unsafe_allow_html=True)

# 5. عرض الأخبار في Columns
if articles:
    cols = st.columns(2)
    for i, art in enumerate(articles):
        # تحليل مشاعر الخبر المنفرد
        single_sentiment = TextBlob(art['title']).sentiment.polarity
        sentiment_class = "positive" if single_sentiment >= 0 else "negative"
        sentiment_label = "PROFITABLE TREND" if single_sentiment >= 0 else "RISK ALERT"

        with cols[i % 2]:
            st.markdown(f'''<div class="news-card">
                <span class="badge {sentiment_class}">{sentiment_label}</span>
                <br><br>''', unsafe_allow_html=True)
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            st.subheader(art['title'])
            
            if st.button(f"🧠 AI ANALYSIS", key=f"btn_{i}"):
                with st.spinner('Analyzing...'):
                    insight = get_ai_insight(art['title'], art['description'])
                    st.info(insight)
            
            st.markdown(f"[Unlock Full Intelligence]({art['url']})")
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<center>© 2026 TechPulse Global | Silicon Valley Standard AI</center>", unsafe_allow_html=True)
