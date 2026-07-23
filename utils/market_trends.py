"""
Gurgaon Real Estate — Market Trends Dashboard
------------------------------------------------
v2: rebuilt against the actual `gurgaon_market_trends.csv` schema.

Data-quality fixes that matter for a portfolio piece:
- `builder_name` is NOT the real estate developer — it's the listing
  source/agent ("Property In Gurgaon", "Home", "Seller", "Proptiger"...).
  The real developer lives in `company_name` (M3M, DLF, Godrej, Signature…).
  Using `builder_name` for "Top Builders" (like the original code did)
  produces a meaningless chart. Fixed to use `company_name`.
- `property_type` is a free-text listing title (1,800+ unique values,
  basically ad titles). `flat_type` is the clean category
  (Apartment / Floor / Plot / Villa / House / Penthouse) — used instead.
- A handful of listings have absurd outliers (e.g. one row lists area at
  ~958,000 sq.ft, another lists 132 BHK) that stretch axes and make
  scatter/histogram charts unreadable. These are clipped (1st–99th
  percentile) only for the visuals that are sensitive to them — the KPI
  numbers still reflect the full dataset.
- Builder-level "average price" is only computed for builders with a
  minimum listing volume, so a single ultra-luxury outlier project
  doesn't masquerade as a "top premium builder".

Visual-design fixes (this was the main complaint — "looking ugly"):
- One consistent color system instead of a different rainbow colorscale
  (Turbo/Viridis/Plasma/Set2/Set3/Pastel) on every single chart.
- A shared Plotly template, consistent chart heights/margins/fonts.
- Content organized into tabs instead of one long scroll of 15+ charts.
- Styled KPI cards via a small CSS injection instead of default st.metric.
"""

import streamlit as st
import plotly.express as px
import pandas as pd


# ==========================================================================
# Design system — one place to change the whole dashboard's look
# ==========================================================================

PRIMARY = "#5B4FE9"        # accent (headers, highlights)
SEQUENTIAL_SCALE = "Purples"    # used for every "ranked bar" chart
CATEGORICAL_PALETTE = [
    "#5B4FE9", "#00B8A9", "#F6A609", "#F65D5D",
    "#3BB3E0", "#8E7DFF", "#2FB380", "#F08CD8",
]
PLOTLY_TEMPLATE = "plotly_white"
CHART_FONT = dict(family="Inter, Segoe UI, sans-serif", size=13, color="#2B2B33")


def _inject_css():
    st.markdown(
        f"""
        <style>
        .kpi-card {{
            background: white;
            border: 1px solid #ECECF4;
            border-radius: 14px;
            padding: 16px 18px;
            box-shadow: 0 2px 10px rgba(30, 30, 60, 0.04);
        }}
        .kpi-label {{
            font-size: 0.80rem;
            color: #7A7A8C;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-size: 1.55rem;
            font-weight: 700;
            color: #1E1E2E;
        }}
        .section-divider {{
            margin: 1.6rem 0 0.8rem 0;
            border-top: 1px solid #ECECF4;
        }}
        div[data-testid="stMetricValue"] {{ color: {PRIMARY}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _kpi_card(col, label: str, value: str):
    col.markdown(
        f"""<div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def _style(fig, title: str, height: int = 440, **layout_kwargs):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title=dict(text=title, font=dict(size=16, family=CHART_FONT["family"], color="#1E1E2E")),
        font=CHART_FONT,
        height=height,
        margin=dict(l=10, r=10, t=55, b=10),
        coloraxis_showscale=False,
        **layout_kwargs,
    )
    return fig


# ==========================================================================
# Data helpers
# ==========================================================================

def _clip_outliers(df: pd.DataFrame, col: str, lower=0.01, upper=0.99) -> pd.DataFrame:
    lo, hi = df[col].quantile([lower, upper])
    return df[df[col].between(lo, hi)]


def _top_n_bar(df: pd.DataFrame, group_col: str, value_col: str, agg: str,
                title: str, x_title: str, n: int = 10, text_fmt=".2f", height=440):
    ranked = (
        df.groupby(group_col, as_index=False)[value_col]
        .agg(agg)
        .rename(columns={value_col: "value"})
        .sort_values("value", ascending=False)
        .head(n)
    )
    fig = px.bar(
        ranked, x="value", y=group_col, orientation="h",
        color="value", color_continuous_scale=SEQUENTIAL_SCALE, text_auto=text_fmt,
    )
    fig.update_traces(marker_line_width=0)
    fig = _style(fig, title, height=height, xaxis_title=x_title, yaxis_title="")
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, width="stretch")


