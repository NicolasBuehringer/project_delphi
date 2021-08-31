#Imports
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import streamlit as st
import requests
import os
#import seaborn as sns
from io import BytesIO
#import plotly.express as px  #need to be included in requirements

#Set page layout to wide
st.set_page_config(layout="wide")

#GCP

from google.cloud import storage

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
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    bucket_name = "project_delphi_bucket"

    # The ID of your GCS object
    source_blob_name = "streamlit/polls.csv"

    # The path to which the file should be downloaded
    destination_file_name = "raw_data"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename("raw_data/test.csv")
    return pd.read_csv("raw_data/test.csv")
    print("Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name))

file = download_blob()
st.dataframe(file)


# ---------------------------------------------------------
# API calls and assignment of variables
# ---------------------------------------------------------

# Forecast from Delphi API
url_delphi = "https://delphi-xq2dtozlga-ew.a.run.app/"

response = requests.get(url_delphi).json()
AFD_forecast = float(response.get("AFD", 0.0))
CDU_forecast = float(response.get("CDU", 0.0))
FDP_forecast = float(response.get("FDP", 0.0))
GRUENE_forecast = float(response.get("GRUENE", 0.0))
LINKE_forecast = float(response.get("LINKE", 0.0))
SPD_forecast = float(response.get("SPD", 0.0))
OTHER_forecast = float(response.get("OTHER", 0.0))

# Current poll from DAWUM API
current_poll = pd.read_csv("raw_data/latest_poll.csv")
AFD_poll = current_poll.loc[0,"AfD"]
CDU_poll = current_poll.loc[0, "CDU/CSU"]
FDP_poll = current_poll.loc[0, "FDP"]
GRUENE_poll = current_poll.loc[0,"Grüne"]
LINKE_poll = current_poll.loc[0,"Linke"]
SPD_poll = current_poll.loc[0,"SPD"]
OTHER_poll = current_poll.loc[0,"other"]

# Poll data and prediction over time
historic_polls = pd.read_csv("raw_data/polls.csv")

# Engineered Twitter Features (KPIs) via Delphi API
tweet_kpis = pd.read_csv("raw_data/tweet_kpis.csv")
tweet_kpis['order'] = pd.Categorical(
    tweet_kpis['party'],
    categories=['CDU', 'SPD', 'GRUENE', 'FDP', 'LINKE', 'AFD', 'OTHER'],
    ordered=True)
tweet_kpis = tweet_kpis.sort_values('order')

# Most liked/ retweeted positive and negative tweet per party
most_liked_tweets = pd.read_csv("raw_data/most_liked_tweets.csv")
most_retweeted_tweets = pd.read_csv("raw_data/most_retweeted_tweets.csv")


# ---------------------------------------------------------
# Streamlit layout
# ---------------------------------------------------------

'''
# German Federal Election forecast
'''

'''
Our goal is to create the most accurate forecast for the upcoming German federal elections on 26th September 2021
using a state-of-the art deep learning algorithm trained on current poll and Twitter data.
'''

'''
## Forecast
'''
col1, col2,  = st.columns((1,1))

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
fig1 = plt.figure(figsize=(7,7))
plt.pie(val, wedgeprops=dict(width=0.5,edgecolor='w'), labels=label, colors=colors)

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
poll_date = current_poll.loc[0,"Date"]
col2.subheader(f"Delphi vs. current poll as of {poll_date}")

# Label and colors for all following charts
label = ["CDU/CSU", "SPD", "Grünen", "FDP", "Linken", "AFD", "Others"]
colors = ["black", "red", "green", "yellow", "purple", "blue", "grey"]

# Forecast (Delphi) and poll data
forecast = [CDU_forecast, SPD_forecast, GRUENE_forecast, FDP_forecast, LINKE_forecast, AFD_forecast, OTHER_forecast]
polls = [CDU_poll, SPD_poll, GRUENE_poll, FDP_poll, LINKE_poll, AFD_poll, OTHER_poll]

# Label per bar
x = np.arange(len(label))  # the label locations
width = 0.35  # the width of the bars

# Create plots
fig, ax = plt.subplots(figsize=(6,3.5))
rects1 = ax.bar(x - width/2, forecast, width, label='Delphi forecast', color=colors)
rects2 = ax.bar(x + width/2, polls, width, label='Poll', color=["dimgray", "lightcoral", "yellowgreen", "gold", "plum", "cornflowerblue", "lightgray"])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xticks(x)
ax.set_xticklabels(label)
ax.legend()
ax.bar_label(rects1, padding=10)
ax.bar_label(rects2, padding=3)
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
st.markdown("## Timeline: Delphi vs. poll forecast")
st.markdown("Line graph comparing prediciton from Delphi with poll per party over time (e.g. last week)")

# Mock data for chart
np.random.seed(2021)
N = 10
rng = pd.date_range(start='2021-08-16', end='2021-08-25')
df = pd.DataFrame(np.random.uniform(5, 20, size=(10,14)), columns=["CSU", "SPD", "Grünen", "FDP", "Linken", "AFD", "Others", "CSU_poll", "SPD_poll", "Grünen_poll", "FDP_poll", "Linken_poll", "AFD_poll", "Others_poll"], index=rng)
st.line_chart(df)

st.markdown("""---""")

#-------------------------------------------------------------
# Twitter Insights
col15, col16 = st.columns((3,1))

col15.markdown("## Twitter Insights")
col15.markdown("")
col15.markdown("")
col15.markdown("")

#Select button to change behavoiur of Twitter KPI diagrams and displayed tweets
parties_select = ["All", "CDU/CSU", "SPD", "Grünen", "FDP", "Linken", "AFD", "Others"]
selected_party = col16.selectbox("Filter for party", parties_select)

# Twitter Key Metrics
col11, col12, col13, col14 = st.columns((1,1,1,1))

label = ["CDU/CSU", "SPD", "Grünen", "FDP", "Linken", "AFD", "Others"]
colors = ["black", "red", "green", "yellow", "purple", "blue", "grey"]

# Change behavoiur of Twitter KPI diagrams and displayed tweets based on chosen party
if selected_party=="All":
    colors = ["black", "red", "green", "yellow", "purple", "blue", "grey"]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "OVERALL"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] == "OVERALL"].reset_index(drop=True)
