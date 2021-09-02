#Imports
from google.cloud import storage
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO

import pandas as pd
import numpy as np
import streamlit as st
#import requests
import os

#Set page layout to wide
st.set_page_config(layout="wide")

#---------------------------------------------
#GCP
#---------------------------------------------

# create credentials file
google_credentials_file = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

if not os.path.isfile(google_credentials_file):

    print("write credentials file 🔥" + f"\n- path: {google_credentials_file}")

    # retrieve credentials
    json_credentials = os.environ["GOOGLE_CREDS"]

    # write credentials
    with open(google_credentials_file, "w") as file:

        file.write(json_credentials)

else:

    print("credentials file already exists 🎉")



def download_blob():
    """Downloads the project delphi logo image from the bucket."""
    # The ID of your GCS bucket
    bucket_name = "project_delphi_bucket"

    # The ID of your GCS object
    source_blob_name = "streamlit/delphi_project_logo_dark.png"

    # The path to which the file should be downloaded
    destination_file_name = "delphi_project_logo_dark.png"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    return mpimg.imread("delphi_project_logo_dark.png")





def get_data_from_gcp(path, index_column=None):
    """method to get the required data from google cloud bucket"""

    client = storage.Client()
    #if local:
    #    path = "raw_data/most_liked_tweets.csv"
    df = pd.read_csv(path, index_col=index_column)
    return df


# Links for all datasets needed to be displayed on Heroku
link_current_poll = "gs://project_delphi_bucket/streamlit/latest_poll.csv"
link_historic_polls = "gs://project_delphi_bucket/streamlit/polls.csv"
link_tweet_kpis = "gs://project_delphi_bucket/streamlit/tweet_kpis.csv"
link_most_liked_tweets = "gs://project_delphi_bucket/streamlit/most_liked_tweets.csv"
link_most_retweeted_tweets = "gs://project_delphi_bucket/streamlit/most_retweeted_tweets.csv"
link_logo = "gs://project_delphi_bucket/streamlit/delphi_project_logo_dark.png"
link_predicition = "gs://project_delphi_bucket/streamlit/prediction_database/prediciton_2021_09_01.csv"
link_no_of_tweets = "gs://project_delphi_bucket/streamlit/no_of_tweets.csv"

# ---------------------------------------------------------
# API calls and assignment of variables
# ---------------------------------------------------------

# Project Delphi Logo
logo_img = download_blob()

# Forecast from Delphi API
#url_delphi = "https://delphi-xq2dtozlga-ew.a.run.app/"

#response = requests.get(url_delphi).json()
forecast = get_data_from_gcp(link_predicition, index_column="Unnamed: 0")
AFD_forecast = round(forecast.iloc[-1]["AFD"], 3)*100
CDU_forecast = round(forecast.iloc[-1]["CDU"], 3)*100
FDP_forecast = round(forecast.iloc[-1]["FDP"], 3)*100
GRUENE_forecast = round(forecast.iloc[-1]["GRUENE"], 3)*100
LINKE_forecast = round(forecast.iloc[-1]["LINKE"], 3)*100
SPD_forecast = round(forecast.iloc[-1]["SPD"], 3)*100
OTHER_forecast = round(forecast.iloc[-1]["OTHER"], 3)*100

# Current poll from DAWUM API
current_poll = get_data_from_gcp(link_current_poll)
AFD_poll = round(current_poll.loc[0,"AfD"],1)
CDU_poll = round(current_poll.loc[0, "CDU/CSU"],1)
FDP_poll = round(current_poll.loc[0, "FDP"],1)
GRUENE_poll = round(current_poll.loc[0,"Grüne"],1)
LINKE_poll = round(current_poll.loc[0,"Linke"],1)
SPD_poll = round(current_poll.loc[0,"SPD"],1)
OTHER_poll = round(current_poll.loc[0, "other"], 1)

# Poll data and prediction over time
historic_polls = get_data_from_gcp(link_historic_polls, index_column="Date")
historic_polls = historic_polls.tail(30)

