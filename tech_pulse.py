import streamlit as st
import requests
from groq import Groq
import tweepy
import streamlit.components.v1 as components

# 1. تعريف رابط الموقع (ضروري باش يبان فالتويت)
SITE_URL = "https://techpulse-global.streamlit.app/"

# 2. دالة النشر (مع حل مشكل الرابط)
def post_to_x(title):
    try:
        client = tweepy.Client(
            consumer_key=st.secrets["X_API_KEY"],
            consumer_secret=st.secrets["X_API_SECRET"],
            access_token=st.secrets["X_ACCESS_TOKEN"],
            access_token_secret=st.secrets["X_ACCESS_SECRET"]
        )
        # تقصير العنوان لضمان مساحة للرابط (تجنب مشكل الاختفاء)
        short_title = (title[:180] + '..') if len(title) > 180 else title
        tweet_content = f"🚨 {short_title}\n\n🔗 Full Analysis: {SITE_URL}\n\n#TechNews #AI"
        
        client.create_tweet(text=tweet_content)
        return True
    except Exception as e:
        print(f"X Error: {e}")
        return False

# 3. إعدادات الصفحة والستايل
st.set_page_config(page_title="TechPulse AI", layout="wide", page_icon="⚡")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 45px; font-weight: 900; color: #00CCFF; text-align: center; }
    .news-card { background: #111111; padding: 20px; border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

# 4. جلب الأخبار
def fetch_news():
    try:
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&country=us&apiKey={st.secrets["NEWS_API_KEY"]}'
        return requests.get(url).json().get('articles', [])[:10]
    except: return []

articles = fetch_news()

# 5. الجزء الخاص بـ Cron-job (Automation)
# إذا دخل Cron-job للسيت مع هاد البراميتر، غادي يبوسطي أحدث خبر أوتوماتيكياً
if "auto_post" in st.query_params:
    if articles:
        latest_art = articles[0]
        success = post_to_x(latest_art['title'])
        if success:
            st.write("✅ Auto-posted latest news to X!")
        else:
            st.write("❌ Failed to auto-post.")

# 6. عرض الأخبار مع بوطون النشر اليدوي (للتأكد)
if articles:
    cols = st.columns(2)
    for i, art in enumerate(articles):
        with cols[i % 2]:
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'): st.image(art['urlToImage'])
            st.subheader(art['title'])
            
            # زر النشر اليدوي (جربو دابا باش تأكد من الرابط)
            if st.button(f"🚀 SHARE ON X", key=f"x_{i}"):
                if post_to_x(art['title']):
                    st.success("Posted with Link! Check your X profile.")
                else:
                    st.error("Error posting to X.")
            st.markdown('</div>', unsafe_allow_html=True)
