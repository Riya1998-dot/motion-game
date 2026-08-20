import streamlit as st
import feedparser

st.set_page_config(
    page_title="AI News Trend Detector",
    page_icon="📰",
    layout="wide"
)

st.title("🧠 AI News Trend Detector")
st.caption("Live News Monitoring System")

st.divider()

# News sources
feeds = {
    "Google News - Technology":
        "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en",

    "Google News - Artificial Intelligence":
        "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-IN&gl=IN&ceid=IN:en",

    "Google News - Cybersecurity":
        "https://news.google.com/rss/search?q=cybersecurity&hl=en-IN&gl=IN&ceid=IN:en"
}

if st.button("🔄 Fetch Live News", use_container_width=True):

    for source, url in feeds.items():

        st.subheader(f"📰 {source}")

        news = feedparser.parse(url)

        for article in news.entries[:5]:

            st.markdown(
                f"### {article.title}"
            )

            if hasattr(article, "published"):
                st.caption(article.published)

            st.markdown(
                f"[Read Article →]({article.link})"
            )

            st.divider()

st.info(
    "V1: Live news collection. "
    "AI trend detection will be added in the next version."
)
