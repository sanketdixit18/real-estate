




# import os
# import pickle
# import urllib.request
# import pandas as pd




# PIPELINE_URLS = {
#     "gurgaon": "https://github.com/sanketdixit18/Real-estate-app/releases/download/v1.0/pipeline.pkl"
# }

# def download_pipeline(city):
#     pipeline_path = f"model/{city}/pipeline.pkl"

#     # Already downloaded
#     if os.path.exists(pipeline_path):
#         return

#     os.makedirs(os.path.dirname(pipeline_path), exist_ok=True)

#     print(f"Downloading pipeline for {city}...")

#     try:
#         urllib.request.urlretrieve(
#             PIPELINE_URLS[city],
#             pipeline_path
#         )
#         print("Pipeline downloaded successfully.")

#     except Exception as e:
#         raise RuntimeError(f"Failed to download pipeline: {e}")

#     if not os.path.isfile(pipeline_path):
#         raise FileNotFoundError(
#             f"{pipeline_path} was not downloaded successfully."
#         )


# def load_city(city):

#     city = city.lower()

#     analytics_df = pd.read_csv(f"data/{city}/analytics.csv")
#     wordcloud_df = pd.read_csv(f"data/{city}/wordcloud.csv")
#     recommendation_df = pd.read_csv(f"data/{city}/recommendation.csv")
#     market_df = pd.read_csv(f"data/{city}/market_trends.csv")

#     locality_df = None

#     with open(f"model/{city}/df.pkl", "rb") as f:
#         df = pickle.load(f)

#     download_pipeline(city)

#     with open(f"model/{city}/pipeline.pkl", "rb") as f:
#         pipeline = pickle.load(f)

#     with open(f"model/{city}/recommend_df.pkl", "rb") as f:
#         recommend_df = pickle.load(f)

#     with open(f"model/{city}/hybrid_similarity.pkl", "rb") as f:
#         similarity = pickle.load(f)

#     return (
#         df,
#         pipeline,
#         analytics_df,
#         wordcloud_df,
#         recommendation_df,
#         locality_df,
#         market_df,
#         recommend_df,
#         similarity
#     )


import os
import pickle
import joblib
import urllib.request
import pandas as pd



PIPELINE_URLS = {

    "gurgaon":
    "https://github.com/sanketdixit18/Real-estate-app/releases/download/v1.0/pipeline.pkl",
    "mumbai":
    "https://github.com/sanketdixit18/Real-estate-app/releases/download/v1.1/pipeline.pkl",

}





def download_pipeline(city):

    path = f"model/{city}/pipeline.pkl"


    if os.path.exists(path):
        return


    if city not in PIPELINE_URLS:
        return


    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )


    urllib.request.urlretrieve(
        PIPELINE_URLS[city],
        path
    )






# -----------------------------
# Prediction Loader
# -----------------------------

def load_prediction(city):

    city = city.lower()


    df_path = f"model/{city}/df.pkl"


    pipeline_path = f"model/{city}/pipeline.pkl"



    if not os.path.exists(df_path):

        raise FileNotFoundError(
            f"{df_path} missing"
        )



    with open(
        df_path,
        "rb"
    ) as f:

        df = pickle.load(f)



    download_pipeline(city)



    pipeline = joblib.load(
        pipeline_path
    )


    return df, pipeline






# -----------------------------
# Analytics Loader
# -----------------------------

def load_analytics(city):

    city = city.lower()


    analytics_path = (
        f"data/{city}/analytics.csv"
    )

    # wordcloud_path = (
    #     f"data/{city}/wordcloud.csv"
    # )
    wordcloud_path = f"data/{city}/wordcloud.csv"

    if os.path.exists(wordcloud_path):
        wordcloud_df = pd.read_csv(wordcloud_path)
    else:
        wordcloud_df = None



    analytics_df = None
    wordcloud_df = None



    if os.path.exists(analytics_path):

        analytics_df = pd.read_csv(
            analytics_path
        )



    if os.path.exists(wordcloud_path):

        wordcloud_df = pd.read_csv(
            wordcloud_path
        )



    return analytics_df, wordcloud_df






# -----------------------------
# Recommendation Loader
# -----------------------------

def load_recommendation(city):

    city = city.lower()


    recommend_df = None
    similarity = None



    rec_path = (
        f"model/{city}/recommend_df.pkl"
    )

    sim_path = (
        f"model/{city}/hybrid_similarity.pkl"
    )



    if os.path.exists(rec_path):

        with open(
            rec_path,
            "rb"
        ) as f:

            recommend_df = pickle.load(f)



    if os.path.exists(sim_path):

        with open(
            sim_path,
            "rb"
        ) as f:

            similarity = pickle.load(f)



    return recommend_df, similarity






# -----------------------------
# Market Loader
# -----------------------------

def load_market(city):

    city = city.lower()


    path = (
        f"data/{city}/market_trends.csv"
    )


    if os.path.exists(path):

        return pd.read_csv(path)



    return None