def _donut(series: pd.Series, title: str, height=380):
    counts = series.value_counts().reset_index()
    counts.columns = ["label", "count"]
    fig = px.pie(
        counts, names="label", values="count", hole=0.55,
        color_discrete_sequence=CATEGORICAL_PALETTE,
    )
    fig.update_traces(textinfo="percent+label", textfont_size=12)
    fig = _style(fig, title, height=height, showlegend=False)
    st.plotly_chart(fig, width="stretch")


# ==========================================================================
# Main page
# ==========================================================================

def market_trends_page(market_df: pd.DataFrame):
    _inject_css()

    st.title("📈 Gurgaon Real Estate — Market Trends")
    st.caption("Market intelligence dashboard · price, location, and builder analysis")

    # ---- Filters ----
    with st.expander("🎛 Filters", expanded=False):
        f1, f2, f3, f4 = st.columns(4)
        sel_locality = f1.selectbox("Locality", ["All"] + sorted(market_df["locality"].unique()))
        sel_builder = f2.selectbox("Builder", ["All"] + sorted(market_df["company_name"].unique()))
        sel_type = f3.selectbox("Property Type", ["All"] + sorted(market_df["flat_type"].unique()))
        sel_segment = f4.selectbox("Price Segment", ["All"] + sorted(market_df["price_segment"].unique()))

    mask = pd.Series(True, index=market_df.index)
    if sel_locality != "All":
        mask &= market_df["locality"] == sel_locality
    if sel_builder != "All":
        mask &= market_df["company_name"] == sel_builder
    if sel_type != "All":
        mask &= market_df["flat_type"] == sel_type
    if sel_segment != "All":
        mask &= market_df["price_segment"] == sel_segment
    df = market_df[mask]

    if df.empty:
        st.warning("No listings match the selected filters — try widening them.")
        return

    # ---- KPI row ----
    k1, k2, k3, k4, k5 = st.columns(5)
    _kpi_card(k1, "Avg Price", f"₹ {df['price_cr'].mean():.2f} Cr")
    _kpi_card(k2, "Avg Rate", f"₹ {df['price_per_sqft'].mean():,.0f} /sq.ft")
    _kpi_card(k3, "Localities", f"{df['locality'].nunique()}")
    _kpi_card(k4, "Listings", f"{len(df):,}")
    _kpi_card(k5, "Median BHK", f"{df['bhk'].median():.0f} BHK")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    tab_overview, tab_location, tab_builders, tab_price, tab_highlights = st.tabs(
        ["🏠 Overview", "📍 Location", "🏗 Builders & Projects", "💰 Price & Area", "🏆 Highlights"]
    )

    # ------------------------------------------------------------------
    with tab_overview:
        c1, c2 = st.columns(2)
        with c1:
            _donut(df["price_segment"], "Price Segment Mix")
        with c2:
            _donut(df["flat_type"], "Property Type Mix")

        c3, c4 = st.columns(2)
        with c3:
            _donut(df["status"], "Construction Status")
        with c4:
            _donut(df["rera_approval"], "RERA Approval")

    # ------------------------------------------------------------------
    with tab_location:
        c1, c2 = st.columns(2)
        with c1:
            _top_n_bar(df, "locality", "price_cr", "mean",
                       "Top 10 Most Expensive Localities", "Avg Price (Cr)")
        with c2:
            _top_n_bar(df, "locality", "price_per_sqft", "mean",
                       "Top 10 Highest Rate Localities", "₹ / sq.ft", text_fmt=".0f")

        listings = df["locality"].value_counts().head(12).reset_index()
        listings.columns = ["locality", "value"]
        fig = px.bar(listings, x="locality", y="value", color="value",
                     color_continuous_scale=SEQUENTIAL_SCALE, text_auto=True)
        fig.update_traces(marker_line_width=0)
        fig = _style(fig, "Most Active Localities by Listings", height=420,
                     xaxis_title="", yaxis_title="Listings")
        st.plotly_chart(fig, width="stretch")

    # ------------------------------------------------------------------
    with tab_builders:
        # only builders with meaningful volume qualify for "avg price" ranking
        volume_ok = df["company_name"].value_counts()
        eligible_builders = volume_ok[volume_ok >= max(5, int(len(df) * 0.002))].index
        builder_df = df[df["company_name"].isin(eligible_builders)]

        c1, c2 = st.columns(2)
        with c1:
            _top_n_bar(df, "company_name", "price_cr", "count",
                       "Top Builders by Listings", "Listings", text_fmt=True)
        with c2:
            if not builder_df.empty:
                _top_n_bar(builder_df, "company_name", "price_cr", "mean",
                           "Top Premium Builders (min. listing volume)", "Avg Price (Cr)")
            else:
                st.info("Not enough listing volume per builder to rank by average price.")

        st.markdown("##### Top Societies / Projects")
        soc = df[df["society"] != "Outside Socity"]["society"].value_counts().head(10).reset_index()
        soc.columns = ["society", "value"]
        fig = px.bar(soc, x="value", y="society", orientation="h",
                     color="value", color_continuous_scale=SEQUENTIAL_SCALE, text_auto=True)
        fig.update_traces(marker_line_width=0)
        fig = _style(fig, "Most Listed Projects", height=420, xaxis_title="Listings", yaxis_title="")
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, width="stretch")

    # ------------------------------------------------------------------
    with tab_price:
        clipped = _clip_outliers(_clip_outliers(df, "price_cr"), "area")
        st.caption("Scatter and histograms below exclude the top/bottom 1% of price & area "
                   "values (data-entry outliers) for a readable scale. KPI numbers above use the full dataset.")

        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(clipped, x="price_cr", nbins=30, color_discrete_sequence=[PRIMARY])
            fig = _style(fig, "Price Distribution", xaxis_title="Price (Cr)", yaxis_title="Listings")
            st.plotly_chart(fig, width="stretch")
        with c2:
            fig = px.scatter(clipped, x="area", y="price_cr", color="flat_type",
                              opacity=0.6, color_discrete_sequence=CATEGORICAL_PALETTE,
                              hover_data=["locality"])
            fig = _style(fig, "Area vs Price", xaxis_title="Area (sq.ft)", yaxis_title="Price (Cr)")
            st.plotly_chart(fig, width="stretch")

        c3, c4 = st.columns(2)
        with c3:
            fig = px.box(clipped, x="flat_type", y="price_cr", color="flat_type",
                         color_discrete_sequence=CATEGORICAL_PALETTE)
            fig = _style(fig, "Price by Property Type", xaxis_title="", yaxis_title="Price (Cr)", showlegend=False)
            st.plotly_chart(fig, width="stretch")
        with c4:
            rera_price = df.groupby("rera_approval", as_index=False)["price_per_sqft"].mean()
            fig = px.bar(rera_price, x="rera_approval", y="price_per_sqft",
                         color="rera_approval", color_discrete_sequence=CATEGORICAL_PALETTE,
                         text_auto=".0f")
            fig = _style(fig, "Avg Rate: RERA vs Non-RERA", xaxis_title="",
                         yaxis_title="₹ / sq.ft", showlegend=False)
            st.plotly_chart(fig, width="stretch")

    # ------------------------------------------------------------------
    with tab_highlights:
        price_by_locality = df.groupby("locality")["price_cr"].mean()
        expensive, expensive_price = price_by_locality.idxmax(), price_by_locality.max()
        cheap, cheap_price = price_by_locality.idxmin(), price_by_locality.min()

        builder_counts = df["company_name"].value_counts()
        top_builder, builder_listings = builder_counts.idxmax(), builder_counts.max()

        locality_counts = df["locality"].value_counts()
        active_locality, active_count = locality_counts.idxmax(), locality_counts.max()

        r1 = st.columns(4)
        r1[0].info(f"**🏆 Most Expensive Locality**\n\n{expensive}\n\n₹ {expensive_price:.2f} Cr avg")
        r1[1].success(f"**💸 Most Affordable Locality**\n\n{cheap}\n\n₹ {cheap_price:.2f} Cr avg")
        r1[2].warning(f"**🏗 Top Builder by Volume**\n\n{top_builder}\n\n{builder_listings:,} listings")
        r1[3].error(f"**📍 Most Active Locality**\n\n{active_locality}\n\n{active_count:,} listings")

        r2 = st.columns(4)
        r2[0].metric("Popular Type", df["flat_type"].mode()[0])
        r2[1].metric("Common BHK", f"{df['bhk'].mode()[0]} BHK")
        r2[2].metric("RERA-Approved Share", f"{(df['rera_approval'] == 'Approved By Rera').mean() * 100:.0f}%")
        r2[3].metric("Ready-to-Move Share", f"{(df['status'] == 'Ready to Move').mean() * 100:.0f}%")