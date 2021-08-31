from polls_data_clean import clean_data
from google.cloud import storage
from params import BUCKET_NAME
from utils import get_date_n_days_ago

import pandas as pd
import os


def poll_for_streamlit():

    #get poll data
    polls = clean_data()
    polls.drop(columns=["Surveyed_Persons"], inplace=True)
    polls.set_index("Date", inplace=True)

    # Return latest poll
    latest_poll = polls.iloc[[-1]]

    return polls, latest_poll


def tweet_kpis_for_streamlit(tweet_kpis):
    ''' Returns the most recent twitter kpis to display on streamlit '''

    # Get latest tweets date
    latest_tweet_date = tweet_kpis["tweet_date"].max()

    # Slice Dataframe for most recent Twitter KPIs
    tweet_kpis = tweet_kpis[tweet_kpis["tweet_date"] == latest_tweet_date]

    return tweet_kpis


def most_popular_tweets(df, tweet_date):
    ''' Find and return the most liked/ most retweeted positive and negative tweets overall and per party
    --> returns two df most_liked_tweets, most_retweeted_tweets '''

    #Create empty dataframe for most likes and most retweeted tweets
    most_liked_tweets = pd.DataFrame()
    most_retweeted_tweets = pd.DataFrame()

    # Create lists for iterations for party and sentiment
    parties = ['CDU', 'SPD', 'GRUENE', 'FDP', 'LINKE', 'AFD', 'OTHER']
    sentiments = [-2, 2]  #-2: negative, +2: positive

    #Columns to keep
    columns = [
        'username', 'text', 'tweet_date', 'retweet_count', 'reply_count', 'like_count',
        'sentiment', "party"
    ]
    #'username'

    #Only keep relevant columns of Twitter dataframe
    df = df[columns]

    #Change to datemtime
    df["tweet_date"] = pd.to_datetime(df["tweet_date"])

    #Change format of datetime to 2021-08-25
    df["tweet_date"] = df["tweet_date"].dt.strftime('%Y-%m-%d')

    # Filter df for day of tweet
    df = df[df["tweet_date"] == tweet_date]

    #Get most liked/ retweeted Tweets over all parties
    for sentiment in sentiments:

        #Filter for sentiment
        tweets_tmp = df[df["sentiment"] == sentiment].reset_index()

        # Find tweet with most likes and concatenate to final df
        most_liked_tweet = tweets_tmp.iloc[[tweets_tmp["like_count"].idxmax()]]
        most_liked_tweets = pd.concat([most_liked_tweets, most_liked_tweet],
                                      ignore_index=True)
        most_liked_tweets["party"] = "OVERALL"

        # Find tweet with most retweets and concatenate to final df
        most_retweeted_tweet = tweets_tmp.iloc[[
            tweets_tmp["retweet_count"].idxmax()
        ]]
        most_retweeted_tweets = pd.concat(
            [most_retweeted_tweets, most_retweeted_tweet], ignore_index=True)
        most_retweeted_tweets["party"] = "OVERALL"

    #Get most liked/ retweeted Tweets for each party
    for party in parties:

        tweets_party_df = df[df["party"] == party]

        #Find tweets with most likes & most retweets per party and concatenate them to the final dfs
        for sentiment in sentiments:

            #Filter for sentiment
            tweets_tmp = pd.DataFrame(tweets_party_df[
                tweets_party_df["sentiment"] == sentiment].reset_index())

            # Find tweet with most likes and concatenate to final df
            most_liked_tweet = tweets_tmp.iloc[[
                tweets_tmp["like_count"].idxmax()
            ]]
            most_liked_tweets = pd.concat(
                [most_liked_tweets, most_liked_tweet], ignore_index=True)

            # Find tweet with most retweets and concatenate to final df
            most_retweeted_tweet = tweets_tmp.iloc[[
                tweets_tmp["retweet_count"].idxmax()
            ]]
            most_retweeted_tweets = pd.concat(
                [most_retweeted_tweets, most_retweeted_tweet],
                ignore_index=True)

    return most_liked_tweets, most_retweeted_tweets


def upload_streamlit_data_to_gcp(df, filename, index=False):
    client = storage.Client()
    STORAGE_LOCATION = f"streamlit/{filename}.csv"
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(STORAGE_LOCATION)
    print(f"Start upload DataFrame to {STORAGE_LOCATION}")
    blob.upload_from_string(df.to_csv(index=index), 'text/csv')
    print("Upload completed")


def get_streamlit_data(feature_database, daily_database, days_ago=1):
    '''
    Takes in engineered features df and daily tweets + sentiment df
    and creates tables to be displayed on streamlit and uploads them to GCP
    1. Poll history and most recent poll
    2. Tweet KPIs history
    3. Most liked/ most retweeted positive and negative tweets
    '''

    # Save Poll data as .csv and upload to GCP
    polls, latest_poll = poll_for_streamlit()
    upload_streamlit_data_to_gcp(polls, "polls", index=True)
    upload_streamlit_data_to_gcp(latest_poll, "latest_poll", index=True)

    # Save Tweet Kpis as .csv and upload to GCP
    #test_kpi = pd.read_csv("raw_data/data_final_20210826_v1.csv")
    tweet_kpis = tweet_kpis_for_streamlit(feature_database)
    upload_streamlit_data_to_gcp(tweet_kpis, "tweet_kpis", index=False)

    # Save most liked/ most retweeted positive and negative tweets and upload to GCP
    #test = pd.read_csv("raw_data/df_all_v2.csv")
    tweet_date = get_date_n_days_ago(days_ago)
    tweet_date = tweet_date.replace("_", "-")

    #tweet_date = "2021-08-26"
    most_liked_tweets, most_retweeted_tweets = most_popular_tweets(
        daily_database, tweet_date)
    upload_streamlit_data_to_gcp(most_liked_tweets,
                                 "most_liked_tweets",
                                 index=False)
    upload_streamlit_data_to_gcp(most_retweeted_tweets,
                                 "most_retweeted_tweets",
                                 index=False)






if __name__ == "__main__":

    feature_database = pd.read_csv("raw_data/data_final_20210826_v1.csv")
    daily_database = pd.read_csv("raw_data/df_all_v2.csv")
    get_streamlit_data(feature_database, daily_database, days_ago=5)

    '''
    # Save Poll data as .csv for streamlit
    polls, latest_poll = poll_for_streamlit()
    upload_streamlit_data_to_gcp(polls, "polls", index=True)
    upload_streamlit_data_to_gcp(latest_poll, "latest_poll", index=True)

    # Save Tweet Kpis as .csv for streamlit
    test_kpi = pd.read_csv("raw_data/data_final_20210826_v1.csv")
    tweet_kpis = tweet_kpis_for_streamlit(test_kpi)
    upload_streamlit_data_to_gcp(tweet_kpis, "tweet_kpis", index=False)

    # Save most liked/ most retweeted positive and negative tweets
    test = pd.read_csv("raw_data/df_all_v2.csv")
    tweet_date = "2021-08-26"
    most_liked_tweets, most_retweeted_tweets = most_popular_tweets(test, tweet_date)
    upload_streamlit_data_to_gcp(most_liked_tweets,
                                 "most_liked_tweets",
                                 index=False)
    upload_streamlit_data_to_gcp(most_retweeted_tweets,
                                 "most_retweeted_tweets",
                                 index=False)
                                 '''
