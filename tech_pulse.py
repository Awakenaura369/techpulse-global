import streamlit as st
import requests
from groq import Groq
import streamlit.components.v1 as components

# 1. إعدادات الصفحة والسيو (SEO & Page Setup)
st.set_page_config(
    page_title="TechPulse AI | Global Tech Intelligence",
    page_icon="⚡",
    layout="wide"
)

# إضافة Meta Tags وكود التحقق ديال Google Search Console
st.markdown("""
    <head>
        <meta name="google-site-verification" content="Zx7FhZjS-T4dZqBjfiCy-ejzeh779QxVNByWsTRDmNc" />
        
        <meta name="description" content="AI-driven strategic tech analysis for global markets. Get the latest insights on AI, hardware, and software trends from Silicon Valley.">
        <meta name="keywords" content="AI News, Technology Analysis, US Tech, TechPulse, Groq AI, Llama 3 Analysis">
        <meta name="author" content="TechPulse AI">
    </head>
""", unsafe_allow_html=True)

# 2. الستايل النيون (Neon & Modern UI)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { 
        font-size: 55px; font-weight: 900; color: #00CCFF; 
        text-align: center; text-shadow: 0 0 20px #00CCFF; margin-bottom: 5px; 
    }
    .sub-title { font-size: 18px; color: #8892b0; text-align: center; margin-bottom: 40px; font-style: italic; }
    .news-card {
        background: #111111; padding: 25px; border-radius: 15px; 
        border: 1px solid #1f2937; margin-bottom: 25px; transition: 0.4s ease;
    }
    .news-card:hover { border-color: #00CCFF; box-shadow: 0 0 20px rgba(0,204,255,0.15); transform: translateY(-5px); }
    .insight-box {
        background: rgba(0, 204, 255, 0.07); border-left: 5px solid #00CCFF;
        padding: 15px; margin-top: 15px; font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        width: 100%; background-color: transparent; border: 1px solid #00CCFF; color: #00CCFF;
        border-radius: 8px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #00CCFF; color: black; }
    </style>
""", unsafe_allow_html=True)

# --- الجنب (Sidebar) للأخبار وللإعلانات مستقبلاً ---
with st.sidebar:
    st.markdown("<h2 style='color:#00CCFF;'>🚀 Ad Space</h2>", unsafe_allow_html=True)
    # هاد البلاصة هي فين غاتحط كود Adsterra فاش تجيبو
    components.html("""
        <div style="border: 1px dashed #444; color: #666; height: 250px; display: flex; align-items: center; justify-content: center;">
            Adsterra Banner Here
        </div>
    """, height=260)
    st.markdown("---")
    st.markdown("### 🌐 Market: USA / Global")
    st.info("AI Analysis is powered by Llama-3.3-70B via Groq.")

# --- الواجهة الرئيسية ---
st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">PREMIUM STRATEGIC INTELLIGENCE FOR THE TECH ELITE</div>', unsafe_allow_html=True)

# دالة جلب الأخبار
def fetch_tech_news():
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&country=us&apiKey={api_key}'
        res = requests.get(url).json()
        return res.get('articles', [])[:10] # غايجبد 10 ديال الأخبار
    except Exception as e:
        st.error("Error fetching news.")
        return []

# دالة Groq
def get_ai_insight(title, context):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        prompt = f"Analyze as a Silicon Valley Strategic Consultant: Title: {title}. Context: {context}. Give a Verdict and Future Market Impact."
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
        return res.choices[0].message.content
    except:
        return "Intelligence system is currently calibrating. Please try again."

# عرض المحتوى
articles = fetch_tech_news()

if articles:
    cols = st.columns(2)
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            
            st.subheader(art['title'])
            st.caption(f"📅 {art['publishedAt'][:10]} | Source: {art['source']['name']}")
            
            if st.button(f"🧠 ANALYZE INSIGHT", key=f"btn_{i}"):
                with st.spinner('AI is processing market impact...'):
                    insight = get_ai_insight(art['title'], art['description'])
                    st.markdown(f'<div class="insight-box"><b>⚡ STRATEGIC VERDICT:</b><br>{insight}</div>', unsafe_allow_html=True)
            
            st.markdown(f"[View Original Source]({art['url']})")
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #444;'>© 2026 TechPulse Global | AI-Powered Market Analytics</p>", unsafe_allow_html=True)
