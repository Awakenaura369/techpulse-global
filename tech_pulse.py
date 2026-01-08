import streamlit as st
import requests
from groq import Groq
import tweepy
import streamlit.components.v1 as components

# 1. إعدادات الموقع
SITE_URL = "https://techpulse-global.streamlit.app/"

# 2. دالة النشر في X
def post_to_x(title):
    try:
        client = tweepy.Client(
            consumer_key=st.secrets["X_API_KEY"],
            consumer_secret=st.secrets["X_API_SECRET"],
            access_token=st.secrets["X_ACCESS_TOKEN"],
            access_token_secret=st.secrets["X_ACCESS_SECRET"]
        )
        # ضمان وجود الرابط وتقصير العنوان
        short_title = title[:160] + "..." if len(title) > 160 else title
        content = f"🚨 {short_title}\n\n🔗 Full Analysis: {SITE_URL}\n\n#AI #TechNews"
        client.create_tweet(text=content)
        return True
    except Exception as e:
        st.error(f"X API Error: {e}")
        return False

# 3. دالة التحليل بالذكاء الاصطناعي
def get_ai_analysis(title):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Analyze this tech news briefly for investors: {title}"}]
        )
        return completion.choices[0].message.content
    except:
        return "Analysis currently unavailable."

# 4. واجهة المستخدم (UI)
st.set_page_config(page_title="TechPulse AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .title { color: #00CCFF; text-align: center; font-size: 40px; font-weight: bold; }
    .card { background: #111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

# 5. جلب الأخبار
url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&country=us&apiKey={st.secrets["NEWS_API_KEY"]}'
articles = requests.get(url).json().get('articles', [])[:10]

# 6. نظام الأوتوماتيك لـ Cron-job
if "auto_post" in st.query_params and articles:
    post_to_x(articles[0]['title'])
    st.write("🤖 Auto-post triggered!")

# 7. عرض الأخبار
if articles:
    for i, art in enumerate(articles):
        with st.container():
            st.markdown(f'<div class="card"><h3>{art["title"]}</h3></div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    st.info(get_ai_analysis(art['title']))
            with col2:
                if st.button(f"🚀 SHARE ON X", key=f"x_{i}"):
                    if post_to_x(art['title']):
                        st.success("Shared with Link!")
