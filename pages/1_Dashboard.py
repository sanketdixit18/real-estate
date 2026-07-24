# import streamlit as st

# from utils.loader import load_city
# from utils.prediction import prediction_page
# from utils.analytics import analytics_page
# from utils.recommendation import recommendation_page
# from utils.market_trends import market_trends_page

# # -------------------------
# # Select City
# # -------------------------

# st.sidebar.title("🏙 Select City")

# city = st.sidebar.selectbox(
#     "Choose City",
#     [
#         "Gurgaon",
#         "Mumbai"
#     ]
# )

# # -------------------------
# # Load Selected City
# # -------------------------

# (
#     df,
#     pipeline,
#     analytics_df,
#     wordcloud_df,
#     recommendation_df,
#     locality_df,
#     market_df,
#     recommend_df,
#     similarity
# ) = load_city(city)




# st.title(f"🏠 {city} Real Estate Dashboard")

# st.markdown(
#     f"Explore **{city}** Real Estate with Prediction, Analytics, Recommendation and Market Trends."
# )

# st.divider()


# # ==========================================
# # TABS
# # ==========================================

# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "🏠 Prediction",
#     "📊 Analysis",
#     "🎯 Recommendation",
#     "📈 Market Trends",
#     "🗺️ Locality Explorer"
# ])


# # ==========================================
# # PREDICTION
# # ==========================================

# with tab1:
#     prediction_page(
#         df,
#         pipeline,
#         city
#     )


# # ==========================================
# # ANALYTICS
# # ==========================================

# with tab2:
#     analytics_page(
#         analytics_df,
#         wordcloud_df
#     )


# # ==========================================
# # RECOMMENDATION
# # ==========================================

# with tab3:
#     recommendation_page(
#         recommend_df,
#         similarity
#     )


# # ==========================================
# # MARKET TRENDS
# # ==========================================

# with tab4:
#     market_trends_page(
#         market_df
#     )


# # ==========================================
# # LOCALITY EXPLORER
# # ==========================================

# with tab5:
#     st.info("Coming Soon...")


import streamlit as st


from utils.loader import (
    load_prediction,
    load_analytics,
    load_recommendation,
    load_market
)


from utils.prediction import prediction_page
from utils.analytics import analytics_page
from utils.recommendation import recommendation_page
from utils.market_trends import market_trends_page




st.sidebar.title(
    "🏙 Select City"
)



city = st.sidebar.selectbox(
    "Choose City",
    [
        "Gurgaon",
        "Mumbai"
    ]
)



city = city.lower()



# -------------------------
# Load Prediction
# -------------------------

df, pipeline = load_prediction(city)



# -------------------------
# Optional Modules
# -------------------------

# analytics_df, wordcloud_df = load_analytics(city)


# recommend_df, similarity = load_recommendation(city)


# market_df = load_market(city)





st.title(
    f"🏠 {city.title()} Real Estate"
)





tab1,tab2,tab3,tab4 = st.tabs(
[
"🏠 Prediction",
"📊 Analytics",
"🎯 Recommendation",
"📈 Market Trends"
]
)






with tab1:


    prediction_page(
        df,
        pipeline,
        city
    )







# with tab2:


#     if analytics_df is not None:

#         analytics_page(
#             analytics_df,
#             wordcloud_df,
#             city
#         )

#     else:

#         st.info(
#             f"Analytics not available for {city}"
#         )








# with tab3:


#     if recommend_df is not None:


#         recommendation_page(
#             recommend_df,
#             similarity
#         )


#     else:


#         st.info(
#             "Recommendation not available."
#         )







# with tab4:


#     if market_df is not None:


#         market_trends_page(
#             market_df
#         )


    # else:


    #     st.info(
    #         "Market trends not available."
    #     )
