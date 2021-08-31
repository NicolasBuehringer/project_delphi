from project_delphi.merge_database import merge_daily_to_master
from project_delphi.twitter_api_data import get_data
from project_delphi.sentiment_analyzer import get_sentiment
# from features.py import clean_database
# run every day after midnight

def run_app(start_time, end_time):
    """
    1. Collects all tweets for the last day for every party and stores in raw_tweets
    2. Analyzes sentiment of daily_tweets and saves in daily_database
    3. download old tweet database, concats new daily database, uploads it to gcs and saves it in tweet_database
    """

    daily_raw_tweets = get_data(start_time, end_time)

    daily_database = get_sentiment(daily_raw_tweets)

    tweet_database = merge_daily_to_master(daily_database)

    # features_database = clean_database(tweet_database) --> Finn
    # get_features()
    # model = run_model(features_database)

    # update api
