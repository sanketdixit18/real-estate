# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import ast


# def analytics_page(analytics_df, wordcloud_df,city):
    
#         st.title("🌍 Gurgaon Analytics Dashboard")

#         geo_tab, wordcloud_tab, scatter_tab, pie_tab, box_tab, property_tab = st.tabs([
#             "🗺️ Geo Map",
#             "☁️ Word Cloud",
#             "📈 Area vs Price",
#             "🥧 BHK Distribution",
#             "📦 Bedroom Price",
#             "📊 Property Type",
#         ])

#         # -------------------------------
#         # GEO MAP
#         # -------------------------------
#         with geo_tab:

#             # ======================================================
#             # KPI CARDS
#             # ======================================================
#             avg_price = analytics_df["price"].mean()
#             max_price = analytics_df["price"].max()
#             min_price = analytics_df["price"].min()
#             total_sectors = analytics_df["sector"].nunique()
#             total_properties = len(analytics_df)

#             col1, col2, col3, col4 = st.columns(4)
#             col1.metric("🏠 Avg Price", f"₹ {avg_price:.1f} Cr")
#             col2.metric("📈 Highest", f"₹ {max_price:.1f} Cr")
#             col3.metric("📉 Lowest", f"₹ {min_price:.3f} Cr")
#             col4.metric("📍 Sectors", total_sectors)
#             # col5.metric("🏢 Listings", total_properties)

#             st.divider()

#             # ======================================================
#             # LAYOUT
#             # ======================================================
#             left, right = st.columns([1, 3])

#             # ======================================================
#             # FILTERS
#             # ======================================================
#             with left:
#                 st.subheader("🎛️ Filters")

#                 selected_sector = st.selectbox(
#                     "Sector",
#                     ["All"] + sorted(analytics_df["sector"].unique())
#                 )

#                 price_range = st.slider(
#                     "Price Range (Cr)",
#                     min_value=float(analytics_df["price"].min()),
#                     max_value=float(analytics_df["price"].max()),
#                     value=(
#                         float(analytics_df["price"].min()),
#                         float(analytics_df["price"].max())
#                     )
#                 )

#             # ======================================================
#             # APPLY FILTERS
#             # ======================================================
#             filtered_df = analytics_df.copy()

#             if selected_sector != "All":
#                 filtered_df = filtered_df[filtered_df["sector"] == selected_sector]

#             filtered_df = filtered_df[
#                 (filtered_df["price"] >= price_range[0]) &
#                 (filtered_df["price"] <= price_range[1])
#             ]

#             # ======================================================
#             # CREATE MAP DATA
#             # ======================================================
#             map_df = (
#                 filtered_df
#                 .groupby("sector", as_index=False)
#                 .agg({
#                     "price": "mean",
#                     "latitude": "first",
#                     "longitude": "first"
#                 })
#             )

#             # ======================================================
#             # RIGHT PANEL
#             # ======================================================
#             with right:
#                 st.subheader("🗺️ Gurgaon Property Price Map")

#                 fig = go.Figure()

#                 fig.add_trace(
#                     go.Scattermapbox(
#                         lat=map_df["latitude"],
#                         lon=map_df["longitude"],
#                         mode="markers",
#                         text=map_df["sector"],
#                         customdata=map_df[["price"]],
#                         marker=dict(
#                             size=18,
#                             color=map_df["price"],
#                             colorscale="Turbo",
#                             showscale=True,
#                             opacity=0.85,
#                             colorbar=dict(title="Avg Price (Cr)")
#                         ),
#                         hovertemplate=(
#                             "<b>%{text}</b><br><br>"
#                             "Average Price : ₹ %{customdata[0]:.2f} Cr"
#                             "<extra></extra>"
#                         )
#                     )
#                 )

#                 fig.update_layout(
#                     mapbox=dict(
#                         style="carto-positron",
#                         center=dict(lat=28.4595, lon=77.0266),
#                         zoom=10
#                     ),
#                     height=550,
#                     margin=dict(l=0, r=0, t=0, b=0)
#                 )