# Engineered Twitter Features (KPIs) via Delphi API
tweet_kpis = get_data_from_gcp(link_tweet_kpis)
tweet_kpis['order'] = pd.Categorical(
    tweet_kpis['party'],
    categories=['CDU', 'SPD', 'GRUENE', 'FDP', 'AFD', 'LINKE', 'OTHER'],
    ordered=True)
tweet_kpis = tweet_kpis.sort_values('order')

# Most liked/ retweeted positive and negative tweet per party
most_liked_tweets = get_data_from_gcp(link_most_liked_tweets)
most_retweeted_tweets = get_data_from_gcp(link_most_retweeted_tweets)

# No of todays and total no of Tweets in database
no_of_tweets = get_data_from_gcp(link_no_of_tweets)

# ---------------------------------------------------------
# Streamlit layout
# ---------------------------------------------------------

# Insert Logo Image on top left corner of the website
col0, col01 = st.columns((5,1))
col0.title("German Federal Election forecast")
col01.image(logo_img)


'''
Our goal is to create the most accurate forecast for the upcoming German federal elections on 26th September 2021
using a state-of-the art deep learning algorithm trained on current poll and Twitter data.
'''

'''
## Forecast
'''
col1, col2,  = st.columns((1,1.2))

#1st Chart: Half donut plot of delphi forecast
col1.subheader("Our forecast")

#data
label = ["Others", "Linken", "SPD", "Grünen", "FDP", "CDU/CSU", "AFD"]
colors = ["grey", "purple", "red", "green", "yellow", "black", "blue"]
val = [OTHER_forecast, LINKE_forecast, SPD_forecast, GRUENE_forecast,
    FDP_forecast, CDU_forecast, AFD_forecast]

# append artifical label, value (50%) in order to create half donut chart
label.append("")
val.append(sum(val))  # 50% blank

#Create plot
fig1, ax0 = plt.subplots(figsize=(6.9,6.9))
ax0.pie(val,
        #autopct='%1.1f%%',
        #pctdistance =0.75,
        #textprops=dict(color="w"),
        wedgeprops=dict(width=0.5, edgecolor='w'),
        labels=label,
        colors=colors)



#save plot as png image
fig1.savefig("forecast.png", bbox_inches='tight')

# Read the image
img = mpimg.imread("forecast.png")
height, width, c = img.shape

# Cut the image in half in order to only show upper half
height_cutoff = height // 2
s1 = img[:height_cutoff, :, :]
col1.image(s1)


#-------------------------------------------------------------
# 2nd Chart: Delphi vs. current poll (grouped bar chart)
poll_date = current_poll.loc[0, "Date"]
col2.subheader(f"Delphi forecast vs. current poll as of {poll_date}")

# Label and colors for all following charts
label = ["CDU/CSU", "SPD", "Grünen", "FDP", "AFD", "Linken", "Others"]
colors = ["black", "red", "green", "yellow", "blue", "purple", "grey"]

# Forecast (Delphi) and poll data
forecast = [CDU_forecast, SPD_forecast, GRUENE_forecast, FDP_forecast, AFD_forecast, LINKE_forecast, OTHER_forecast]
polls = [CDU_poll, SPD_poll, GRUENE_poll, FDP_poll, AFD_poll, LINKE_poll, OTHER_poll]

# Label per bar
x = np.arange(len(label))  # the label locations
width = 0.4  # the width of the bars

# Create plots
fig, ax = plt.subplots(figsize=(6.8,3.5))
rects1 = ax.bar(x - width/2, forecast, width, label='Delphi forecast', color=colors)
rects2 = ax.bar(x + width/2, polls, width, label='Poll', color=["dimgray", "lightcoral", "yellowgreen", "gold", "cornflowerblue", "plum", "lightgray"])


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xticks(x)
ax.set_xticklabels(label)
ax.legend()
ax.bar_label(rects1, padding=3, fmt='%.1f')
ax.bar_label(rects2, padding=3,  fmt='%.1f')
ymax = forecast +polls
ax.set_ylim([0,max(ymax)+5])


# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#set layout to tight
fig.tight_layout()

# Convert image to BytesIo so it can be displayed in streamlit
buf = BytesIO()
fig.savefig(buf, format="png")
col2.image(buf)

