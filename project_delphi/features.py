# Imports
import pandas as pd
import numpy as np
import datetime


cdu_path = '/Users/finnzurmuehlen/Downloads/2021_cdu_with_sentiment.csv'
spd_path = ''


def load_and_clean_csv(party, csv_path):
    '''
    Function loads CSV data from the Twitter API+Sentiment and returns a cleaned DF
    '''
    # Load CSV Dataset via Path
    df = pd.read_csv(csv_path, lineterminator='\n', low_memory=False)

    # Create "Party" Column and rename other columns
    df['party'] = party
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
             'sentiment'
            ]]

    # Clean dataset columns:
       # Change dtype
    df["tweet_date"] = df["tweet_date"].astype(str)
    df = df[df.tweet_date.str.match('(\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2})')]
    df = df[(df.tweet_date.str.len() == 23) | (df.tweet_date.str.len() == 24)]
    df['tweet_date'] = df['tweet_date'].str.slice(0,19)
    df["tweet_date"] = pd.to_datetime(df["tweet_date"])
    df['profile_creation_date'] = df['profile_creation_date'].str.slice(0,19)
    df["profile_creation_date"] = pd.to_datetime(df["profile_creation_date"])
       # Drop duplicates
    df = df.drop_duplicates()
       # Transform sentiment to numeric type
    dict_to_numeric = {"negative": -2, "neutral": 1, "positive": 2}
    df["sentiment"].replace(dict_to_numeric, inplace=True)

    return df


if __name__ == '__main__':
    pass
