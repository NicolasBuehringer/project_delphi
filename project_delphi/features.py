# Imports
from os import link
import pandas as pd
import numpy as np
import datetime
from project_delphi.polls_data_clean import clean_data




def load_and_clean_csv(df):
    '''
    Function loads DF data from the Twitter API+Sentiment and returns a cleaned DF
    '''
    # rename columns
    df = df.rename(columns={"tweet_created_at": "tweet_date",
                                "public_metrics.retweet_count": "retweet_count",
                                "public_metrics.reply_count": "reply_count",
                                "public_metrics.like_count": "like_count",
                                "profile_created_at": "profile_creation_date",
                                "public_metrics.followers_count": "followers_count",
                                "public_metrics.following_count": "following_count",
                                "public_metrics.tweet_count": "user_tweet_count"
                                })

    # Including only columns that we want to use in the future
    df = df[['party',
                'tweet_date',
                'author_id',
                'tweet_id',
                'text',
                'source',
                'retweet_count',
                'reply_count',
                'like_count',
                'profile_creation_date',
                'followers_count',
                'following_count',
                'user_tweet_count',
                'location',
                'sentiment',
                'username'
                ]]

    # Clean dataset columns:
    # Change dtype
    df["tweet_date"] = df["tweet_date"].astype(str)
    df = df[df.tweet_date.str.match('(\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2})')]
    df = df[(df.tweet_date.str.len() == 23) | (df.tweet_date.str.len() == 24)]
    df['tweet_date'] = df['tweet_date'].str.slice(0,19)
    df["tweet_date"] = pd.to_datetime(df["tweet_date"])

    df["profile_creation_date"] = df["profile_creation_date"].astype(str)
    df = df[df.profile_creation_date.str.match(
        '(\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2})')]
    df['profile_creation_date'] = df['profile_creation_date'].str.slice(0,19)
    df["profile_creation_date"] = pd.to_datetime(df["profile_creation_date"])
    # Drop duplicates
    #df = df.drop_duplicates()
    # Transform sentiment to numeric type
    dict_to_numeric = {"negative": -2, "neutral": 1, "positive": 2}
    df["sentiment"].replace(dict_to_numeric, inplace=True)

    return df


    #def concat_dfs(cleaned_df):
    '''
    Function concatenates multiple dataframes into one DF
    '''
    #df_all = pd.concat(list_of_dfs)
    #df_all = df_all.reset_index(drop=True)
    #return df_all


def create_non_sentiment_features(df):

    # Create: "Len per tweet of each party"
    df["avg_len_of_tweet"] = df["text"].str.len()

    #Rename Columns
    df = df.rename(columns={"followers_count": "avg_followers_count",
                       "following_count": "avg_following_count",
                       "user_tweet_count": "avg_user_tweet_count"
                      })
    # Change dtypes
    df = df.fillna(0)
    df["reply_count"] = df["reply_count"].astype(float)
    df["retweet_count"] = df["retweet_count"].astype(float)
    df["like_count"] = df["like_count"].astype(float)
    df["avg_len_of_tweet"] = df["avg_len_of_tweet"].astype(float)
    df["avg_followers_count"] = df["avg_followers_count"].astype(float)
    df["avg_following_count"] = df["avg_following_count"].astype(float)
    df["avg_user_tweet_count"] = df["avg_user_tweet_count"].astype(float)

    df["tweet_date"] = pd.to_datetime(df["tweet_date"])

    #Create temporary DF
    df_temp = df.groupby([pd.Grouper(key='tweet_date',freq='D'), 'party']).agg({
    "reply_count": "sum",
    "retweet_count": "sum",
    "like_count": "sum",
    "avg_len_of_tweet": "mean",
    "avg_followers_count": "mean",
    "avg_following_count": "mean",
    "avg_user_tweet_count": "mean"
    })

    #Create: Followers Ratio
    df_temp["avg_ff_ratio"] = df_temp["avg_followers_count"] / df_temp["avg_following_count"]

    # Create: share of tweets that a party has in comparison to all tweets on a given day
    df_temp_2 = df.groupby([pd.Grouper(key='tweet_date',freq='D'), 'party']).agg({
    "text": "count"}).groupby(level=0).apply(lambda x: x/x.sum())

    # Create: Share of tweets that come from a unique user for each party on a given day
    df_temp_3 = df.groupby([pd.Grouper(key='tweet_date',freq='D'), 'party']).agg({
    "author_id": "nunique",
    "text": "count"})
    df_temp_3["share_unique_users"] = df_temp_3["author_id"] / df_temp_3["text"]
    df_temp_3 = df_temp_3["share_unique_users"]

    # Join the different temporary DFs into a final DataFrame
    df_final = df_temp.join(df_temp_2).join(df_temp_3)
    df_final = df_final.rename(columns={'text': "share_of_tweets"})

    return df_final


