import gepd
import numpy as np
import pandas as pd
import datetime


def get_data(**kwargs):
    data = gepd.gepd()
    df = data.get_surveys()

    return df

def get_parties(**kwargs):

    data = gepd.gepd()
    parties_dict = data.get_parties()

    parties_dict_short = {}
    for key, value in parties_dict.items():
        parties_dict_short[key] = value["Shortcut"]
    return parties_dict_short

def clean_data(yesterday = False):

    current_time = datetime.datetime.today()
    # get current time yesterday
    # current_time_yesterday = (current_time - datetime.timedelta(1))
    # convert to ISO 8601: YYYY-MM-DDTHH:mm:ssZ
    # this is UTC; we are not accounting for german time zone +02:00
    start_date = "2021-05-22"
    end_date = f"{str(current_time)[:10]}"

    if yesterday:
        end_date = str(current_time - datetime.timedelta(1))[:10]


    other_parties = ["Sonstige", "Freie Wähler", "BP","Die PARTEI", "SSW", "BVB/FW", "NPD", "Piraten",\
                    "BIW", "Tierschutzpartei"]

    parties_dict_short = get_parties()
    df = get_data()
    df = df.rename(columns=parties_dict_short)
    df = df.loc[df["Parliament_ID"] == "0"]

    df["Date"] =  pd.to_datetime(df["Date"], format= "Y-M-D")
    df_dated = df.loc[(df['Date'] > start_date) & (df['Date'] <= end_date)]

    df_dated = df_dated.fillna(0)
    df_dated["CDU/CSU"] = df_dated["CDU/CSU"] + df_dated["CDU"] + df_dated["CSU"]
    df_dated = df_dated.drop(columns = ["CDU", "CSU"])
    df_dated["other"] =  df_dated[other_parties].sum(axis=1)

    df_dated = df_dated.drop( columns = other_parties ).drop( columns = ["Parliament_ID","Institute_ID", "Tasker_ID"] )

    df_dated_grouped = df_dated.groupby(by = "Date").mean()

    correct_dates = pd.DataFrame(pd.date_range(start = start_date, end = end_date ))

    df_dated = correct_dates.merge(df_dated_grouped, how = "left", left_on= 0 , right_on = ["Date" ]).set_index([0])

    df_dated = df_dated.fillna(method='ffill')

    df_final =  df_dated.iloc[2:].round(2)
    df_final.index.name = 'Date'

    df_final["Surveyed_Persons"] = df_final["Surveyed_Persons"].astype(int)

    df_final = df_final.reset_index()

    return df_final

if __name__ == '__main__':
    print("working")
    df = clean_data()
    print(df)
