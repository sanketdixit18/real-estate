import streamlit as st

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Real Estate Price Prediction | Sanket Dixit",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CITY DATA — add a new dict here to support another city, no HTML editing needed
# ---------------------------------------------------------------------------
CITIES = [
    # {
    #     "emoji": "🌆",
    #     "name": "Mumbai",
    #     "tag": "Location-based Model",
    #     "points": [
    #         "Apartments & independent houses",
    #         "Location-wise price prediction",
    #         "Area (sq. ft.) driven analysis",
    #         "Market insight visualizations",
    #     ],
    # },
    {
        "emoji": "🏙️",
        "name": "Gurgaon",
        "tag": "Sector-based Model",
        "status": "active",
        "points": [
            "Apartments & independent floors",
            "Sector-wise price prediction",
            "Property comparison tool",
            "Price trend analysis",
        ],
    },
    {
        "emoji": "🚀",
        "name": "Upcoming Cities",
        "tag": "Future Expansion",
        "status": "coming_soon",
        "points": [
            "Mumbai",
            "Bengaluru",
            "Delhi NCR",
            "Hyderabad",
            "Pune",
        ],
    }
    # {
    #     "emoji": "🏢",
    #     "name": "Pune",
    #     "tag": "Micro-market Model",
    #     "points": ["Point 1", "Point 2", "Point 3", "Point 4"],
    # },
]

