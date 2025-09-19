import requests
import streamlit as st
from bs4 import BeautifulSoup
import html

NEWS_API_KEY = "2d282d61fa0d456fb4c77f00569cfac9"
MAX_ARTICLES = 12  

AI_KEYWORDS = ["ai", "artificial intelligence", "machine learning", "ml"]

def strip_html(text):
    if not text:
        return ""
    return BeautifulSoup(text, "html.parser").get_text(separator=" ", strip=True)

def is_ai_related(text):
    if not text:
        return False
    lower = text.lower()
    return any(keyword in lower for keyword in AI_KEYWORDS)

@st.cache_data(ttl=3600)
def get_daily_ai_news():
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=ai OR artificial intelligence OR machine learning OR ml&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"pageSize=30&"
        f"apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to fetch news. Please check API or quota.")
        return []

    data = response.json()
    raw_articles = data.get("articles", [])

    cleaned_articles = []
    for article in raw_articles:
        raw_title = article.get("title", "")
        raw_desc = article.get("description", "")
        raw_content = article.get("content", "")
        raw_source = article.get("source", {}).get("name", "Unknown Source")

        clean_title = strip_html(raw_title)
        clean_summary = strip_html(raw_desc or raw_content)
        clean_source = strip_html(raw_source)

        if "biztoc" in clean_source.lower():
            continue

        if is_ai_related(clean_title) or is_ai_related(clean_summary):
            cleaned_articles.append({
                "title": clean_title,
                "summary": clean_summary,
                "source": clean_source,
                "url": article.get("url", "#"),
            })

        if len(cleaned_articles) >= 9:
            break

    return cleaned_articles


def _card_html(news: dict) -> str:
    title = html.escape(news.get('title', 'No Title'))
    summary = html.escape(news.get('summary', ''))
    source = html.escape(news.get('source', 'Unknown Source'))
    url = news.get('url', '#')

    return f"""
        <div style="
            background:white;
            border:1px solid #ddd;
            border-radius:12px;
            padding:18px;
            height:300px;
            display:flex;
            flex-direction:column;
            justify-content:space-between;
            box-shadow:0 2px 8px rgba(0,0,0,.05);
            transition:box-shadow .3s ease;
            overflow:hidden;
        ">
            <div style="font-weight:600;font-size:17px;color:#0056D6;margin-bottom:10px;">
                🔷 {title}
            </div>
            <div style="font-size:14px;color:#333;flex-grow:1; overflow:hidden; text-overflow:ellipsis;">
                {summary}
            </div>
            <div style="font-size:12px;color:#888;margin:10px 0 6px 0;">
                {source}
            </div>
            <a href="{url}" target="_blank"
               style="font-size:14px;font-weight:bold;color:#007BFF;text-decoration:none;">
               Read more →
            </a>
        </div>
    """


def show_ai_news():
    st.title("AI & Dev News Feed")
    st.caption("Top news stories on AI/ML, filtered and cleaned every 1 hour.")

    news_items = get_daily_ai_news()
    if not news_items:
        st.warning("No AI/ML news articles found right now.")
        return

    rows = [news_items[i:i + 3] for i in range(0, len(news_items), 3)]
    for row in rows:
        cols = st.columns(3)
        for idx, news in enumerate(row):
            with cols[idx]:
                st.markdown(_card_html(news), unsafe_allow_html=True)