import os
import datetime
from google.cloud import storage
from project_delphi.params import BUCKET_NAME


def get_date_n_days_ago(ndelta=0):
    """
    Returns date n days ago in format YYYY_MM_DD. Without parameter it returns today's date.
    """
    # get current time as datetime
    current_time = datetime.datetime.today()

    # check if a historic date is requested
    if ndelta == 0:

        current_time = str(current_time)

        return f"{current_time[:4]}_{current_time[5:7]}_{current_time[8:10]}"

    # get current time yesterday
    current_time_yesterday = str(current_time - datetime.timedelta(ndelta))

    return f"{current_time_yesterday[:4]}_{current_time_yesterday[5:7]}_{current_time_yesterday[8:10]}"