#                 st.plotly_chart(fig, width="stretch")

#         # -------------------------------
#         # WORD CLOUD
#         # -------------------------------
#         with wordcloud_tab:
#             st.header("☁️ Amenities Word Cloud")

#             selected_sector = st.selectbox(
#                 "Select Sector",
#                 ["All"] + sorted(wordcloud_df["sector"].unique())
#             )

#             filtered_df = wordcloud_df.copy()

#             if selected_sector != "All":
#                 filtered_df = filtered_df[filtered_df["sector"] == selected_sector]

#             all_features = []
#             for item in filtered_df["features"]:
#                 try:
#                     feature_list = ast.literal_eval(item)
#                     all_features.extend(feature_list)
#                 except Exception:
#                     pass

#             text = " ".join(all_features)

#             wc = WordCloud(
#                 width=1200,
#                 height=600,
#                 background_color="white",
#                 colormap="viridis"
#             ).generate(text)

#             fig, ax = plt.subplots(figsize=(14, 7))
#             ax.imshow(wc)
#             ax.axis("off")

#             st.pyplot(fig)

#         # -------------------------------
#         # AREA VS PRICE DISTRIBUTION
#         # -------------------------------
#         with scatter_tab:
#             st.header("📈 Area vs Price Analysis")
#             st.caption("Relationship between Built-up Area and Property Price")

#             col1, col2 = st.columns(2)

#             with col1:
#                 property_type = st.selectbox(
#                     "Property Type",
#                     ["All"] + sorted(analytics_df["property_type"].unique())
#                 )

#             with col2:
#                 bedrooms = st.selectbox(
#                     "Bedrooms",
#                     ["All"] + sorted(analytics_df["bedRoom"].unique().tolist())
#                 )

#             filtered = analytics_df.copy()

#             if property_type != "All":
#                 filtered = filtered[filtered["property_type"] == property_type]

#             if bedrooms != "All":
#                 filtered = filtered[filtered["bedRoom"] == bedrooms]

#             fig = px.scatter(
#                 filtered,
#                 x="built_up_area",
#                 y="price",
#                 color="property_type",
#                 size="bedRoom",
#                 hover_name="sector",
#                 hover_data={
#                     "built_up_area": True,
#                     "price": ":.2f",
#                     "bedRoom": True
#                 },
#                 height=650
#             )

#             fig.update_layout(
#                 template="plotly_dark",
#                 xaxis_title="Built-up Area (sq ft)",
#                 yaxis_title="Price (Crore ₹)",
#                 title="Area vs Property Price",
#                 legend_title="Property Type"
#             )

#             st.plotly_chart(fig, width="stretch")

#         # -------------------------------
#         # BHK DISTRIBUTION
#         # -------------------------------
#         with pie_tab:
#             st.header("🛏 Bedroom Distribution")

#             # ======================================
#             # FILTER
#             # ======================================
#             selected_sector_pie = st.selectbox(
#                 "📍 Select Sector",
#                 ["All"] + sorted(analytics_df["sector"].unique()),
#                 key="pie_sector"
#             )

#             if selected_sector_pie == "All":
#                 pie_df = analytics_df.copy()
#             else:
#                 pie_df = analytics_df[analytics_df["sector"] == selected_sector_pie].copy()

#             if pie_df.empty:
#                 st.warning("No properties found for the selected sector.")
#                 st.stop()

#             # ======================================
#             # KPI CARDS
#             # ======================================
#             col1, col2, col3, col4 = st.columns(4)

#             col1.metric("🏆 Most Common", f"{pie_df['bedRoom'].mode()[0]} BHK")
#             col2.metric("🏠 Total Properties", len(pie_df))
#             col3.metric("📊 Avg Price", f"₹ {pie_df['price'].mean():.2f} Cr")
#             col4.metric("🔢 Bedroom Types", pie_df["bedRoom"].nunique())

#             st.divider()

