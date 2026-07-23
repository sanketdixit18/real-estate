# import streamlit as st
# import pandas as pd
# import numpy as np

# def prediction_page(df, pipeline):
    
#         st.header("House Price Prediction")
#         # Prediction form here
#         st.header("Enter your inputs")
#         #property types
#         # property_type=st.selectbox('Property Type',['Flat','House'])
#         property_type = st.selectbox(
#             "Property Type",
#             sorted(df['property_type'].unique().tolist())
#         )
#         sector = st.selectbox(
#             'Sector',
#             sorted(df['sector'].unique().tolist())
#         )

#         bedrooms = st.selectbox(
#             'Bedrooms',
#             sorted(df['bedRoom'].unique().tolist())
#         )

#         bathroom = st.selectbox(
#             'Bathrooms',
#             sorted(df['bathroom'].unique().tolist())
#         )

#         balcony = st.selectbox(
#             'Balconies',
#             sorted(df['balcony'].unique().tolist())
#         )

#         property_age = st.selectbox(
#             'Property Age',
#             sorted(df['agePossession'].unique().tolist())
#         )

#         built_up_area = st.number_input(
#             'Built Up Area (sq ft)',
#             min_value=100,
#             step=50
#         )

#         servant_room = st.selectbox(
#             'Servant Room',
#             [0.0,1.0]
#         )

#         store_room = st.selectbox(
#             'Store Room',
#             [0.0,1.0]
#         )

#         furnishing_type = st.selectbox(
#             'Furnishing',
#             sorted(df['furnishing_type'].unique())
#         )

#         luxury_category = st.selectbox(
#             'Luxury Category',
#             sorted(df['luxury_category'].unique())
#         )

#         floor_category = st.selectbox(
#             'Floor Category',
#             sorted(df['floor_category'].unique())
#         )

#         # -------------------------------
#         # Prediction
#         # -------------------------------

#         if st.button("🔮 Predict Price"):

#             # Create input dataframe
#             data = [[
#                 property_type,
#                 sector,
#                 bedrooms,
#                 bathroom,
#                 balcony,
#                 property_age,
#                 built_up_area,
#                 servant_room,
#                 store_room,
#                 furnishing_type,
#                 luxury_category,
#                 floor_category
#             ]]

#             columns = [
#                 'property_type',
#                 'sector',
#                 'bedRoom',
#                 'bathroom',
#                 'balcony',
#                 'agePossession',
#                 'built_up_area',
#                 'servant room',
#                 'store room',
#                 'furnishing_type',
#                 'luxury_category',
#                 'floor_category'
#             ]

#             input_df = pd.DataFrame(data, columns=columns)

#             # Make prediction
#             prediction = pipeline.predict(input_df)

#             # Convert back from log scale
#             predicted_price = np.expm1(prediction)[0]

#             # Confidence Range (Approx.)
#             error_margin = 0.22          # You can replace this with RMSE later
#             lower_price = predicted_price - error_margin
#             upper_price = predicted_price + error_margin

#             # Prevent negative values
#             lower_price = max(lower_price, 0)

#             st.divider()

#             st.success("✅ Prediction Generated Successfully")

#             # Display Metrics
#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 st.metric(
#                     label="📉 Lower Estimate",
#                     value=f"₹ {lower_price:.2f} Cr"
#                 )

#             with col2:
#                 st.metric(
#                     label="🏠 Predicted Price",
#                     value=f"₹ {predicted_price:.2f} Cr"
#                 )

#             with col3:
#                 st.metric(
#                     label="📈 Upper Estimate",
#                     value=f"₹ {upper_price:.2f} Cr"
#                 )

#             st.info(
#                 f"""
#         ### Estimated Price Range

#         🏠 **Your property is estimated to be worth between**

#         ## ₹ {lower_price:.2f} Crore — ₹ {upper_price:.2f} Crore

#         The estimated market value based on the selected property features is:

#         ### **₹ {predicted_price:.2f} Crore**
#         """
#             )

#             # Optional: Show input summary
#             with st.expander("📋 View Property Details"):

#                 st.dataframe(
#                     input_df,
#                     width="stretch",
#                     hide_index=True
#                 )

# import streamlit as st
# import pandas as pd
# import numpy as np


# def prediction_page(df, pipeline, city):

#     st.header("🏠 House Price Prediction")

#     city = city.lower()


#     if city == "gurgaon":

#         gurgaon_prediction(df, pipeline)


#     elif city == "mumbai":

#         mumbai_prediction(df, pipeline)




# # --------------------------------------------------
# # Gurgaon Prediction
# # --------------------------------------------------

# def gurgaon_prediction(df, pipeline):

#     st.subheader("Enter Gurgaon Property Details")


#     property_type = st.selectbox(
#         "Property Type",
#         sorted(df['property_type'].unique())
#     )


#     sector = st.selectbox(
#         "Sector",
#         sorted(df['sector'].unique())
#     )


#     bedroom = st.selectbox(
#         "Bedrooms",
#         sorted(df['bedRoom'].unique())
#     )


#     bathroom = st.selectbox(
#         "Bathrooms",
#         sorted(df['bathroom'].unique())
#     )


#     balcony = st.selectbox(
#         "Balcony",
#         sorted(df['balcony'].unique())
#     )


