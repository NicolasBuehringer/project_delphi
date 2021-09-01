import datetime
import pandas as pd
from germansentiment import SentimentModel
from google.cloud import storage


def get_sentiment(raw_tweets):
    """
    Analyzes the sentiment of tweets in a dataframe given that the tweet column is named text.
    """

    model = SentimentModel()

    # sentiment predictions will be appended as a list to this list for each iteration
    full_sentiment = []

    # set amount of analyzed tweets per iteration and maximum index
    x = 500
    max_len = len(raw_tweets) - 1

    # iterate over a range of 0, len_dataframe with step size 987
    for i in range(0,max_len, x):
        print(i)
        # slice dataframe for the current 987 rows
        temp = raw_tweets.iloc[i: (i + x)]

        # turn tweets into a list for sentiment analysis
        temp_tweets = list(temp.text)

        # make sure that its a list of strings; otherwise error: cant replace float
        temp_tweets = [str(x) for x in temp_tweets]


        # predict sentiment analysis on x amount of tweets
        temp_result = model.predict_sentiment(temp_tweets)

        # append to before defined empty list
        full_sentiment.append(temp_result)

    # turn list of lists from each iteration into one list --> flatten
    full_sentiment = sum(full_sentiment, [])

    # save sentiment as new column in raw_database
    raw_tweets["sentiment"] = full_sentiment

    # this isnt really raw_tweets anymore but dont want to redefine
    return raw_tweets


if __name__ == "__main__":
    today_date = str(datetime.datetime.today())

    data = pd.read_csv("temp_tweet_database_08_30.csv")

    database = get_sentiment(data)

    database.to_csv(f"tweet_database_{today_date[5:7]}_{today_date[8:10]}.csv")
