import streamlit as st
import requests
from groq import Groq
from textblob import TextBlob
import urllib.parse
import streamlit.components.v1 as components

# ======================
# 1️⃣ Site Config & SEO
# ======================
SITE_URL = "https://techpulse-global.streamlit.app/"
PREVIEW_IMG = "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80"

st.set_page_config(page_title="TechPulse AI 3.2 ⚡ Offline", layout="wide", page_icon="🤖")

# ======================
# 2️⃣ Flashy UI CSS
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
@keyframes glow { 0% { box-shadow: 0 0 5px #00CCFF; } 50% { box-shadow: 0 0 20px #58A6FF; } 100% { box-shadow: 0 0 5px #00CCFF; } }
.footer { text-align: center; padding: 40px; color: #8B949E; font-size: 13px; border-top: 1px solid #30363D; margin-top: 50px; }
.footer a { color: #58A6FF; text-decoration: none; margin: 0 10px; }
.market-mood { background: #0D1117; border-radius: 12px; padding: 12px; margin-bottom: 15px; font-weight:bold; text-align:center; }
</style>
""", unsafe_allow_html=True)

# ======================
# 3️⃣ Session State Initialization
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_calls" not in st.session_state:
    st.session_state.api_calls = 0
if "ai_cache" not in st.session_state:
    st.session_state.ai_cache = {}

DAILY_LIMIT = 5

# ======================
# 4️⃣ Adsterra Top
# ======================
components.html('''
<div style="text-align:center;">
<script type="text/javascript">
atOptions = {
    "key" : "5f66cec17e51208142b62c4800c4705d",
    "format" : "iframe",
    "height" : 90,
    "width" : 728,
    "params" : {}
};
</script>
<script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script>
</div>
''', height=100)

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
    if article_id in st.session_state.ai_cache:
        return st.session_state.ai_cache[article_id]

    if st.session_state.api_calls >= DAILY_LIMIT:
        return "⚠️ Daily AI limit reached. Come back tomorrow or refresh session."

    client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    try:
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Quick analysis for investors: {title}"}]
        )
        result = chat.choices[0].message.content
    except:
        result = "AI temporarily unavailable. Try again later."

    # Sentiment Analysis
    sentiment = TextBlob(title).sentiment.polarity
    sentiment_tag = "📈 Positive" if sentiment > 0 else ("📉 Negative" if sentiment < 0 else "⚖️ Neutral")
    result = f"{result}\n\nSentiment: {sentiment_tag}"

    # Cache & Increment API count
    st.session_state.ai_cache[article_id] = result
    st.session_state.api_calls += 1

    return result

# ======================
# 7️⃣ Market Sentiment Function
# ======================
def get_sentiment_index(title):
    polarity = TextBlob(title).sentiment.polarity
    if polarity > 0.2:
        return "🚀 BULLISH (+78%)", "#3FB950"
    elif polarity < -0.2:
        return "📉 BEARISH (-65%)", "#FF5555"
    else:
        return "⚖️ NEUTRAL (0%)", "#F0E68C"

# ======================
# 8️⃣ Display News
# ======================
st.markdown('<div class="main-header"><h1>TECH PULSE AI ⚡ Offline</h1><p>Global Intelligence</p></div>', unsafe_allow_html=True)

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
            
            # Market Sentiment
            mood_text, mood_color = get_sentiment_index(art['title'])
            st.markdown(f'<div class="market-mood" style="color:{mood_color}">Sentiment Index: {mood_text}</div>', unsafe_allow_html=True)
            
            # Buttons: AI Analysis + Share on X + Share on Facebook
            c1, c2, c3 = st.columns([1,1,1])
            with c1:
                if st.button(f"🧠 AI ANALYSIS", key=f"ai_{i}"):
                    analysis = ai_analyze(article_id, art['title'])
                    st.info(analysis)
            with c2:
                t_text = f"⚡ INTEL: {art['title']}\n\n🔗 Report: {SITE_URL}"
                t_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(t_text)}"
                st.markdown(f'''
                    <a href="{t_url}" target="_blank">
                        <div style="background-color:#1F6FEB; color:white; padding:10px; border-radius:6px; text-align:center; font-weight:600;">🚀 SHARE ON X</div>
                    </a>
                ''', unsafe_allow_html=True)
            with c3:
                fb_url = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(SITE_URL)}&quote={urllib.parse.quote(art['title'])}"
                st.markdown(f'''
                    <a href="{fb_url}" target="_blank">
                        <div style="background-color:#3b5998; color:white; padding:10px; border-radius:6px; text-align:center; font-weight:600;">📘 SHARE ON FB</div>
                    </a>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 9️⃣ Adsterra Bottom
# ======================
components.html('''
<div style="text-align:center; margin-top:20px;">
<script type="text/javascript">
atOptions = {
    "key" : "5f66cec17e51208142b62c4800c4705d",
    "format" : "iframe",
    "height" : 90,
    "width" : 728,
    "params" : {}
};
</script>
<script type="text/javascript" src="https://fugitivedepart.com/5f66cec17e51208142b62c4800c4705d/invoke.js"></script>
</div>
''', height=100)

# ======================
# 10️⃣ Footer
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
