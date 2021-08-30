import pandas as pd
from polls_data_clean import get_data, clean_data, get_parties


def poll_for_streamlit():

    #get poll data
    polls = clean_data()

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
    parties = ["SPD", "CDU", "LINKE", "GRUENE", "FDP", "AFD", "OTHERS"]
    sentiments = ["positive", "negative"]

    #Columns to keep
    columns = [
        'text', 'tweet_created_at', 'public_metrics.retweet_count',
        'public_metrics.reply_count', 'public_metrics.like_count', 'username',
        'sentiment', "party"
    ]

    #Only keep relevant columns of Twitter dataframe
    df = df[columns]

    #Change datatype to numeric
    df["public_metrics.like_count"] = pd.to_numeric(
        df["public_metrics.like_count"])
    df["public_metrics.reply_count"] = pd.to_numeric(
        df["public_metrics.reply_count"])

    # Filter df for day of tweet
    df = df[df["tweet_created_at"]==tweet_date]

    #Get most liked/ retweeted Tweets over all parties
    for sentiment in sentiments:

        #Filter for sentiment
        tweets_tmp = pd.DataFrame(
            df[df["sentiment"] == sentiment].reset_index())

        # Find tweet with most likes and concatenate to final df
        most_liked_tweet = tweets_tmp.iloc[[
            tweets_tmp["public_metrics.like_count"].idxmax()
        ]]
        most_liked_tweets = pd.concat([most_liked_tweets, most_liked_tweet],
                                      ignore_index=True)
        most_liked_tweets["party"] = "OVERALL"

        # Find tweet with most retweets and concatenate to final df
        most_retweeted_tweet = tweets_tmp.iloc[[
            tweets_tmp["public_metrics.retweet_count"].idxmax()
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
                tweets_tmp["public_metrics.like_count"].idxmax()
            ]]
            most_liked_tweets = pd.concat(
                [most_liked_tweets, most_liked_tweet], ignore_index=True)

            # Find tweet with most retweets and concatenate to final df
            most_retweeted_tweet = tweets_tmp.iloc[[
                tweets_tmp["public_metrics.retweet_count"].idxmax()
            ]]
            most_retweeted_tweets = pd.concat(
                [most_retweeted_tweets, most_retweeted_tweet],
                ignore_index=True)

    return most_liked_tweets, most_retweeted_tweets



if __name__ == "__main__":

    #test1 = clean_data()
    poll_for_streamlit()

'''    test = pd.read_csv("raw_data/test.csv")
    tweet_date = "2021-08-26"
    t1, t2 = most_popular_tweets(test, tweet_date)
    print(t1)
    print(t2)'''