elif selected_party == "CDU/CSU":
    colors = [x if x =="black" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "CDU"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="CDU"].reset_index(drop=True)
elif selected_party == "SPD":
    colors = [x if x == "red" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "SPD"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] == "SPD"].reset_index(drop=True)
elif selected_party == "Grünen":
    colors = [x if x == "green" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "GRUENE"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="GRUENE"].reset_index(drop=True)
elif selected_party == "FDP":
    colors = [x if x == "yellow" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "FDP"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="FDP"].reset_index(drop=True)
elif selected_party == "Linken":
    colors = [x if x == "purple" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "LINKE"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="LINKE"].reset_index(drop=True)
elif selected_party == "AFD":
    colors = [x if x == "blue" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "AFD"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="AFD"].reset_index(drop=True)
elif selected_party == "Others":
    colors = [x if x == "grey" else "lightgray" for x in colors]
    tweet_likes = most_liked_tweets[most_liked_tweets["party"] == "OTHER"].reset_index(drop=True)
    tweet_retweets = most_retweeted_tweets[most_retweeted_tweets["party"] =="OTHER"].reset_index(drop=True)


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
ax22.bar(x=tweet_kpis["party"],
         height=tweet_kpis["share_unique_users"],
         color=colors)
plt.xticks(rotation='vertical')
ax22.set_xticks(x)
ax22.set_xticklabels(label)

#Hide the right and top spines
ax22.spines['right'].set_visible(False)
ax22.spines['top'].set_visible(False)

fig22.savefig(buf, format="png", bbox_inches='tight')
col12.image(buf)

#6th Graph: Share of positive Tweets
col13.markdown("**% positive Tweets**")
fig23, ax23 = plt.subplots(figsize=(3, 2.5))
ax23.bar(x=tweet_kpis["party"],
         height=tweet_kpis["share_of_positive_tweets"],
         color=colors)
plt.xticks(rotation='vertical')
ax23.set_xticks(x)
ax23.set_xticklabels(label)

# Hide the right and top spines
ax23.spines['right'].set_visible(False)
ax23.spines['top'].set_visible(False)

fig23.savefig(buf, format="png", bbox_inches='tight')
col13.image(buf)

#7th Graph: Share of negative Tweets
col14.markdown("**% negative Tweets**")
fig24, ax24 = plt.subplots(figsize=(3, 2.5))
ax24.bar(x=tweet_kpis["party"],
         height=tweet_kpis["share_of_negative_tweets"],
         color=colors)
plt.xticks(rotation='vertical')
ax24.set_xticks(x)
ax24.set_xticklabels(label)

# Hide the right and top spines
ax24.spines['right'].set_visible(False)
ax24.spines['top'].set_visible(False)

fig24.savefig(buf, format="png", bbox_inches='tight')
col14.image(buf)

st.markdown("""---""")

#-------------------------------------------------------------
# Display of Todays most 💙 Tweets
st.subheader("Todays most 💙 Tweets")
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
st.subheader("Todays most 🔁 Tweets")
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
