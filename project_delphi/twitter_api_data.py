import requests
import time
import datetime
import os
import pandas as pd
from google.cloud import storage
from project_delphi.twitter_api_params import query_dict, get_credentials
from project_delphi.params import BUCKET_NAME


def create_url(keywords, start_date, end_date, max_results = 10):
    """Create the url with current keywords"""

    #Change to the endpoint you want to collect data from
    search_url = "https://api.twitter.com/2/tweets/search/all"

    #change params based on the endpoint you are using
    query_params = {'query': keywords,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,geo.place_id',
                    'tweet.fields': 'id,text,created_at,lang,public_metrics,source',
                    'user.fields': 'id,created_at,location,public_metrics',
                    'place.fields': 'full_name,country_code,geo,place_type',
                    'next_token': {}}

    # return tuple: [0] is search_url and [1] is the dict with query params
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token):
    """Returns the api response in a json format and sets 'next_token' value"""

    #params dict received from create_url function, set next_token value
    params['next_token'] = next_token

    # call api
    response = requests.request("GET", url, headers = headers, params = params)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    # return api response as json
    return response.json()


def call_api(headers,
             keywords,
             start_time,
             end_time,
             max_results,
             new_token=None):
    """Calls the twitter api and returns a dataframe containig all fetched information"""

    # create url by calling above defined function; url is a tuple
    url = create_url(keywords, start_time, end_time, max_results)

    # call api with above defined function
    response = connect_to_endpoint(url[0], headers, url[1], new_token)

    #response has 3 keys:
    #"data": tweet information in a dict
    #"includes": dict with one key "users" which is a dict of user information
    #"meta": api request information


    # create first DataFrame about tweets out of data key
    tweet_df = pd.json_normalize(response["data"])

    # rename columns to not get identical names with user_df
    tweet_df.rename(columns={'id':'tweet_id',
                             'created_at': "tweet_created_at"},
                    inplace=True)

    # create second DataFrame about users out of response key
    user_df = pd.json_normalize(response["includes"]["users"])

    # rename columns to not get identical names with tweet_df
    user_df.rename(columns={'id':'author_id',
                            'created_at': "profile_created_at"},
                    inplace=True)

    # merge two dataframes into one
    merged_df = tweet_df.merge(user_df, how = "outer", on="author_id")


    collected_tweets = response["meta"]["result_count"]
    next_token = response["meta"].get("next_token", False)

    # return a df containing all information from the api call, the next_token for continuous search and number of collected tweets
    return merged_df, next_token, collected_tweets


def get_data(party, keywords, start_time,
             end_time, max_results, tweet_amount):
    """Calls the twitter api until a maximun 'tweet_amount' has been reached or
       there are no more results and next_token is False.
       Returns a DataFrame containing all fethed information for one combination of keywords"""

    # create a main DataFrame to which all the api call results for one party are concatenated
    one_party_df = pd.DataFrame()
    headers = get_credentials()

    # set collected tweet counter to zero
    collected_tweets = 0

    # call the api the first time resulting in a returned DataFrame, the next token and number of collected tweets
    single_api_call_df, next_token, collected_tweets = call_api(headers, keywords,
                                   start_time, end_time,
                                   max_results,
                                   new_token=None)

    # concat the DataFrames to save function call result
    one_party_df = pd.concat([one_party_df, single_api_call_df], ignore_index=True)

    # add number of fetched tweets to counter
    collected_tweets += collected_tweets

    # while there is a next token in api call result
    # call the api again with the next_token as additional parameter until the value becomes false
    while next_token:

        # sleep 4 seconds to not exceed api call limit per 15 Minutes (300)
        time.sleep(4)

        # call api with new next_token
        single_api_call_df, next_token, collected_tweets = call_api(headers, keywords,
                                       start_time, end_time,
                                       max_results,
                                       new_token=next_token)
        print(collected_tweets)
        # save result and add number of tweets
        one_party_df = pd.concat([one_party_df, single_api_call_df], ignore_index=True)
        collected_tweets += collected_tweets


        # break the loop if the predefined search limit is reached
        if collected_tweets > tweet_amount:
            print(f"Reached predefined search limit of {tweet_amount} tweets")
            break

    # after collecting all tweets create a new column containing the party's name
    one_party_df["party"] = party

    # return a DataFrame with all tweets for one time period
    return one_party_df



"""def run_app():
    temp_data = get_tweets

    full_data = sentiment(temp_data)

    cleaned_data = cleaner(full_data)"""


def upload_tweets_to_gcp(date):

    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nicolas/code/NicolasBuehringer/gcp/project-delphi-323909-05dee7633cbe.json"

    client = storage.Client()

    STORAGE_LOCATION = f"twitter_data/temp_tweets/temp_tweet_database_{date[5:7]}_{date[8:10]}.csv"

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(STORAGE_LOCATION)

    blob.upload_from_filename(
        f"temp_tweet_database_{date[5:7]}_{date[8:10]}.csv"
    )


if __name__ == "__main__":
    """
    # create a master DataFrame for all parties
    all_parties_df = pd.DataFrame()

    # get current time"""
    current_time = datetime.datetime.today()
    """
    # get current time yesterday
    current_time_yesterday = (current_time - datetime.timedelta(1))

    # convert to ISO 8601: YYYY-MM-DDTHH:mm:ssZ
    # this is UTC; we are not accounting for german time zone +02:00
    start_time = f"{str(current_time_yesterday)[:10]}T00:00:01.000Z"
    end_time = f"{str(current_time)[:10]}T00:00:01.000Z"

    # set max results per api call
    max_results = 500

    # for key, value in query_dict from twitter_api_params.py
    for party, keywords in query_dict.items():

        # set maximum tweet amount from keywords dict
        tweet_amount =  keywords[1]

        # collect the DataFrame for one party-keyword combination
        one_party_df = get_data(party, keywords[0], start_time,
                             end_time, max_results, tweet_amount)

        # concat to master DataFrame
        all_parties_df = pd.concat([all_parties_df, one_party_df], ignore_index=True)

        # save master DataFrame as a csv
        all_parties_df.to_csv(
            f"temp_tweet_database_{str(current_time)[5:7]}_{str(current_time)[8:10]}.csv"
        )
    """
    upload_tweets_to_gcp(str(current_time))
