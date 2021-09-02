from project_delphi.model import rnn_model_predict
from project_delphi.streamlit_data import get_streamlit_data
from project_delphi.features import get_features, load_and_clean_csv
from project_delphi.merge_database import merge_daily_to_master
from project_delphi.twitter_api_data import get_data
from project_delphi.sentiment_analyzer import get_sentiment
import pandas as pd
import datetime

def run_app(start_time, end_time):
    """
    1. Collects all tweets for the last day for every party and stores in raw_tweets
    2. Analyzes sentiment of daily_tweets and saves in daily_database
    4. Clean daily data to only get columns we want
    4. Download old tweet database, concats new daily database, uploads it to gcs and saves it in tweet_database
    5. Engineer features from tweet database and fetch poll data.
       Return everything in one double grouped dataframe by date and the seven parties
    6. Collect data for streamlit website and upload it to gcp
    7. Run model with all data and upload prediction to gcp
    """
    #print(f"----- STARTING AT {datetime.datetime.today()} -----")

    #daily_raw_tweets = get_data(start_time, end_time)
    #print(f"----- 1. FINISHED AT {datetime.datetime.today()} -----")
    #print(f"Fetched {len(daily_raw_tweets)} tweets from yesterday")

    #daily_database = get_sentiment(daily_raw_tweets)
    #print(f"----- 2. FINISHED AT {datetime.datetime.today()} -----")
    tweet_database = pd.read_csv(
        "/Users/nicolas/Downloads/tweets_tweet_database_2021_09_01.csv",
        lineterminator="\n")

    #daily_database = load_and_clean_csv(daily_database)
    #print(f"----- 3. FINISHED AT {datetime.datetime.today()} -----")

    #tweet_database = merge_daily_to_master(daily_database)
    #print(f"----- 4. FINISHED AT {datetime.datetime.today()} -----")

    features_database = get_features(tweet_database)
    print(f"----- 5. FINISHED AT {datetime.datetime.today()} -----")

    get_streamlit_data(
        features_database,
        tweet_database
    )
    print(f"----- 6. FINISHED AT {datetime.datetime.today()} -----")

    rnn_model_predict(features_database)
    print(f"----- 7. FINISHED AT {datetime.datetime.today()} -----")
