import datetime
import pandas as pd
from germansentiment import SentimentModel

def get_sentiment(data):
# import new daily dataframe google cloud -- how??


    model = SentimentModel()

    # sentiment predictions will be appended as a list to this list for each iteration
    full_sentiment = []

    # set amount of analyzed tweets per iteration and maximum index
    x = 1000
    max_len = len(data) - 1

    # iterate over a range of 0, len_dataframe with step size 987
    for i in range(0,max_len, x):

        # slice dataframe for the current 987 rows
        temp = data.iloc[i: (i + x)]

        # turn tweets into a list for sentiment analysis
        temp_tweets = list(temp.text)

        # make sure that its a list of strings; otherwise error: cant replace float
        temp_tweets = [str(x) for x in temp_tweets]


        # predict sentiment analysis on x amount of tweets
        temp_result = model.predict_sentiment(temp_tweets)

        # append to before defined empty list
        full_sentiment.append(temp_result)

    full_sentiment = sum(full_sentiment, [])
    data["sentiment"] = full_sentiment

    return data


if __name__ == "__main__":
    today_date = str(datetime.datetime.today())

    data = pd.read_csv("temp_tweet_database_08_30.csv")

    database = get_sentiment(data)

    database.to_csv(f"tweet_database_{today_date[5:7]}_{today_date[8:10]}.csv")
