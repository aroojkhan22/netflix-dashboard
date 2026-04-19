import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Netflix Analytics Pro", page_icon="🎬", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/netflix_titles.csv")

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df["year_added"] = df["date_added"].dt.year
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Unknown")
df["listed_in"] = df["listed_in"].fillna("Unknown")

# ---------------- COUNTRY LIST ----------------
all_countries = (
    df["country"]
    .str.split(", ")
    .explode()
    .dropna()
    .unique()
    .tolist()
)
all_countries = sorted(all_countries)

# ---------------- STYLE ----------------
st.markdown("""
<style>
/* Remove top white bar */
header[data-testid="stHeader"]{
    background: transparent;
    height: 0px;
}

/* Main app background */
.stApp {
    background:
        radial-gradient(circle at top left, #2a0018 0%, #090909 35%),
        radial-gradient(circle at bottom right, #22002e 0%, #090909 40%);
    color: white;
}

/* Main content */
.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Headings */
h1 {
    color: white !important;
    font-weight: 800 !important;
    font-size: 3rem !important;
    letter-spacing: 0.5px;
}

h2, h3 {
    color: #ff2d55 !important;
    font-weight: 800 !important;
}

p, div, label, span {
    color: white !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050505 0%, #0d0d0d 60%, #14051a 100%);
    border-right: 1px solid #222;
    width: 260px !important;
}

/* Inputs */
.stMultiSelect div[data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] > div {
    background: #151515 !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 14px !important;
    color: white !important;
    min-height: 52px !important;
}

/* Dropdown popup */
div[data-baseweb="popover"] {
    background: #111111 !important;
}

div[role="listbox"] {
    background: #111111 !important;
    color: white !important;
    border: 1px solid #333 !important;
}

div[role="option"] {
    background: #111111 !important;
    color: white !important;
    font-weight: 500 !important;
}

div[role="option"]:hover {
    background: #E50914 !important;
    color: white !important;
}

/* Fallback dropdown */
ul {
    background: #111111 !important;
}

li {
    background: #111111 !important;
    color: white !important;
    font-weight: 500 !important;
}

li:hover {
    background: #E50914 !important;
    color: white !important;
}

/* Text input */
input {
    color: white !important;
    caret-color: white !important;
}

/* Selected tags */
span[data-baseweb="tag"] {
    background: linear-gradient(90deg, #E50914, #ff4d6d) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: linear-gradient(145deg, #111111, #1b1b1b);
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 0 18px rgba(229, 9, 20, 0.12);
}

/* Section cards */
.card {
    background: linear-gradient(145deg, #0d0d0d, #151515);
    border: 1px solid #252525;
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.08);
    margin-bottom: 20px;
    transition: 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.22);
}

/* Hero card */
.hero-card {
    background: linear-gradient(135deg, rgba(229,9,20,0.10), rgba(168,85,247,0.10));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 22px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}

/* Notes */
.small-note {
    color: #d1d5db !important;
    font-size: 15px;
}

/* Divider */
.hr-line {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #3a3a3a, transparent);
    margin-top: 10px;
    margin-bottom: 20px;
}

/* Sidebar title */
.sidebar-title {
    color: #ff4d6d !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown('<div class="sidebar-title">🎛 Filters</div>', unsafe_allow_html=True)

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=["Movie", "TV Show"],
    default=["Movie", "TV Show"]
)

country_filter = st.sidebar.selectbox(
    "Select Country",
    ["All"] + all_countries
)

# ---------------- FILTERING ----------------
filtered_df = df[df["type"].isin(type_filter)]

if country_filter != "All":
    filtered_df = filtered_df[
        filtered_df["country"].str.contains(
            rf"(^|,\s){re.escape(country_filter)}($|,\s)",
            na=False
        )
    ]

# ---------------- HERO SECTION ----------------
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st.markdown("# 🎬 NETFLIX ANALYTICS PRO")
st.markdown(
    "<p class='small-note'>Explore Netflix Movies and TV Shows with elegant interactive analytics and clean visual insights.</p>",
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- KPI CARDS ----------------
total_titles = len(filtered_df)
movies = len(filtered_df[filtered_df["type"] == "Movie"])
shows = len(filtered_df[filtered_df["type"] == "TV Show"])

c1, c2, c3 = st.columns(3)
c1.metric("Total Titles", total_titles)
c2.metric("Movies", movies)
c3.metric("TV Shows", shows)

st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)

# ---------------- FIRST ROW ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Content Type Share")
    type_counts = filtered_df["type"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 4), facecolor="#111111")
    ax.set_facecolor("#111111")
    ax.pie(
        type_counts,
        labels=type_counts.index,
        autopct="%1.1f%%",
        colors=["#E50914", "#8b5cf6"],
        textprops={"color": "white", "fontsize": 12},
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Top Ratings")
    ratings = filtered_df["rating"].value_counts().head(8)

    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#111111")
    ax.set_facecolor("#111111")
    ax.bar(
        ratings.index,
        ratings.values,
        color=["#E50914", "#ff4d6d", "#c084fc", "#a855f7", "#9333ea", "#fb7185", "#be123c", "#7c3aed"]
    )
    ax.tick_params(axis="x", rotation=35, colors="white", labelsize=10)
    ax.tick_params(axis="y", colors="white")
    ax.set_ylabel("Count", color="white")
    for spine in ax.spines.values():
        spine.set_color("#444")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SECOND ROW ----------------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Top Genres")
    genres = filtered_df["listed_in"].str.split(", ").explode()
    top_genres = genres.value_counts().head(8)

    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#111111")
    ax.set_facecolor("#111111")
    ax.barh(top_genres.index[::-1], top_genres.values[::-1], color="#a855f7")
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white", labelsize=10)
    ax.set_xlabel("Count", color="white")
    for spine in ax.spines.values():
        spine.set_color("#444")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Content Added By Year")
    yearly = filtered_df["year_added"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#111111")
    ax.set_facecolor("#111111")
    ax.plot(
        yearly.index,
        yearly.values,
        color="#ff4d6d",
        marker="o",
        linewidth=3,
        markersize=8
    )
    ax.tick_params(axis="x", colors="white", rotation=45)
    ax.tick_params(axis="y", colors="white")
    ax.set_xlabel("Year", color="white")
    ax.set_ylabel("Titles Added", color="white")
    for spine in ax.spines.values():
        spine.set_color("#444")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center style='color:#aaa;'>Built with ❤️ using Streamlit | Portfolio Project by Arooj</center>",
    unsafe_allow_html=True
)