import streamlit as st
import feedparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from datetime import datetime
import re

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI News Trend Detector V2",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI News Trend Detector")
st.caption("LIVE News + Automatic AI/ML Topic Detection + Trend Score")

st.divider()

# --------------------------------------------------
# NEWS SOURCES
# --------------------------------------------------

feeds = {
    "Technology":
        "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en",

    "Artificial Intelligence":
        "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-IN&gl=IN&ceid=IN:en",

    "Cybersecurity":
        "https://news.google.com/rss/search?q=cybersecurity&hl=en-IN&gl=IN&ceid=IN:en",

    "Cloud Computing":
        "https://news.google.com/rss/search?q=cloud+computing&hl=en-IN&gl=IN&ceid=IN:en",

    "Stock Market":
        "https://news.google.com/rss/search?q=stock+market&hl=en-IN&gl=IN&ceid=IN:en"
}


# --------------------------------------------------
# FETCH NEWS
# --------------------------------------------------

def fetch_news():

    articles = []

    for source, url in feeds.items():

        news = feedparser.parse(url)

        for article in news.entries[:8]:

            title = article.get("title", "No Title")
            link = article.get("link", "#")
            published = article.get("published", "Recently")

            articles.append({
                "title": title,
                "link": link,
                "published": published,
                "source": source
            })

    return articles


# --------------------------------------------------
# CLEAN TEXT
# --------------------------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        "",
        text
    )

    return text


# --------------------------------------------------
# AI / ML TOPIC DETECTION
# --------------------------------------------------

def detect_topics(articles):

    if len(articles) < 3:
        return articles

    texts = [
        clean_text(article["title"])
        for article in articles
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=100
    )

    matrix = vectorizer.fit_transform(texts)

    # Number of topics
    number_of_topics = min(5, len(articles))

    model = KMeans(
        n_clusters=number_of_topics,
        random_state=42,
        n_init=10
    )

    clusters = model.fit_predict(matrix)

    # Get important words for each cluster
    feature_names = vectorizer.get_feature_names_out()

    topic_names = {}

    for cluster_id in range(number_of_topics):

        center = model.cluster_centers_[cluster_id]

        top_words = center.argsort()[-3:][::-1]

        words = [
            feature_names[i]
            for i in top_words
        ]

        topic_names[cluster_id] = " / ".join(words)

    for i, article in enumerate(articles):

        cluster_id = clusters[i]

        article["topic"] = topic_names[cluster_id]

    return articles


# --------------------------------------------------
# TREND SCORE
# --------------------------------------------------

def calculate_trends(articles):

    topic_counts = {}

    for article in articles:

        topic = article["topic"]

        topic_counts[topic] = (
            topic_counts.get(topic, 0) + 1
        )

    max_count = max(topic_counts.values())

    for article in articles:

        count = topic_counts[article["topic"]]

        # Trend score from 0 to 100
        score = int(
            (count / max_count) * 100
        )

        article["trend_score"] = score

    return articles, topic_counts


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if st.button(
    "🔄 Fetch LIVE News",
    use_container_width=True
):

    with st.spinner("Collecting live news and running AI/ML analysis..."):

        articles = fetch_news()

        if not articles:

            st.error(
                "Unable to collect news. "
                "Please check your internet connection."
            )

        else:

            # AI/ML topic detection
            articles = detect_topics(articles)

            # Trend calculation
            articles, topic_counts = calculate_trends(
                articles
            )

            # --------------------------------------------------
            # TOP METRICS
            # --------------------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "📰 Total News",
                len(articles)
            )

            col2.metric(
                "🧠 Topics Detected",
                len(topic_counts)
            )

            top_topic = max(
                topic_counts,
                key=topic_counts.get
            )

            col3.metric(
                "🔥 Top Topic",
                top_topic
            )

            col4.metric(
                "📈 Trend Score",
                "100 / 100"
            )

            st.divider()

            # --------------------------------------------------
            # TRENDING TOPICS
            # --------------------------------------------------

            st.header("🔥 Trending Topics")

            sorted_topics = sorted(
                topic_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )

            for topic, count in sorted_topics:

                score = int(
                    (count / max(topic_counts.values()))
                    * 100
                )

                st.write(
                    f"### 🔥 {topic}"
                )

                st.progress(
                    score / 100
                )

                st.caption(
                    f"{count} related articles • "
                    f"Trend Score: {score}/100"
                )

            st.divider()

            # --------------------------------------------------
            # NEWS ARTICLES
            # --------------------------------------------------

            st.header("📰 Live News Analysis")

            for article in articles:

                score = article["trend_score"]

                if score >= 80:
                    status = "🔥 HIGH TREND"

                elif score >= 50:
                    status = "📈 RISING"

                else:
                    status = "📊 NORMAL"

                st.markdown(
                    f"## {article['title']}"
                )

                col1, col2, col3 = st.columns(3)

                col1.write(
                    f"🧠 **AI Topic:** {article['topic']}"
                )

                col2.write(
                    f"📈 **Trend Score:** {score}/100"
                )

                col3.write(
                    f"🚦 **Status:** {status}"
                )

                st.caption(
                    f"Source: {article['source']} | "
                    f"{article['published']}"
                )

                st.markdown(
                    f"[🔗 Read Full Article →]({article['link']})"
                )

                st.divider()


# --------------------------------------------------
# INFORMATION
# --------------------------------------------------

st.info(
    "V2 uses TF-IDF + K-Means Machine Learning "
    "to automatically group similar news headlines "
    "and calculate a Trend Score based on topic frequency."
)