#-------------------------------------------------------------
# 3rd Graph: Timeline: Delphi vs. poll forecast
st.markdown("## Latest polling data")
st.markdown("")

# Create Line chart to display historic poll data
st.line_chart(historic_polls)

st.markdown("""---""")

#-------------------------------------------------------------
# Twitter Insights
col15, col001, col002, col16 = st.columns(4)

col15.markdown("## Twitter Insights")
col15.markdown("")
col15.markdown("")
col15.markdown("")

# Total no. of tweets analyzed
no_tweets_total = (no_of_tweets.iloc[0]["no_tweets_total"] / 1_000_000).round(1)
col001.metric("Total # Tweets analyzed", f"{no_tweets_total} m")
# No. of tweets today
no_tweets_today = (no_of_tweets.iloc[0]["no_tweets_today"]/1000).round(1)
col002.metric("# Tweets today", f"{no_tweets_today} k")

#Select button to change behavoiur of Twitter KPI diagrams and displayed tweets
parties_select = ["All", "CDU/CSU", "SPD", "Grünen", "FDP", "Linken", "AFD", "Others"]
selected_party = col16.selectbox("Filter for party", parties_select)

# Twitter Key Metrics
col11, col12, col13, col14 = st.columns((1,1,1,1))

label = ["CDU/CSU", "SPD", "Grünen", "FDP", "AFD", "Linken", "Others"]
colors = ["black", "red", "green", "yellow", "blue", "purple", "grey"]

# Change behavoiur of Twitter KPI diagrams and displayed tweets based on chosen party
if selected_party=="All":
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "OVERALL"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] == "OVERALL"].reset_index(drop=True)
    party = "Overall"
elif selected_party == "CDU/CSU":
    colors = [x if x =="black" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "CDU"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="CDU"].reset_index(drop=True)
    party = "CDU/CSU"
elif selected_party == "SPD":
    colors = [x if x == "red" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "SPD"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] == "SPD"].reset_index(drop=True)
    party = "SPD"
elif selected_party == "Grünen":
    colors = [x if x == "green" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "GRUENE"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="GRUENE"].reset_index(drop=True)
    party = "Grünen"
elif selected_party == "FDP":
    colors = [x if x == "yellow" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "FDP"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="FDP"].reset_index(drop=True)
    party = "FDP"
elif selected_party == "Linken":
    colors = [x if x == "purple" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "LINKE"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="LINKE"].reset_index(drop=True)
    party = "Linken"
elif selected_party == "AFD":
    colors = [x if x == "blue" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "AFD"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="AFD"].reset_index(drop=True)
    party = "AFD"
elif selected_party == "Others":
    colors = [x if x == "grey" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "OTHER"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="OTHER"].reset_index(drop=True)
    party = "Others"


#4th Graph: Share of tweets per party
col11.markdown("**% Tweets per party**")
fig21, ax21 = plt.subplots(figsize=(3, 3))
ax21.pie(tweet_kpis["share_of_tweets"], labels=label, colors=colors)
fig21.tight_layout()
buf = BytesIO()
fig21.savefig(buf, format="png", bbox_inches='tight')
col11.image(buf)

#5th Graph: Share of unique_users
col12.markdown("**% unique users**")
fig22, ax22 = plt.subplots(figsize=(3, 2.5))
uu = ax22.bar(x=tweet_kpis["party"],
         height=tweet_kpis["share_unique_users"],
         color=colors)
plt.xticks(rotation='vertical')
ax22.set_xticks(x)
ax22.set_xticklabels(label)
ax22.set_ylim([0, 1])
ax22.bar_label(uu, padding=3, fmt='%.1f')

#Hide the right and top spines
ax22.spines['right'].set_visible(False)
ax22.spines['top'].set_visible(False)

fig22.savefig(buf, format="png", bbox_inches='tight')
col12.image(buf)

#6th Graph: Share of positive Tweets
col13.markdown("**% positive Tweets**")
fig23, ax23 = plt.subplots(figsize=(3, 2.5))
po = ax23.bar(x=tweet_kpis["party"],
         height=tweet_kpis["share_of_positive_tweets"],
         color=colors)