def create_sentiment_features(df):
    '''
    Generates the following features: "Weighted Sentiment", "Share of positive tweets", "Share of negative tweets".
    '''
    # Change dtype
    df = df.fillna(0)
    df["retweet_count"] = df["retweet_count"].astype(float)
    df["like_count"] = df["like_count"].astype(float)
    df["sentiment"] = df["sentiment"].astype(float)

    df = df[["tweet_date","party","retweet_count", "like_count", "sentiment"]]
    # Generate "Weighted Sentiment"
    df["like_count"] = df["like_count"]+10
    df["retweet_count"] = df["retweet_count"]+10
    df["weighted_sentiment"] = np.log10(df["like_count"]) * np.log10(df["retweet_count"]) * df["sentiment"]

    # Generate "Share of positive tweets"
    df["share_of_positive_tweets"] = df["sentiment"]
    dict_only_positive = {-2: 0, 1: 0, 2: 1}
    df["share_of_positive_tweets"].replace(dict_only_positive, inplace=True)

    # Generate "Share of negative tweets"
    df["share_of_negative_tweets"] = df["sentiment"]
    dict_only_negative = {-2: 1, 1: 0, 2: 0}
    df["share_of_negative_tweets"].replace(dict_only_negative, inplace=True)

    df["share_of_positive_tweets2"] = df["share_of_positive_tweets"]
    df["share_of_negative_tweets2"] = df["share_of_negative_tweets"]

    df["tweet_date"] = pd.to_datetime(df["tweet_date"])

    df = df.groupby([pd.Grouper(key='tweet_date',freq='D'), "party"]).agg({
        "weighted_sentiment": "mean",
        "share_of_positive_tweets": "sum",
        "share_of_positive_tweets2": "count",
        "share_of_negative_tweets": "sum",
        "share_of_negative_tweets2": "count",})
    df["share_of_positive_tweets"] = df["share_of_positive_tweets"] / df["share_of_positive_tweets2"]
    df["share_of_negative_tweets"] = df["share_of_negative_tweets"] / df["share_of_negative_tweets2"]
    df = df.drop(columns=["share_of_positive_tweets2", "share_of_negative_tweets2"])

    return df


def join_features(df1, df2):
    df_joined = df1.join(df2)
    return df_joined


def load_poll_df():
    df = clean_data(yesterday=True)
    df = df[["Date", "CDU/CSU", 'SPD', 'Grüne', 'FDP', "Linke", 'AfD', 'other']]
    return df


def create_rnn_final_df(df_poll ,df_joined):
    '''
    Joines (how=outer) engineered features DF and poll DF for the German parties
    '''
    # Rename df_poll columns and change dtype to datetime
    df_poll = df_poll.rename(columns = {"Date": "tweet_date",
                                        "CDU/CSU":"CDU",
                                        "Grüne": "GRUENE",
                                        "Linke": "LINKE",
                                        "AfD": "AFD",
                                        "other": "OTHER"
                                       })
    df_poll["tweet_date"] = pd.to_datetime(df_poll["tweet_date"])
    df_poll = df_poll.set_index("tweet_date")

    # Unstack the indexes in order to join on the tweet date and parties
    df_poll = pd.DataFrame(df_poll.T.unstack(level = 0))
    df_poll.index = df_poll.index.set_names(['tweet_date', 'party'])

    # Join both DFs together
    df_final = df_poll.join(df_joined, how = "outer")

    # Rename new column as "poll"
    df_final = df_final.rename(columns = {0: "poll"})

    print("Success")
    #df_final.to_csv('/Users/finnzurmuehlen/Downloads/df_final_py_test_2.csv')
    return df_final


def get_features(df):
    #df_clean = load_and_clean_csv(df)
    df_non_sentiment = create_non_sentiment_features(df)
    df_sentiment = create_sentiment_features(df)
    df_joined = join_features(df_non_sentiment, df_sentiment)
    df_poll = load_poll_df()
    df_final = create_rnn_final_df(df_poll, df_joined)
    return df_final



if __name__ == '__main__':
    pass