#             # ======================================
#             # COUNT BEDROOMS
#             # ======================================
#             bhk_count = (
#                 pie_df["bedRoom"]
#                 .value_counts()
#                 .sort_index()
#                 .reset_index()
#             )
#             bhk_count.columns = ["Bedroom", "Count"]

#             # ======================================
#             # LAYOUT
#             # ======================================
#             left, right = st.columns([2, 1])

#             # ======================================
#             # PIE CHART
#             # ======================================
#             with left:
#                 fig = px.pie(
#                     bhk_count,
#                     names="Bedroom",
#                     values="Count",
#                     hole=0.55,
#                     color="Bedroom",
#                     color_discrete_sequence=px.colors.qualitative.Set3
#                 )

#                 fig.update_traces(
#                     textposition="inside",
#                     textinfo="percent+label",
#                     hovertemplate=(
#                         "<b>%{label} BHK</b><br>"
#                         "Properties : %{value}<br>"
#                         "Percentage : %{percent}<extra></extra>"
#                     )
#                 )

#                 fig.update_layout(
#                     title=f"Bedroom Distribution ({selected_sector_pie})",
#                     height=550,
#                     showlegend=True
#                 )

#                 st.plotly_chart(fig, width="stretch")

#             # ======================================
#             # BEDROOM STATS
#             # ======================================
#             with right:
#                 st.subheader("📋 BHK Summary")

#                 bhk_stats = (
#                     pie_df
#                     .groupby("bedRoom")
#                     .agg(
#                         Properties=("bedRoom", "count"),
#                         Avg_Price=("price", "mean")
#                     )
#                     .reset_index()
#                 )
#                 bhk_stats["Avg_Price"] = bhk_stats["Avg_Price"].round(2)

#                 st.dataframe(
#                     bhk_stats,
#                     hide_index=True,
#                     width="stretch",
#                     height=350
#                 )

#                 st.divider()

#                 st.subheader("🏆 Most Popular")

#                 top = bhk_stats.sort_values("Properties", ascending=False).iloc[0]

#                 st.success(
#                     f"""
#                     **{int(top['bedRoom'])} BHK**

#                     {int(top['Properties'])} Properties

#                     Avg Price

#                     ₹ {top['Avg_Price']:.2f} Cr
#                     """
#                 )

#         # -------------------------------
#         # BEDROOM BOX PLOT
#         # -------------------------------
#         with box_tab:
#             st.header("📦 Bedroom Price Analysis")
#             st.caption("Distribution of property prices across different bedroom categories.")

#             selected_sector_box = st.selectbox(
#                 "📍 Select Sector",
#                 ["All"] + sorted(analytics_df["sector"].unique()),
#                 key="box_sector"
#             )

#             if selected_sector_box == "All":
#                 box_df = analytics_df.copy()
#             else:
#                 box_df = analytics_df[analytics_df["sector"] == selected_sector_box].copy()

#             if box_df.empty:
#                 st.warning("No properties found.")
#                 st.stop()

#             col1, col2, col3 = st.columns(3)

#             col1.metric("🏠 Total Properties", len(box_df))
#             col2.metric("📊 Average Price", f"₹ {box_df['price'].mean():.2f} Cr")
#             col3.metric("🛏 Bedroom Types", box_df["bedRoom"].nunique())

#             st.divider()

#             fig = px.box(
#                 box_df,
#                 x="bedRoom",
#                 y="price",
#                 color="bedRoom",
#                 points="outliers",
#                 color_discrete_sequence=px.colors.qualitative.Set3
#             )

#             fig.update_layout(
#                 title="Bedroom vs Property Price",
#                 xaxis_title="Bedrooms",
#                 yaxis_title="Price (Crore ₹)",
#                 height=650
#             )

#             fig.update_traces(
#                 hovertemplate=(
#                     "<b>%{x} BHK</b><br>"
#                     "Price : ₹ %{y:.2f} Cr<extra></extra>"
#                 )
#             )

#             st.plotly_chart(fig, width="stretch")

#             st.subheader("📋 Price Summary")

