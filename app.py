import requests
import streamlit as st
import pickle
import re

API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
OMDB_API_KEY = "3c99009e"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown(
    """
<style>
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
.small-muted { color:#6b7280; font-size: 0.92rem; }
.movie-title { font-size: 0.9rem; line-height: 1.15rem; height: 2.3rem; overflow: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

def normalize_title(title):
    title = title.lower()
    title = re.sub(r"\s*\(\d{4}\)", "", title)
    title = re.sub(r"[^a-z0-9\s]", "", title)
    return title.strip()

def fetch_imdb_details(movie_title):
    r = requests.get(
        "http://www.omdbapi.com/",
        params={"t": movie_title, "apikey": OMDB_API_KEY},
    ).json()
    if r.get("Response") == "True":
        return {
            "imdb_rating": r.get("imdbRating", "N/A"),
            "imdb_votes": r.get("imdbVotes", "N/A"),
        }
    return {"imdb_rating": "N/A", "imdb_votes": "N/A"}

@st.cache_data
def load_sentiment_data():
    with open("movie_sentiment.pkl", "rb") as f:
        raw = pickle.load(f)
    return {normalize_title(k): v for k, v in raw.items()}

@st.cache_data(ttl=30)
def api_get_json(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, r.text
        return r.json(), None
    except Exception as e:
        return None, str(e)

def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    st.query_params.pop("id", None)
    st.rerun()

def goto_details(tmdb_id):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = tmdb_id
    st.query_params["view"] = "details"
    st.query_params["id"] = str(tmdb_id)
    st.rerun()

def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return
    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for _ in range(rows):
        colset = st.columns(cols)
        for c in colset:
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1
            with c:
                if m.get("poster_url"):
                    st.image(m["poster_url"], width=220)
                if st.button("Open", key=f"{key_prefix}_{idx}_{m.get('tmdb_id')}"):
                    goto_details(m["tmdb_id"])
                st.markdown(
                    f"<div class='movie-title'>{m.get('title','')}</div>",
                    unsafe_allow_html=True,
                )

def parse_tmdb_search_to_cards(data, keyword, limit=24):
    keyword = keyword.lower()
    raw_items = []
    if isinstance(data, dict) and "results" in data:
        for m in data["results"]:
            if not m.get("id") or not m.get("title"):
                continue
            raw_items.append(
                {
                    "tmdb_id": m["id"],
                    "title": m["title"],
                    "poster_url": f"{TMDB_IMG}{m['poster_path']}"
                    if m.get("poster_path")
                    else None,
                    "release_date": m.get("release_date", ""),
                }
            )
    matched = [x for x in raw_items if keyword in x["title"].lower()]
    final = matched if matched else raw_items
    suggestions = []
    for x in final[:10]:
        year = x["release_date"][:4] if x["release_date"] else ""
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))
    cards = final[:limit]
    return suggestions, cards

if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass

with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)

st.title("🎬 Movie Recommender")
st.markdown(
    "<div class='small-muted'>Search → Select → View details & recommendations</div>",
    unsafe_allow_html=True,
)
st.divider()

if st.session_state.view == "home":
    typed = st.text_input("Search movie", placeholder="avengers, batman...")

    if typed.strip():
        data, err = api_get_json("/tmdb/search", {"query": typed})
        if err:
            st.error(err)
        else:
            suggestions, cards = parse_tmdb_search_to_cards(data, typed)
            if suggestions:
                labels = ["-- Select --"] + [s[0] for s in suggestions]
                choice = st.selectbox("Suggestions", labels)
                if choice != "-- Select --":
                    goto_details(dict(suggestions)[choice])
            poster_grid(cards, cols=grid_cols, key_prefix="search")
        st.stop()

    data, err = api_get_json("/home", {"category": home_category})
    if err:
        st.error(err)
    else:
        poster_grid(data, cols=grid_cols, key_prefix="home")

elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id

    if st.button("← Back"):
        goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err:
        st.error(err)
        st.stop()

    left, right = st.columns([1, 2])

    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], width=320)

    with right:
        st.markdown(f"## {data['title']}")
        st.markdown(f"**Release:** {data.get('release_date','-')}")
        st.markdown(
            f"**Genres:** {', '.join(g['name'] for g in data.get('genres',[]))}"
        )

        imdb = fetch_imdb_details(data["title"])
        st.markdown(f"**IMDb Rating:** {imdb['imdb_rating']}")
        st.markdown(f"**IMDb Votes:** {imdb['imdb_votes']}")

        st.write(data.get("overview"))

        sentiment_cache = load_sentiment_data()
        key = normalize_title(data["title"])
        sentiment = sentiment_cache.get(key)

        if not sentiment:
            base = re.sub(r"\s+\d+$", "", key)
            sentiment = sentiment_cache.get(base)

        if sentiment:
            st.markdown("### 📊 Sentiment Analysis")
            c1, c2 = st.columns(2)
            c1.metric("Positive Reviews", sentiment["total_positive"])
            c2.metric("Negative Reviews", sentiment["total_negative"])

            st.markdown("#### 👍 Top 5 Positive Reviews")
            for i, r in enumerate(sentiment["top_positive_reviews"], 1):
                st.write(f"{i}. {r[:300]}...")

            st.markdown("#### 👎 Top 5 Negative Reviews")
            for i, r in enumerate(sentiment["top_negative_reviews"], 1):
                st.write(f"{i}. {r[:300]}...")
        else:
            st.info("Sentiment data not available for this movie.")

    st.divider()

    bundle, _ = api_get_json(
        "/movie/search", {"query": data["title"], "tfidf_top_n": 12}
    )

    if bundle:
        st.markdown("### 🔎 Similar Movies")
        poster_grid(
            [
                {
                    "tmdb_id": x["tmdb"]["tmdb_id"],
                    "title": x["title"],
                    "poster_url": x["tmdb"]["poster_url"],
                }
                for x in bundle.get("tfidf_recommendations", [])
                if x.get("tmdb")
            ],
            cols=grid_cols,
            key_prefix="tfidf",
        )
