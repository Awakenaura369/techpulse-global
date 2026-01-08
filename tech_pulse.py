import streamlit as st
import requests
from groq import Groq
import tweepy
import streamlit.components.v1 as components

# --- 1. إعدادات الموقع الأساسية ---
SITE_URL = "https://techpulse-global.streamlit.app/"

# --- 2. التحقق من ملكية جوجل (Google Verification) ---
# هاد الجزء كيجاوب جوجل فاش كيقلب على ملف التحقق
if "google8c04de4f0fa47f61" in str(st.query_params):
    st.write("google-site-verification: google8c04de4f0fa47f61.html")
    st.stop()

# --- 3. ملفات الروبوت والسيت ماب (Robots.txt & Sitemap) ---
if "robots.txt" in str(st.query_params):
    st.text("User-agent: *\nDisallow: /_stcore/\nSitemap: " + SITE_URL + "sitemap.xml")
    st.stop()

if "sitemap.xml" in str(st.query_params):
    st.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE_URL}</loc></url></urlset>', unsafe_allow_html=True)
    st.stop()

# --- 4. دالة النشر في X (تويتر) مع ضمان الرابط ---
def post_to_x(title):
    try:
        client = tweepy.Client(
            consumer_key=st.secrets["X_API_KEY"],
            consumer_secret=st.secrets["X_API_SECRET"],
            access_token=st.secrets["X_ACCESS_TOKEN"],
            access_token_secret=st.secrets["X_ACCESS_SECRET"]
        )
        short_title = title[:160] + "..." if len(title) > 160 else title
        content = f"🚨 {short_title}\n\n🔗 Full Analysis: {SITE_URL}\n\n#AI #TechNews #MarketUpdate"
        client.create_tweet(text=content)
        return True
    except Exception as e:
        st.error(f"X API Error: {e}")
        return False

# --- 5. دالة التحليل بالذكاء الاصطناعي ---
def get_ai_analysis(title):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Analyze this tech news briefly for investors: {title}"}]
        )
        return completion.choices[0].message.content
    except:
        return "AI analysis is currently updating. Please check back in a moment."

# --- 6. واجهة المستخدم والستايل النيون ---
st.set_page_config(page_title="TechPulse AI | Global Tech Intelligence", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .title { color: #00CCFF; text-align: center; font-size: 45px; font-weight: 900; text-shadow: 0 0 15px #00CCFF; padding: 10px; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 25px; transition: 0.3s; }
    .card:hover { border-color: #00CCFF; box-shadow: 0 0 10px #00CCFF; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">TECH PULSE AI ⚡</div>', unsafe_allow_html=True)

# --- 7. جلب الأخبار وفحص الحالات ---
def get_news():
    try:
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&country=us&apiKey={st.secrets["NEWS_API_KEY"]}'
        res = requests.get(url).json()
        return res.get('articles', [])[:10]
    except:
        return []

articles = get_news()

# --- 8. نظام الأتمتة (Cron-job Trigger) ---
if "auto_post" in st.query_params and articles:
    post_to_x(articles[0]['title'])
    st.toast("Auto-post executed!")

# --- 9. عرض المحتوى والإعلانات ---
if not articles:
    st.warning("🔄 Fetching latest tech intelligence... Please refresh.")
else:
    # إعلان علوي (Adsterra Banner)
    components.html('<div style="text-align:center;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)

    for i, art in enumerate(articles):
        with st.container():
            st.markdown(f'<div class="card"><h3>{art["title"]}</h3><p style="color:#aaa;">{art.get("description", "")}</p></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    st.info(get_ai_analysis(art['title']))
            with c2:
                if st.button(f"🚀 SHARE ON X", key=f"x_{i}"):
                    if post_to_x(art['title']):
                        st.success("Shared with link!")

    # إعلان سفلي (Adsterra)
    components.html('<div style="text-align:center; margin-top:20px;"><script type="text/javascript">atOptions = {"key" : "5f66cec17e51208142b62c4800c4705d","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script></div>', height=100)