#             summary = (
#                 box_df
#                 .groupby("bedRoom")
#                 .agg(
#                     Minimum=("price", "min"),
#                     Median=("price", "median"),
#                     Average=("price", "mean"),
#                     Maximum=("price", "max")
#                 )
#                 .round(2)
#                 .reset_index()
#             )

#             st.dataframe(summary, width="stretch", hide_index=True)

#         # -------------------------------
#         # PROPERTY TYPE / PRICE HISTOGRAM
#         # -------------------------------
#         with property_tab:
#             st.header("📊 Price Distribution Analysis")

#             # ======================================
#             # FILTER
#             # ======================================
#             selected_sector_hist = st.selectbox(
#                 "📍 Select Sector",
#                 ["All"] + sorted(analytics_df["sector"].unique()),
#                 key="hist_sector"
#             )

#             if selected_sector_hist == "All":
#                 hist_df = analytics_df.copy()
#             else:
#                 hist_df = analytics_df[analytics_df["sector"] == selected_sector_hist].copy()

#             if hist_df.empty:
#                 st.warning("No properties found.")
#                 st.stop()

#             # ======================================
#             # KPI CARDS
#             # ======================================
#             c1, c2, c3, c4 = st.columns(4)

#             c1.metric("Average Price", f"₹ {hist_df['price'].mean():.2f} Cr")
#             c2.metric("Median Price", f"₹ {hist_df['price'].median():.2f} Cr")
#             c3.metric("Maximum Price", f"₹ {hist_df['price'].max():.2f} Cr")
#             c4.metric("Properties", len(hist_df))

#             st.divider()

#             # ======================================
#             # HISTOGRAM
#             # ======================================
#             fig = px.histogram(
#                 hist_df,
#                 x="price",
#                 nbins=40,
#                 marginal="box",
#                 opacity=0.8,
#                 color_discrete_sequence=["#4F46E5"]
#             )

#             fig.update_layout(
#                 title="Property Price Distribution",
#                 xaxis_title="Price (Crore ₹)",
#                 yaxis_title="Number of Properties",
#                 height=600
#             )

#             st.plotly_chart(fig, width="stretch")

#             # ======================================
#             # SUMMARY TABLE
#             # ======================================
#             st.subheader("📋 Statistical Summary")

#             summary = hist_df["price"].describe().round(2)

#             st.dataframe(
#                 summary.to_frame().T,
#                 width="stretch",
#                 hide_index=True
#             )

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast


# ==========================================================
# COLUMN ALIASES
# ==========================================================
# For every "logical" field the dashboard needs, list every
# column name you've seen across different city CSVs.
# Add more aliases here as you onboard new cities — you should
# never need to touch the rest of the file again.
# ==========================================================
COLUMN_ALIASES = {
    "price":          ["price", "Price", "price_cr", "PriceCr", "price_in_cr"],
    "sector":         ["sector", "Sector", "locality", "Locality", "area_name",
                        "location", "Location", "neighborhood"],
    "latitude":       ["latitude", "Latitude", "lat", "Lat"],
    "longitude":      ["longitude", "Longitude", "lon", "lng", "Long"],
    "property_type":  ["property_type", "flat_type", "PropertyType", "type",
                        "Type", "property_category"],
    "bedRoom":        ["bedRoom", "bedrooms", "Bedrooms", "bhk", "BHK",
                        "no_of_bedrooms", "bedroom_num"],
    "built_up_area":  ["built_up_area", "area_sqft", "area", "Area",
                        "built_up_area_sqft", "carpet_area", "super_area"],
    "features":       ["features", "amenities", "Features", "Amenities"],
    "builder_name":   ["builder_name", "company_name", "developer", "builder"],
}


def resolve_columns(df, aliases=COLUMN_ALIASES):
    """
    For each logical field, find the first matching column that actually
    exists in this dataframe. Returns a dict like {"price": "price_cr", ...}.
    Fields that aren't found map to None so callers can check for that.
    """
    resolved = {}
    df_columns = list(df.columns)
    lower_lookup = {c.lower(): c for c in df_columns}

    for logical_name, candidates in aliases.items():
        found = None
        for candidate in candidates:
            if candidate in df_columns:
                found = candidate
                break
            if candidate.lower() in lower_lookup:
                found = lower_lookup[candidate.lower()]
                break
        resolved[logical_name] = found

    return resolved


