import pandas as pd
from google.cloud import storage
from project_delphi.params import BUCKET_NAME
from project_delphi.utils import get_date_n_days_ago
import os

# how get environment variable??



def merge_daily_to_master(daily_database):
    """"
    Downloads  master_database from google cloud, concats current daily_database to it
    and uploads the new master_database with new filename.
    Returns new_master_database for further usage
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nicolas/code/NicolasBuehringer/gcp/project-delphi-323909-05dee7633cbe.json"

    # get dates in format YYYY_MM_DD
    date_two_days_ago = get_date_n_days_ago(2)
    date_yesterday = get_date_n_days_ago(1)

    # download old master_database
    old_master_database = pd.read_csv(
        f"gs://project_delphi_bucket/tweets/tweet_database_{date_two_days_ago[:10]}.csv"
    )

    # concat daily database with old master
    new_master_database = pd.concat([old_master_database, daily_database])

    # save new database as csv
    new_master_database.to_csv(f"tweet_database_{date_yesterday[:10]}.csv")

    # upload new master_database
    client = storage.Client()

    # define storage location
    STORAGE_LOCATION = f"tweets/tweet_database_{date_yesterday[:10]}.csv"

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(STORAGE_LOCATION)

    # upload saved csv
    blob.upload_from_filename(
        f"tweet_database_{date_yesterday[:10]}.csv"
    )

    # return new_master_database for next function in run_app
    return new_master_database
