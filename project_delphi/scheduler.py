from project_delphi.streamlit_data import get_streamlit_data
from project_delphi.features import get_features, load_and_clean_csv
from project_delphi.merge_database import merge_daily_to_master
from project_delphi.twitter_api_data import get_data
from project_delphi.sentiment_analyzer import get_sentiment
import pandas as pd
# from features.py import clean_database
# run every day after midnight

def run_app(start_time, end_time):
    """
    1. Collects all tweets for the last day for every party and stores in raw_tweets
    2. Analyzes sentiment of daily_tweets and saves in daily_database
    3. download old tweet database, concats new daily database, uploads it to gcs and saves it in tweet_database
    """


    #daily_raw_tweets = get_data(start_time, end_time)

    #daily_database = get_sentiment(daily_raw_tweets)

    # daily_database = load_and_clean_csv(daily_database)

    #tweet_database = merge_daily_to_master(daily_database)

    tweet_database = pd.read_csv("~/Downloads/temp_tweet_database_08_31.csv",
                                 lineterminator="\n")
    tweet_database = load_and_clean_csv(tweet_database)
    features_database = get_features(tweet_database)
    print(features_database.columns)

    get_streamlit_data(
        features_database,
        tweet_database
    )


    # website_features = get_streamlit_data(tweet_database)

    # prediction = run_model(feature_database)