def missing_columns_notice(tab_label, needed_keys, cols):
    """Show a friendly message when a tab can't render for this city's data."""
    missing = [k for k in needed_keys if not cols.get(k)]
    if missing:
        st.info(
            f"📭 **{tab_label}** isn't available for this city's dataset — "
            f"missing column(s): {', '.join(missing)}."
        )
        return True
    return False


def analytics_page(analytics_df, wordcloud_df, city):

    st.title(f"🌍 {city} Analytics Dashboard")

    # ======================================================
    # RESOLVE COLUMNS ONCE UP FRONT
    # ======================================================
    cols = resolve_columns(analytics_df)
    wc_cols = resolve_columns(wordcloud_df) if wordcloud_df is not None else {}

    PRICE = cols.get("price")
    SECTOR = cols.get("sector")
    LAT = cols.get("latitude")
    LON = cols.get("longitude")
    PTYPE = cols.get("property_type")
    BEDROOM = cols.get("bedRoom")
    AREA = cols.get("built_up_area")

    # Human-friendly label for whichever column actually matched (e.g. a
    # Mumbai CSV using "location" should say "Location" in the UI, not
    # "Sector" just because that's what Gurgaon happened to call it).
    SECTOR_LABEL = SECTOR.replace("_", " ").title() if SECTOR else "Sector"

    geo_tab, wordcloud_tab, scatter_tab, pie_tab, box_tab, property_tab = st.tabs([
        "🗺️ Geo Map",
        "☁️ Word Cloud",
        "📈 Area vs Price",
        "🥧 BHK Distribution",
        "📦 Bedroom Price",
        "📊 Property Type",
    ])

    # -------------------------------
    # GEO MAP
    # -------------------------------
    with geo_tab:
        if missing_columns_notice("Geo Map", ["price", "sector", "latitude", "longitude"], cols):
            pass
        else:
            # ======================================================
            # KPI CARDS
            # ======================================================
            avg_price = analytics_df[PRICE].mean()
            max_price = analytics_df[PRICE].max()
            min_price = analytics_df[PRICE].min()
            total_sectors = analytics_df[SECTOR].nunique()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🏠 Avg Price", f"₹ {avg_price:.1f} Cr")
            col2.metric("📈 Highest", f"₹ {max_price:.1f} Cr")
            col3.metric("📉 Lowest", f"₹ {min_price:.3f} Cr")
            col4.metric(f"📍 {SECTOR_LABEL}s", total_sectors)

            st.divider()

            # ======================================================
            # LAYOUT
            # ======================================================
            left, right = st.columns([1, 3])

            # ======================================================
            # FILTERS
            # ======================================================
            with left:
                st.subheader("🎛️ Filters")

                selected_sector = st.selectbox(
                    SECTOR_LABEL,
                    ["All"] + sorted(analytics_df[SECTOR].dropna().unique()),
                    key="geo_sector"
                )

                price_range = st.slider(
                    "Price Range (Cr)",
                    min_value=float(analytics_df[PRICE].min()),
                    max_value=float(analytics_df[PRICE].max()),
                    value=(
                        float(analytics_df[PRICE].min()),
                        float(analytics_df[PRICE].max())
                    )
                )

            # ======================================================
            # APPLY FILTERS
            # ======================================================
            filtered_df = analytics_df.copy()

            if selected_sector != "All":
                filtered_df = filtered_df[filtered_df[SECTOR] == selected_sector]

            filtered_df = filtered_df[
                (filtered_df[PRICE] >= price_range[0]) &
                (filtered_df[PRICE] <= price_range[1])
            ]

            # ======================================================
            # CREATE MAP DATA
            # ======================================================
            map_df = (
                filtered_df
                .groupby(SECTOR, as_index=False)
                .agg({
                    PRICE: "mean",
                    LAT: "first",
                    LON: "first"
                })
            )

            # ======================================================
            # RIGHT PANEL
            # ======================================================
            with right:
                st.subheader(f"🗺️ {city} Property Price Map")

                if map_df.empty:
                    st.warning("No properties found for the selected filters.")
                else:
                    fig = go.Figure()

                    fig.add_trace(
                        go.Scattermapbox(
                            lat=map_df[LAT],
                            lon=map_df[LON],
                            mode="markers",
                            text=map_df[SECTOR],
                            customdata=map_df[[PRICE]],
                            marker=dict(
                                size=18,
                                color=map_df[PRICE],
                                colorscale="Turbo",
                                showscale=True,
                                opacity=0.85,
                                colorbar=dict(title="Avg Price (Cr)")
                            ),
                            hovertemplate=(
                                "<b>%{text}</b><br><br>"
                                "Average Price : ₹ %{customdata[0]:.2f} Cr"
                                "<extra></extra>"
                            )
                        )
                    )

                    fig.update_layout(
                        mapbox=dict(
                            style="carto-positron",
                            center=dict(
                                lat=float(map_df[LAT].mean()),
                                lon=float(map_df[LON].mean())
                            ),
                            zoom=10
                        ),
                        height=550,
                        margin=dict(l=0, r=0, t=0, b=0)
                    )

                    st.plotly_chart(fig, width="stretch")

    # -------------------------------
    # WORD CLOUD
    # -------------------------------
    with wordcloud_tab:
        st.header("☁️ Amenities Word Cloud")

        wc_sector = wc_cols.get("sector")
        wc_features = wc_cols.get("features")
        wc_sector_label = wc_sector.replace("_", " ").title() if wc_sector else "Sector"

        if wordcloud_df is None or missing_columns_notice(
            "Word Cloud", ["sector", "features"], wc_cols
        ):
            pass
        else:
            selected_sector = st.selectbox(
                f"Select {wc_sector_label}",
                ["All"] + sorted(wordcloud_df[wc_sector].dropna().unique()),
                key="wc_sector"
            )

            filtered_df = wordcloud_df.copy()

            if selected_sector != "All":
                filtered_df = filtered_df[filtered_df[wc_sector] == selected_sector]

            all_features = []
            for item in filtered_df[wc_features]:
                try:
                    feature_list = ast.literal_eval(item)
                    all_features.extend(feature_list)
                except Exception:
                    pass

            text = " ".join(all_features)

            if not text.strip():
                st.warning("No amenity data available for the selected sector.")
            else:
                wc = WordCloud(
                    width=1200,
                    height=600,
                    background_color="white",
                    colormap="viridis"
                ).generate(text)

                fig, ax = plt.subplots(figsize=(14, 7))
                ax.imshow(wc)
                ax.axis("off")

                st.pyplot(fig)

    # -------------------------------
    # AREA VS PRICE DISTRIBUTION
    # -------------------------------
    with scatter_tab:
        st.header("📈 Area vs Price Analysis")
        st.caption("Relationship between Built-up Area and Property Price")

        if missing_columns_notice(
            "Area vs Price", ["price", "built_up_area"], cols
        ):
            pass
        else:
            col1, col2 = st.columns(2)

            with col1:
                if PTYPE:
                    property_type = st.selectbox(
                        "Property Type",
                        ["All"] + sorted(analytics_df[PTYPE].dropna().unique()),
                        key="scatter_ptype"
                    )
                else:
                    property_type = "All"
                    st.caption("Property type column not available for this city.")

            with col2:
                if BEDROOM:
                    bedrooms = st.selectbox(
                        "Bedrooms",
                        ["All"] + sorted(analytics_df[BEDROOM].dropna().unique().tolist()),
                        key="scatter_bedroom"
                    )
                else:
                    bedrooms = "All"
                    st.caption("Bedroom column not available for this city.")

            filtered = analytics_df.copy()

            if PTYPE and property_type != "All":
                filtered = filtered[filtered[PTYPE] == property_type]

            if BEDROOM and bedrooms != "All":
                filtered = filtered[filtered[BEDROOM] == bedrooms]

            scatter_kwargs = dict(
                x=AREA,
                y=PRICE,
                hover_name=SECTOR if SECTOR else None,
                height=650
            )
            if PTYPE:
                scatter_kwargs["color"] = PTYPE
            if BEDROOM:
                scatter_kwargs["size"] = BEDROOM

            fig = px.scatter(filtered, **scatter_kwargs)

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Built-up Area (sq ft)",
                yaxis_title="Price (Crore ₹)",
                title="Area vs Property Price",
                legend_title=PTYPE if PTYPE else ""
            )

            st.plotly_chart(fig, width="stretch")

    # -------------------------------
    # BHK DISTRIBUTION
    # -------------------------------
    with pie_tab:
        st.header("🛏 Bedroom Distribution")

        if missing_columns_notice("Bedroom Distribution", ["bedRoom", "price"], cols):
            pass
        else:
            selected_sector_pie = "All"
            if SECTOR:
                selected_sector_pie = st.selectbox(
                    f"📍 Select {SECTOR_LABEL}",
                    ["All"] + sorted(analytics_df[SECTOR].dropna().unique()),
                    key="pie_sector"
                )

            if SECTOR and selected_sector_pie != "All":
                pie_df = analytics_df[analytics_df[SECTOR] == selected_sector_pie].copy()
            else:
                pie_df = analytics_df.copy()

            if pie_df.empty:
                st.warning("No properties found for the selected sector.")
            else:
                # KPI CARDS
                col1, col2, col3, col4 = st.columns(4)

                col1.metric("🏆 Most Common", f"{pie_df[BEDROOM].mode()[0]} BHK")
                col2.metric("🏠 Total Properties", len(pie_df))
                col3.metric("📊 Avg Price", f"₹ {pie_df[PRICE].mean():.2f} Cr")
                col4.metric("🔢 Bedroom Types", pie_df[BEDROOM].nunique())

                st.divider()

                bhk_count = (
                    pie_df[BEDROOM]
                    .value_counts()
                    .sort_index()
                    .reset_index()
                )
                bhk_count.columns = ["Bedroom", "Count"]

                left, right = st.columns([2, 1])

                with left:
                    fig = px.pie(
                        bhk_count,
                        names="Bedroom",
                        values="Count",
                        hole=0.55,
                        color="Bedroom",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )

                    fig.update_traces(
                        textposition="inside",
                        textinfo="percent+label",
                        hovertemplate=(
                            "<b>%{label} BHK</b><br>"
                            "Properties : %{value}<br>"
                            "Percentage : %{percent}<extra></extra>"
                        )
                    )

                    fig.update_layout(
                        title=f"Bedroom Distribution ({selected_sector_pie})",
                        height=550,
                        showlegend=True
                    )

                    st.plotly_chart(fig, width="stretch")

                with right:
                    st.subheader("📋 BHK Summary")

                    bhk_stats = (
                        pie_df
                        .groupby(BEDROOM)
                        .agg(
                            Properties=(BEDROOM, "count"),
                            Avg_Price=(PRICE, "mean")
                        )
                        .reset_index()
                    )
                    bhk_stats["Avg_Price"] = bhk_stats["Avg_Price"].round(2)

                    st.dataframe(
                        bhk_stats,
                        hide_index=True,
                        width="stretch",
                        height=350
                    )

                    st.divider()

                    st.subheader("🏆 Most Popular")

                    top = bhk_stats.sort_values("Properties", ascending=False).iloc[0]

                    st.success(
                        f"""
                        **{top[BEDROOM]} BHK**

                        {int(top['Properties'])} Properties

                        Avg Price

                        ₹ {top['Avg_Price']:.2f} Cr
                        """
                    )

    # -------------------------------
    # BEDROOM BOX PLOT
    # -------------------------------
    with box_tab:
        st.header("📦 Bedroom Price Analysis")
        st.caption("Distribution of property prices across different bedroom categories.")

        if missing_columns_notice("Bedroom Price Analysis", ["bedRoom", "price"], cols):
            pass
        else:
            selected_sector_box = "All"
            if SECTOR:
                selected_sector_box = st.selectbox(
                    f"📍 Select {SECTOR_LABEL}",
                    ["All"] + sorted(analytics_df[SECTOR].dropna().unique()),
                    key="box_sector"
                )

            if SECTOR and selected_sector_box != "All":
                box_df = analytics_df[analytics_df[SECTOR] == selected_sector_box].copy()
            else:
                box_df = analytics_df.copy()

            if box_df.empty:
                st.warning("No properties found.")
            else:
                col1, col2, col3 = st.columns(3)

                col1.metric("🏠 Total Properties", len(box_df))
                col2.metric("📊 Average Price", f"₹ {box_df[PRICE].mean():.2f} Cr")
                col3.metric("🛏 Bedroom Types", box_df[BEDROOM].nunique())

                st.divider()

                fig = px.box(
                    box_df,
                    x=BEDROOM,
                    y=PRICE,
                    color=BEDROOM,
                    points="outliers",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )

                fig.update_layout(
                    title="Bedroom vs Property Price",
                    xaxis_title="Bedrooms",
                    yaxis_title="Price (Crore ₹)",
                    height=650
                )

                fig.update_traces(
                    hovertemplate=(
                        "<b>%{x} BHK</b><br>"
                        "Price : ₹ %{y:.2f} Cr<extra></extra>"
                    )
                )

                st.plotly_chart(fig, width="stretch")

                st.subheader("📋 Price Summary")

                summary = (
                    box_df
                    .groupby(BEDROOM)
                    .agg(
                        Minimum=(PRICE, "min"),
                        Median=(PRICE, "median"),
                        Average=(PRICE, "mean"),
                        Maximum=(PRICE, "max")
                    )
                    .round(2)
                    .reset_index()
                )

                st.dataframe(summary, width="stretch", hide_index=True)

    # -------------------------------
    # PROPERTY TYPE / PRICE HISTOGRAM
    # -------------------------------
    with property_tab:
        st.header("📊 Price Distribution Analysis")

        if missing_columns_notice("Price Distribution", ["price"], cols):
            pass
        else:
            selected_sector_hist = "All"
            if SECTOR:
                selected_sector_hist = st.selectbox(
                    f"📍 Select {SECTOR_LABEL}",
                    ["All"] + sorted(analytics_df[SECTOR].dropna().unique()),
                    key="hist_sector"
                )

            if SECTOR and selected_sector_hist != "All":
                hist_df = analytics_df[analytics_df[SECTOR] == selected_sector_hist].copy()
            else:
                hist_df = analytics_df.copy()

            if hist_df.empty:
                st.warning("No properties found.")
            else:
                c1, c2, c3, c4 = st.columns(4)

                c1.metric("Average Price", f"₹ {hist_df[PRICE].mean():.2f} Cr")
                c2.metric("Median Price", f"₹ {hist_df[PRICE].median():.2f} Cr")
                c3.metric("Maximum Price", f"₹ {hist_df[PRICE].max():.2f} Cr")
                c4.metric("Properties", len(hist_df))

                st.divider()

                fig = px.histogram(
                    hist_df,
                    x=PRICE,
                    nbins=40,
                    marginal="box",
                    opacity=0.8,
                    color_discrete_sequence=["#4F46E5"]
                )

                fig.update_layout(
                    title="Property Price Distribution",
                    xaxis_title="Price (Crore ₹)",
                    yaxis_title="Number of Properties",
                    height=600
                )

                st.plotly_chart(fig, width="stretch")

                st.subheader("📋 Statistical Summary")

                summary = hist_df[PRICE].describe().round(2)

                st.dataframe(
                    summary.to_frame().T,
                    width="stretch",
                    hide_index=True
                )