# ---------------------------------------------------------------------------
# CUSTOM CSS — all text colors are set explicitly so the layout looks the
# same whether Streamlit is running in Light or Dark theme.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        padding: 3rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 1.8rem;
    }
    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        color: #ffffff !important;
    }
    .hero p {
        font-size: 1.05rem;
        color: #d7e3ea !important;
        max-width: 720px;
        line-height: 1.6;
    }
    .badge-row { margin-top: 1.2rem; }
    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.3);
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 0.8rem;
        margin-right: 8px;
        margin-bottom: 8px;
        color: #ffffff !important;
    }

    /* Section header bar — self-contained so it never depends on theme bg */
    .section-title {
        background: #0F2027;
        color: #ffffff !important;
        font-size: 1.15rem;
        font-weight: 700;
        padding: 0.6rem 1.1rem;
        border-radius: 10px;
        margin-top: 2.2rem;
        margin-bottom: 1rem;
        display: inline-block;
    }

    /* Metric cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #eaeaea;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .metric-card h2 {
        font-size: 1.9rem;
        margin: 0;
        color: #203A43 !important;
    }
    .metric-card p {
        margin: 0;
        color: #6b7280 !important;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* City cards */
    .city-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.6rem;
        border: 1px solid #eee;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        height: 100%;
    }
    .city-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    .city-card h3 {
        margin-top: 0;
        color: #0F2027 !important;
    }
    .city-card ul {
        padding-left: 1.2rem;
        margin: 0.5rem 0;
    }
    .city-card li {
        color: #333333 !important;
        margin-bottom: 0.25rem;
    }
    .city-tag {
        display: inline-block;
        background: #eef4f8;
        color: #203A43 !important;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 999px;
        margin-top: 0.6rem;
    }

    /* Feature grid */
    .feature-box {
        background: #fafafa;
        border-left: 4px solid #2C5364;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
        color: #333333 !important;
    }
    .feature-box b { color: #0F2027 !important; }

    /* Info strip */
    .info-strip {
        background: #eef4f8;
        color: #0F2027 !important;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        margin-top: 0.5rem;
        border-left: 4px solid #2C5364;
    }

    /* Footer / dev card */
    .dev-card {
        background: #0F2027;
        color: #ffffff !important;
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin-top: 2.5rem;
    }
    .dev-card p, .dev-card h3 { color: #ffffff !important; }
    .dev-card a {
        color: #7fdbff !important;
        text-decoration: none;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------------------------
# city_names = " and ".join([c["name"] for c in CITIES[:2]]) if len(CITIES) <= 2 else \
#     ", ".join([c["name"] for c in CITIES[:-1]]) + f", and {CITIES[-1]['name']}"

active_cities = [
    c["name"] for c in CITIES 
    if c["status"] == "active"
]

city_names = ", ".join(active_cities)

st.markdown(f"""
<div class="hero">
    <h1>🏠 Real Estate Price Prediction System</h1>
    <p>
        An end-to-end Machine Learning application that estimates residential property
        prices across <b>{city_names}</b> using models trained on real transaction and
        listing data — covering data cleaning, feature engineering, model training,
        and an interactive prediction interface.
    </p>
    <div class="badge-row">
        <span class="badge">🐍 Python</span>
        <span class="badge">📊 Scikit-learn</span>
        <span class="badge">🧮 Pandas / NumPy</span>
        <span class="badge">📈 Streamlit</span>
        <span class="badge">🗺️ EDA & Feature Engineering</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KEY METRICS (⚠️ placeholders — replace with your real model results)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">📌 Project Snapshot</div>', unsafe_allow_html=True)

metric_cols = st.columns(5)
metrics = [
    ("R² Score", "97.8%"),
    ("MAE", "₹18 Lakh"),
    ("Properties Analyzed", "5k+"),
    # ("Cities Covered", str(len(CITIES))),
    ("Cities Covered", str(len(active_cities))),
    ("Features Engineered", "20+"),
    
]
for (label, value), col in zip(metrics, metric_cols):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{value}</h2>
            <p>{label}</p>
        </div>
        """, unsafe_allow_html=True)

# st.caption("⚠️ Update these numbers with your actual model performance (R², MAE, dataset size) before publishing.")

# ---------------------------------------------------------------------------
# CITY CARDS — auto-generated from the CITIES list above, 2 per row.
# To add a new city, just add a dict to CITIES at the top of the file.
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🌍 Supported Markets</div>', unsafe_allow_html=True)

for i in range(0, len(CITIES), 2):
    row = CITIES[i:i + 2]
    cols = st.columns(2)
    for city, col in zip(row, cols):
        points_html = "".join([f"<li>{p}</li>" for p in city["points"]])
        with col:
            st.markdown(f"""
            <div class="city-card">
                <h3>{city['emoji']} {city['name']}</h3>
                <ul>{points_html}</ul>
                <span class="city-tag">{city['tag']}</span>
            </div>
            """, unsafe_allow_html=True)
    if len(row) == 1:
        cols[1].empty()

# ---------------------------------------------------------------------------
# FEATURES / WHAT THIS PROJECT DEMONSTRATES
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🧠 What This Project Demonstrates</div>', unsafe_allow_html=True)

f1, f2 = st.columns(2)
with f1:
    st.markdown("""
    <div class="feature-box"><b>Data Cleaning & Preprocessing</b><br>Handling missing values, outliers, and inconsistent listing formats.</div>
    <div class="feature-box"><b>Feature Engineering</b><br>Deriving price-per-sqft, locality encodings, and property-age features.</div>
    <div class="feature-box"><b>Exploratory Data Analysis</b><br>Visualizing price distribution, correlation heatmaps, and locality trends.</div>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="feature-box"><b>Model Building & Tuning</b><br>Comparing regression models with cross-validation and GridSearchCV.</div>
    <div class="feature-box"><b>Interactive Prediction UI</b><br>Real-time price estimation from user-selected property attributes.</div>
    <div class="feature-box"><b>Deployment-ready App</b><br>Packaged as a multi-page Streamlit application with clean UX.</div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="info-strip">
    👈 Use the sidebar to navigate to the <b>Price Predictor</b>, <b>EDA Dashboard</b>, and <b>Property Comparison</b> pages.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DEVELOPER / RECRUITER CTA
# ---------------------------------------------------------------------------
st.markdown("""
<div class="dev-card">
    <h3>👋 Built by Sanket Dixit</h3>
    <p>Computer Engineering student (Data Science) — building applied ML projects
    focused on real-world, structured data problems.</p>
    <p>
        🔗 <a href="https://linkedin.com/in/sanket-dixit-85983a243" target="_blank">LinkedIn Profile</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        💻 <a href="https://github.com/sanketdixit18/Real-estate-app" target="_blank">GitHub Repository </a>
    </p>
</div>
""", unsafe_allow_html=True)