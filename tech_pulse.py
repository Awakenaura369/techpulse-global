import streamlit as st
import requests
from groq import Groq
from supabase import create_client, Client
import datetime
import urllib.parse
from textblob import TextBlob
import streamlit.components.v1 as components

# ======================
# 1️⃣ Supabase Setup
# ======================
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# ======================
# 2️⃣ Site Config & SEO
# ======================
SITE_URL = "https://techpulse-global.streamlit.app/"
PREVIEW_IMG = "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80"

st.set_page_config(page_title="TechPulse AI 3.0 ⚡", layout="wide", page_icon="🤖")

# ======================
# 3️⃣ UI Styles + Flashy Animations
# ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Orbitron:wght@900&display=swap');
.stApp { background-color: #010409; color: #E6EDF3; font-family: 'Inter', sans-serif; }
.main-header { font-family: 'Orbitron', sans-serif; text-align: center; padding: 20px; }
.main-header h1 { color: #58A6FF; font-size: 48px; margin-bottom: 0; transition: 0.4s; }
.main-header h1:hover { color: #FFDD00; transform: scale(1.08) rotate(-2deg); text-shadow: 0 0 20px #FFDD00; }
.news-card { background: #0D1117; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 25px; overflow: hidden; transition: 0.3s; }
.news-card:hover { transform: translateY(-7px); box-shadow: 0 0 20px #58A6FF; }
.news-title { font-size: 22px; font-weight: bold; color: #F0F6FC; margin-bottom: 10px; transition: 0.3s; }
.news-title:hover { color: #FFDD00; }
.stButton>button { background: linear-gradient(90deg, #1F6FEB, #00CCFF) !important; color: white !important; border-radius: 12px !important; border: none !important; width: 100% !important; font-weight: 700; transition: 0.3s; animation: glow 2s infinite; }
.stButton>button:hover { background: linear-gradient(90deg, #FFDD00, #FFAA00) !important; color: black !important; transform: scale(1.05) rotate(-1deg); }
@keyframes glow {
  0% { box-shadow: 0 0 5px #00CCFF; }
  50% { box-shadow: 0 0 20px #58A6FF; }
  100% { box-shadow: 0 0 5px #00CCFF; }
}
.footer { text-align: center; padding: 40px; color: #8B949E; font-size: 13px; border-top: 1px solid #30363D; margin-top: 50px; }
.footer a { color: #58A6FF; text-decoration: none; margin: 0 10px; }
</style>
""", unsafe_allow_html=True)

# ======================
# 4️⃣ Admin Dashboard (Sidebar)
# ======================
st.sidebar.title("📊 Admin Dashboard")

def get_api_calls_today():
    today = datetime.date.today().isoformat()
    res = supabase.table("ai_usage_log").select("*").eq("date", today).execute()
    if res.data:
        return res.data[0]['calls_count']
    return 0

def increment_api_call():
    today = datetime.date.today().isoformat()
    res = supabase.table("ai_usage_log").select("*").eq("date", today).execute()
    if res.data:
        supabase.table("ai_usage_log").update({"calls_count": res.data[0]['calls_count']+1}).eq("date", today).execute()
    else:
        supabase.table("ai_usage_log").insert({"date": today, "calls_count": 1}).execute()

calls_today = get_api_calls_today()
st.sidebar.metric("AI Calls Today", calls_today, delta=5-calls_today)

top_articles = supabase.table("ai_analysis").select("*").order("timestamp", desc=True).limit(5).execute()
st.sidebar.subheader("Last 5 AI Analyses")
for a in top_articles.data:
    st.sidebar.write(f"- {a['article_id']}: {a['analysis'][:50]}...")

# ======================
# 5️⃣ Fetch News
# ======================
@st.cache_data(ttl=3600)
def fetch_news():
    try:
        api_key = st.secrets["NEWS_API_KEY"].strip()
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={api_key}'
        r = requests.get(url).json()
        return r.get('articles', [])
    except:
        return []

# ======================
# 6️⃣ AI Analysis Function
# ======================
def ai_analyze(article_id, title):
    res = supabase.table("ai_analysis").select("*").eq("article_id", article_id).execute()
    if res.data:
        return res.data[0]['analysis']
    
    if get_api_calls_today() >= 5:
        return "⚠️ Daily AI limit reached. Come back tomorrow or check previous analyses."
    
    client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Quick analysis for investors: {title}"}]
    )
    result = chat.choices[0].message.content
    
    sentiment = TextBlob(title).sentiment.polarity
    sentiment_tag = "📈 Positive" if sentiment > 0 else ("📉 Negative" if sentiment < 0 else "⚖️ Neutral")
    result = f"{result}\n\nSentiment: {sentiment_tag}"
    
    supabase.table("ai_analysis").insert({
        "article_id": article_id,
        "analysis": result,
        "timestamp": datetime.datetime.now().isoformat()
    }).execute()
    
    increment_api_call()
    return result

# ======================
# 7️⃣ Display News
# ======================
st.markdown('<div class="main-header"><h1>TECH PULSE AI ⚡ 3.0</h1><p>Global Intelligence - Ultimate Flashy Edition</p></div>', unsafe_allow_html=True)

articles = fetch_news()
if articles:
    for i, art in enumerate(articles):
        article_id = f"article_{i}"
        with st.container():
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            if art.get('urlToImage'):
                st.image(art['urlToImage'], use_container_width=True)
            st.markdown(f"<div class='news-title'>{art['title']}</div>", unsafe_allow_html=True)
            st.write(f"🌐 {art['source']['name']} | 📅 {art.get('publishedAt', '2026-01-08')[:10]}")
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    analysis = ai_analyze(article_id, art['title'])
                    st.info(analysis)
            with c2:
                t_text = f"⚡ INTEL: {art['title']}\n\n🔗 Report: {SITE_URL}"
                t_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(t_text)}"
                st.markdown(f'<a href="{t_url}" target="_blank"><div style="background-color:#1F6FEB; color:white; padding:10px; border-radius:6px; text-align:center; font-weight:600;">🚀 SHARE ON X</div></a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 8️⃣ Footer
# ======================
st.markdown(f"""
<div class="footer">
    <p>© 2026 <b>TechPulse Global AI</b>. All rights reserved.</p>
    <p>
        <a href="?page=privacy" target="_self">Privacy Policy</a> | 
        <a href="?page=terms" target="_self">Terms of Service</a> | 
        <a href="mailto:contact@techpulse-global.com">Contact Support</a>
    </p>
</div>
""", unsafe_allow_html=True)