#     age = st.selectbox(
#         "Property Age",
#         sorted(df['agePossession'].unique())
#     )


#     built_up_area = st.number_input(
#         "Built Up Area (sqft)",
#         min_value=100,
#         step=50
#     )


#     servant_room = st.selectbox(
#         "Servant Room",
#         [0,1]
#     )


#     store_room = st.selectbox(
#         "Store Room",
#         [0,1]
#     )


#     furnishing = st.selectbox(
#         "Furnishing",
#         sorted(df['furnishing_type'].unique())
#     )


#     luxury = st.selectbox(
#         "Luxury Category",
#         sorted(df['luxury_category'].unique())
#     )


#     floor = st.selectbox(
#         "Floor Category",
#         sorted(df['floor_category'].unique())
#     )



#     if st.button("🔮 Predict Price"):


#         input_df = pd.DataFrame(
#             [[
#                 property_type,
#                 sector,
#                 bedroom,
#                 bathroom,
#                 balcony,
#                 age,
#                 built_up_area,
#                 servant_room,
#                 store_room,
#                 furnishing,
#                 luxury,
#                 floor
#             ]],
#             columns=[
#                 'property_type',
#                 'sector',
#                 'bedRoom',
#                 'bathroom',
#                 'balcony',
#                 'agePossession',
#                 'built_up_area',
#                 'servant room',
#                 'store room',
#                 'furnishing_type',
#                 'luxury_category',
#                 'floor_category'
#             ]
#         )


#         make_prediction(
#             pipeline,
#             input_df
#         )





# # --------------------------------------------------
# # Mumbai Prediction
# # --------------------------------------------------

# def mumbai_prediction(df, pipeline):

#     st.subheader("Enter Mumbai Property Details")



#     area = st.number_input(
#         "Area (sqft)",
#         min_value=100,
#         step=50
#     )


#     locality = st.selectbox(
#         "Locality",
#         sorted(df['locality'].unique())
#     )


#     property_type = st.selectbox(
#         "Property Type",
#         sorted(df['property_type'].unique())
#     )


#     bedroom = st.selectbox(
#         "Bedrooms",
#         sorted(df['bedroom_num'].unique())
#     )


#     bathroom = st.selectbox(
#         "Bathrooms",
#         sorted(df['bathroom_num'].unique())
#     )


#     balcony = st.selectbox(
#         "Balcony",
#         sorted(df['balcony_num'].unique())
#     )


#     furnished = st.selectbox(
#         "Furnished",
#         sorted(df['furnished'].unique())
#     )


#     age = st.selectbox(
#         "Property Age",
#         sorted(df['age'].unique())
#     )



#     if st.button("🔮 Predict Price"):


#         input_df = pd.DataFrame(
#             [[
#                 area,
#                 locality,
#                 property_type,
#                 bedroom,
#                 bathroom,
#                 balcony,
#                 furnished,
#                 age
#             ]],
#             columns=[
#                 'area',
#                 'locality',
#                 'property_type',
#                 'bedroom_num',
#                 'bathroom_num',
#                 'balcony_num',
#                 'furnished',
#                 'age'
#             ]
#         )


#         make_prediction(
#             pipeline,
#             input_df
#         )





# # --------------------------------------------------
# # Common Prediction Function
# # --------------------------------------------------

def make_prediction(pipeline, input_df):


    prediction = pipeline.predict(
        input_df
    )


    predicted_price = np.expm1(
        prediction
    )[0]


    # Error margin
    error_margin = predicted_price * 0.05


    lower_price = max(
        predicted_price - error_margin,
        0
    )


    upper_price = predicted_price + error_margin



    st.divider()


    st.success(
        "✅ Prediction Generated Successfully"
    )


    col1,col2,col3 = st.columns(3)


    with col1:

        st.metric(
            "📉 Lower Estimate",
            f"₹ {lower_price:.2f} Cr"
        )


    with col2:

        st.metric(
            "🏠 Predicted Price",
            f"₹ {predicted_price:.2f} Cr"
        )


    with col3:

        st.metric(
            "📈 Upper Estimate",
            f"₹ {upper_price:.2f} Cr"
        )



    st.info(
        f"""
        ## Estimated Property Value

        Your property price is approximately:

        # ₹ {predicted_price:.2f} Crore

        Expected range:

        ₹ {lower_price:.2f} Cr - ₹ {upper_price:.2f} Cr
        """
    )


    with st.expander(
        "📋 View Property Details"
    ):

        st.dataframe(
            input_df,
            hide_index=True
        )


import streamlit as st
import pandas as pd
import numpy as np

from utils.city_config import CITY_CONFIG



def prediction_page(df,pipeline,city):


    city = city.lower()


    config = CITY_CONFIG[city]


    st.header("🏠 House Price Prediction")


    user_input = {}



    for feature, details in config["inputs"].items():


        input_type = details["type"]



        if input_type=="select":


            user_input[feature] = st.selectbox(

                feature.replace("_"," ").title(),

                sorted(
                    df[feature].dropna().unique()
                )

            )


        elif input_type=="number":


            user_input[feature] = st.number_input(

                feature.replace("_"," ").title(),

                min_value=100,
                step=50

            )



    if st.button("🔮 Predict Price"):


        input_df = pd.DataFrame(
            [user_input]
        )
        make_prediction(
                pipeline,
                input_df
            )