plt.xticks(rotation='vertical')
ax23.set_xticks(x)
ax23.set_xticklabels(label)
ax23.set_ylim([0, 1])
ax23.bar_label(po, padding=3, fmt='%.1f')

# Hide the right and top spines
ax23.spines['right'].set_visible(False)
ax23.spines['top'].set_visible(False)

fig23.savefig(buf, format="png", bbox_inches='tight')
col13.image(buf)

#7th Graph: Share of negative Tweets
col14.markdown("**% negative Tweets**")
fig24, ax24 = plt.subplots(figsize=(3, 2.5))
ng = ax24.bar(x=tweet_kpis["party"],
         height=tweet_kpis["share_of_negative_tweets"],
         color=colors)
plt.xticks(rotation='vertical')
ax24.set_xticks(x)
ax24.set_xticklabels(label)
ax24.set_ylim([0, 1])
ax24.bar_label(ng, padding=3, fmt='%.1f')

# Hide the right and top spines
ax24.spines['right'].set_visible(False)
ax24.spines['top'].set_visible(False)

fig24.savefig(buf, format="png", bbox_inches='tight')
col14.image(buf)

st.markdown("""---""")

#-------------------------------------------------------------
# Display of Todays most 💙 Tweets
st.subheader(f"Todays most 💙 Tweets - {party}")
st.text("")
col3, col4,  = st.columns((1,1))
col31, col32, col33, col41, col42, col43 = st.columns((1,1,1,1,1,1))

# Positive Tweet
username = tweet_likes.loc[1, "username"]
created_at = tweet_likes.loc[1, "tweet_date"]
col3.write(f'**{username}** {created_at}')
col3.write(tweet_likes.loc[1, "text"])
no_likes = int(tweet_likes.loc[1, "like_count"])
no_retweets = int(tweet_likes.loc[1, "retweet_count"])
no_replys = int(tweet_likes.loc[1, "reply_count"])
col31.write(f"🔁 {no_retweets}")
col32.write(f"💬 {no_replys}")
col33.write(f"💙 {no_likes}")


#Negative tweet
username = tweet_likes.loc[0, "username"]
created_at = tweet_likes.loc[0, "tweet_date"]
col4.write(f'**{username}** {created_at}')
col4.write(tweet_likes.loc[0, "text"])
no_likes = int(tweet_likes.loc[0, "like_count"])
no_retweets = int(tweet_likes.loc[0, "retweet_count"])
no_replys = int(tweet_likes.loc[0, "reply_count"])
col41.write(f"🔁 {no_retweets}")
col42.write(f"💬 {no_replys}")
col43.write(f"💙 {no_likes}")


st.text("")
st.text("")
st.markdown("""---""")

#-------------------------------------------------------------
# Display of Todays most 🔁 Tweets
st.subheader(f"Todays most 🔁 Tweets - {party}")
st.text("")

col5, col6,  = st.columns((1,1))
col51, col52, col53, col61, col62, col63 = st.columns((1,1,1,1,1,1))

# Positive Tweet
username = tweet_retweets.loc[1, "username"]
created_at = tweet_retweets.loc[1, "tweet_date"]
col5.write(f'**{username}** {created_at}')
col5.write(tweet_retweets.loc[1, "text"])
no_likes = int(tweet_retweets.loc[1, "like_count"])
no_retweets = int(tweet_retweets.loc[1, "retweet_count"])
no_replys = int(tweet_retweets.loc[1, "reply_count"])
col51.write(f"🔁 {no_retweets}")
col52.write(f"💬 {no_replys}")
col53.write(f"💙 {no_likes}")

#Negative tweet
username = tweet_retweets.loc[0, "username"]
created_at = tweet_retweets.loc[0, "tweet_date"]
col6.write(f'**{username}** {created_at}')
col6.write(tweet_retweets.loc[0, "text"])
no_likes = int(tweet_retweets.loc[0, "like_count"])
no_retweets = int(tweet_retweets.loc[0, "retweet_count"])
no_replys = int(tweet_retweets.loc[0, "reply_count"])
col61.write(f"🔁 {no_retweets}")
col62.write(f"💬 {no_replys}")
col63.write(f"💙 {no_likes}")
