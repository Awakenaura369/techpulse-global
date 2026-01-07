import streamlit as st
import requests
from groq import Groq

# إعدادات ناضية
st.set_page_config(page_title="TechPulse AI", page_icon="⚡", layout="wide")

# CSS السحري: نيون، حواف مائلة، وتفاعل
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 55px; font-weight: 900; color: #00CCFF; text-align: center; text-shadow: 0 0 20px #00CCFF; margin-bottom: 0px; }
    .sub-title { font-size: 16px; color: #8892b0; text-align: center; margin-bottom: 40px; font-style: italic; }
    
    /* Card Design */
    .news-card {
        background: #111111; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #1f2937;
        transition: 0.3s;
        margin-bottom: 25px;
    }
    .news-card:hover { border-color: #00CCFF; box-shadow: 0 0 15px rgba(0,204,255,0.2); }
    
    /* Image Styling */
    .news-img { width: 100%; border-radius: 10px; object-fit: cover; height: 200px; margin-bottom: 15px; }
    
    /* AI Box */
    .insight-box {
        background: rgba(0, 204, 255, 0.05);
        border-left: 4px solid #00CCFF;
        padding: 15px;
        margin-top: 15px;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Intelligence-Driven Tech Briefings for Professionals</div>', unsafe_allow_html=True)

# دالة جلب الأخبار (معدلة لتشمل الصور)
def fetch_tech_news():
    api_key = st.secrets["NEWS_API_KEY"]
    url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&country=us&apiKey={api_key}'
    res = requests.get(url).json()
    return res.get('articles', [])[:6]

# دالة Groq
def get_ai_insight(title, context):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    prompt = f"Analyze like a Wall Street tech expert: Title: {title}. Context: {context}. Give: 1. Strategic Verdict (1 sentence). 2. Impact on Tech Industry."
    res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
    return res.choices[0].message.content

# عرض الأخبار على شكل Grid (جوج فـ السطر)
articles = fetch_tech_news()
if articles:
    cols = st.columns(2) # كيقسم الصفحة لـ جوج
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            
            # عرض الصورة إيلا كانت كاينة
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            
            st.subheader(art['title'])
            st.caption(f"📅 {art['publishedAt'][:10]} | Source: {art['source']['name']}")
            
            # زر التحليل بشكل عصري
            if st.button(f"🧠 AI ANALYSIS", key=f"btn_{i}"):
                with st.spinner('Thinking...'):
                    insight = get_ai_insight(art['title'], art['description'])
                    st.markdown(f'<div class="insight-box"><b>⚡ VERDICT:</b><br>{insight}</div>', unsafe_allow_html=True)
            
            st.markdown(f"[Read Original Article]({art['url']})")
            st.markdown('</div>', unsafe_allow_html=True)
