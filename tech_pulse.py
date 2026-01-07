import streamlit as st
import requests
from groq import Groq

# إعدادات الصفحة - ستايل نقي ومحترف
st.set_page_config(page_title="TechPulse AI | Global Tech Insights", page_icon="⚡", layout="wide")

# الستايل (Dark Mode & Professional Typography)
st.markdown("""
    <style>
    .reportview-container { background: #050505; }
    .main-title { font-size: 40px; font-weight: 800; color: #ffffff; text-align: center; margin-bottom: 10px; }
    .sub-title { font-size: 18px; color: #00CCFF; text-align: center; margin-bottom: 40px; letter-spacing: 2px; }
    .news-card { background: #111111; padding: 25px; border-radius: 10px; border-left: 5px solid #00CCFF; margin-bottom: 20px; }
    .insight-box { background: #0a192f; padding: 15px; border-radius: 5px; border: 1px dashed #00CCFF; color: #ccd6f6; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# العناوين الرئيسية
st.markdown('<div class="main-title">TECH PULSE AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">REAL-TIME GLOBAL TECH ANALYSIS</div>', unsafe_allow_html=True)

# دالة لجلب الأخبار من أمريكا (Tech Sector)
def fetch_tech_news():
    api_key = st.secrets["NEWS_API_KEY"]
    url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&country=us&apiKey={api_key}'
    response = requests.get(url)
    return response.json().get('articles', [])[:5] # كنجيبو آخر 5 أخبار دقيقة

# دالة لتحليل الخبر بواسطة Groq
def get_ai_insight(title, description):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    prompt = f"""
    Analyze the following tech news for a professional US audience:
    Title: {title}
    Context: {description}
    
    Provide a "Sigma Style" analysis:
    1. The Bottom Line (Why it matters in 1 sentence).
    2. Strategic Impact (On market or tech industry).
    Keep it cold, professional, and concise. No fluff.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# عرض الأخبار
articles = fetch_tech_news()

if articles:
    for art in articles:
        with st.container():
            st.markdown(f'<div class="news-card">', unsafe_allow_html=True)
            st.subheader(art['title'])
            st.write(f"Source: {art['source']['name']} | 📅 {art['publishedAt'][:10]}")
            
            # زر التحليل بالذكاء الاصطناعي
            if st.button(f"Analyze Insight", key=art['title']):
                with st.spinner('AI is analyzing...'):
                    insight = get_ai_insight(art['title'], art['description'])
                    st.markdown(f'<div class="insight-box"><b>⚡ AI STRATEGIC INSIGHT:</b><br>{insight}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Could not fetch news. Check your API Key.")

# Footer
st.markdown("---")
st.caption("Powered by Groq Llama 3 & NewsAPI. Target: Global Tech Market.")
