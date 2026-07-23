import streamlit as st
import pandas as pd


def recommendation_page(
        recommend_df,
        similarity
):

    st.title("🎯 Property Recommendation")

    property_name = st.selectbox(

        "Select Property",

        sorted(
            recommend_df["property_name"].unique()
        )

    )


    if st.button("Recommend Similar Properties"):

        index = recommend_df[
            recommend_df["property_name"] == property_name
        ].index[0]

        distances = list(
            enumerate(similarity[index])
        )

        distances = sorted(

            distances,

            reverse=True,

            key=lambda x:x[1]

        )[1:6]


        for i, score in distances:

            property = recommend_df.iloc[i]

            with st.container():

                st.subheader(
                    property["property_name"]
                )

                st.write(
                    f"⭐ Match Score : {score*100:.2f}%"
                )

                st.write(
                    f"💰 Average Price : ₹ {property['avg_price']:.2f} Cr"
                )

                st.write(
                    "🏊 Amenities"
                )

                st.write(
                    ", ".join(
                        property["facilities"][:5]
                    )
                )

                st.write(
                    "📍 Nearby"
                )

                st.write(
                    ", ".join(
                        property["nearby"][:5]
                    )
                )

                st.write(
                    "🛏 Configurations"
                )

                st.write(
                    ", ".join(
                        property["price_details"].keys()
                    )
                )

                st.link_button(

                    "View Property",

                    property["link"]

                )

                st.divider()