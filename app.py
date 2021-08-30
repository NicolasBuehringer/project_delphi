#Imports
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import streamlit as st
import requests
#import seaborn as sns
from io import BytesIO
#import plotly.express as px  #need to be included in requirements

#Set page layout to wide
st.set_page_config(layout="wide")

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

# Engineered Twitter Feautres (KPIs) via Delphi API
#tes = pd.read_csv("raw_data/tweet_kpis.csv")

# Dummy values for Twitter KPIS
twitter_kpis = [
    {'party': 'AFD',
        'replies_count': 14.0,
        'retweets_count': 6.0,
        'likes_count': 34.0,
        'avg_len_of_tweet': 191.6382978723404,
        'share_of_tweets': 0.1374269005847953,
        'share_unique_users': 0.7021276595744681,
        'weighted_sentiment': 0.4,
        'share_of_positive_tweets': 0.4,
        'share_of_negative_tweets': 0.4},
    {'party': 'FDP',
        'replies_count': 6.0,
        'retweets_count': 3.0,
        'likes_count': 19.0,
        'avg_len_of_tweet': 170.0,
        'share_of_tweets': 0.1666666666666666,
        'share_unique_users': 0.9298245614035088,
        'weighted_sentiment': 0.4,
        'share_of_positive_tweets': 0.4,
        'share_of_negative_tweets': 0.4},
    {'party': 'GRUENE',
        'replies_count': 15.0,
        'retweets_count': 5.0,
        'likes_count': 23.0,
        'avg_len_of_tweet': 195.3928571428572,
        'share_of_tweets': 0.2456140350877192,
        'share_unique_users': 0.8214285714285714,
        'weighted_sentiment': 0.4,
        'share_of_positive_tweets': 0.4,
        'share_of_negative_tweets': 0.4},
    {'party': 'LINKE',
        'replies_count': 5.0,
        'retweets_count': 1.0,
        'likes_count': 5.0,
        'avg_len_of_tweet': 150.96296296296296,
        'share_of_tweets': 0.0789473684210526,
        'share_unique_users': 0.7777777777777778,
        'weighted_sentiment': 0.4,
        'share_of_positive_tweets': 0.4,
        'share_of_negative_tweets': 0.4},
    {'party': 'SPD',
        'replies_count': 31.0,
        'retweets_count': 18.0,
        'likes_count': 73.0,
        'avg_len_of_tweet': 201.0708661417323,
        'share_of_tweets': 0.3713450292397661,
        'share_unique_users': 0.7401574803149606,
        'weighted_sentiment': 0.4,
        'share_of_positive_tweets': 0.4,
        'share_of_negative_tweets': 0.4}
    ]

# Dummy values for most liked/ retweeted positive and negative tweet per party
famous_tweets = {'pos_most_likes': {'index': 2420,
  'text': 'Viele #Linke hier auf Twitter reden zwar von Toleranz und Vielfalt und fordern genau das auch ein, leben aber das ganze Gegenteil davon aus. Immer wieder eine bemerkenswerte Feststellung.',
  'tweet_created_at': '2021-08-25T18:05:45.000Z',
  'public_metrics.retweet_count': 109,
  'public_metrics.reply_count': 32,
  'public_metrics.like_count': 948,
  'sentiment': 'positive'},
 'pos_most_rewteets': {'index': 2420,
  'text': 'Viele #Linke hier auf Twitter reden zwar von Toleranz und Vielfalt und fordern genau das auch ein, leben aber das ganze Gegenteil davon aus. Immer wieder eine bemerkenswerte Feststellung.',
  'tweet_created_at': '2021-08-25T18:05:45.000Z',
  'public_metrics.retweet_count': 109,
  'public_metrics.reply_count': 32,
  'public_metrics.like_count': 948,
  'sentiment': 'positive'},
 'neg_most_likes': {'index': 29962,
  'text': 'Linker Bundestagsabgeordneter solidarisiert sich mit rechtem Schwurbelblogger.\n\nIst das ok für die Linksfraktion, @DietmarBartsch @Amira_M_Ali ? https://t.co/LinLZ68TGr',
  'tweet_created_at': '2021-07-28T11:22:44.000Z',
  'public_metrics.retweet_count': 142,
  'public_metrics.reply_count': 515,
  'public_metrics.like_count': 1690,
  'sentiment': 'negative'},
 'neg_most_retweets': {'index': 14464,
    'text': 'Sich über den Tod von 37 Bundeswehrsoldaten in #Afganisten zu freuen…. Einfach ekelhaft, was dieser Funktionär (Bijan Tavasolli) @DieLinke_HH  von sich gibt! https://t.co/NE9LxsJuvb',
    'tweet_created_at': '2021-08-16T08:58:49.000Z',
    'public_metrics.retweet_count': 521,
    'public_metrics.reply_count': 148,
    'public_metrics.like_count': 1589,
    'sentiment': 'negative'}
 }

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

# data
party_color_dict = {
    "Others": "grey",
    "Linken": "purple",
    "SPD": "red",
    "Grünen": "green",
    "FDP": "yellow",
    "CDU/CSU": "black",
    "AFD": "blue"
    }
label = ["Others", "Linken", "SPD", "Grünen", "FDP", "CDU/CSU", "AFD"]
val = [OTHER_forecast, LINKE_forecast, SPD_forecast, GRUENE_forecast, FDP_forecast, CDU_forecast, AFD_forecast]
# append data and assign color
label.append("")
val.append(sum(val))  # 50% blank
colors = [
    party_color_dict.get(label[0], "white"),
    party_color_dict.get(label[1], "white"),
    party_color_dict.get(label[2], "white"),
    party_color_dict.get(label[3], "white"),
    party_color_dict.get(label[4], "white"),
    party_color_dict.get(label[5], "white"),
    party_color_dict.get(label[6], "white")]


col1.subheader("Our forecast")

#Create half donut plot of forecast
fig1 = plt.figure(figsize=(7,7))
plt.pie(val, wedgeprops=dict(width=0.5,edgecolor='w'), labels=label, colors=colors)

#save forecast as png image
fig1.savefig("forecast.png", bbox_inches='tight')

# Read the image
img = mpimg.imread("forecast.png")
height, width, c = img.shape

# Cut the image in half
height_cutoff = height // 2
s1 = img[:height_cutoff, :, :]

# Show upper half
col1.image(s1)



# Delphi vs. current poll (grouped bar chart)
created_at = "2021-08-25"
col2.subheader(f"Delphi vs. current poll as of {created_at}")

labels = ["CSU", "SPD", "Grünen", "FDP", "Linken", "AFD", "Others"]
forecast = [CDU_forecast, SPD_forecast, GRUENE_forecast, FDP_forecast, LINKE_forecast, AFD_forecast, OTHER_forecast]
polls = [CDU_poll, SPD_poll, GRUENE_poll, FDP_poll, LINKE_poll, AFD_poll, OTHER_poll]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(6,3.5))
rects1 = ax.bar(x - width/2, forecast, width, label='Delphi forecast', color=["black", "red", "green", "yellow", "purple", "blue", "grey"])
rects2 = ax.bar(x + width/2, polls, width, label='Poll', color=["dimgray", "lightcoral", "yellowgreen", "gold", "plum", "cornflowerblue", "lightgray"])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

ax.bar_label(rects1, padding=10)
ax.bar_label(rects2, padding=3)
ymax = forecast +polls
ax.set_ylim([0,max(ymax)+5])

fig.tight_layout()


buf = BytesIO()
fig.savefig(buf, format="png")
col2.image(buf)


st.markdown("## Timeline: Delphi vs. poll forecast")
st.markdown("Line graph comparing prediciton from Delphi with poll per party over time (e.g. last week)")

# Mock data for chart
np.random.seed(2021)
N = 10
rng = pd.date_range(start='2021-08-16', end='2021-08-25')
df = pd.DataFrame(np.random.uniform(5, 20, size=(10,14)), columns=["CSU", "SPD", "Grünen", "FDP", "Linken", "AFD", "Others", "CSU_poll", "SPD_poll", "Grünen_poll", "FDP_poll", "Linken_poll", "AFD_poll", "Others_poll"], index=rng)
st.line_chart(df)

st.markdown("""---""")
col15, col16 = st.columns((3,1))

col15.markdown("## Twitter Insights")
col15.markdown("")
col15.markdown("")
col15.markdown("")


parties_select = ["All ", "CDU/CSU", "SPD", "Grünen", "FDP", "Linken", "AFD", "Others"]
col16.selectbox("Filter for party", parties_select)

#"Twitter Key Metrics")
col11, col12, col13, col14 = st.columns((1,1,1,1))



#Share of tweets per party
col11.markdown("**% Tweets per party**")
#share_of_tweets =twitter_kpis[0].get("share_of_tweets")
fig2 = plt.figure(figsize=(3,3),dpi=100)
label = ["Others", "Linken", "SPD", "Grünen", "FDP", "CDU/CSU", "AFD"]
val = [0.05, 0.05, 0.4, 0.1, 0.2, 0.1, 0.15]
colors = [
    party_color_dict.get(label[0], "white"),
    party_color_dict.get(label[1], "white"),
    party_color_dict.get(label[2], "white"),
    party_color_dict.get(label[3], "white"),
    party_color_dict.get(label[4], "white"),
    party_color_dict.get(label[5], "white"),
    party_color_dict.get(label[6], "white")]
ax2 = plt.pie(val, labels=label, colors=colors)
fig2.tight_layout()
buf = BytesIO()
fig2.savefig(buf, format="png", bbox_inches='tight')
col11.image(buf)

#Share of unique_users
col12.markdown("**% unique users**")
col12.markdown("")
#share_unique_users=twitter_kpis[0].get("share_unique_users")
chart_data = pd.DataFrame(np.array(val), index=label)
col12.bar_chart(chart_data, height=250)

#Share of positive Tweets
col13.markdown("**% positive Tweets**")
col13.markdown("")
#share_of_positive_tweets=twitter_kpis[0].get("share_of_positive_tweets")
chart_data = pd.DataFrame(np.array(val), index=label)
col13.bar_chart(chart_data, height=250)

#Share of negative Tweets
col14.markdown("**% negative Tweets**")
col14.markdown("")
#share_of_negative_tweets=twitter_kpis[0].get("share_of_negative_tweets")
chart_data = pd.DataFrame(np.array(val), index=label)
col14.bar_chart(chart_data, height=250)

#Expander per party with key metrics and tweets
#with st.expander("Most Likes 💙"):

#    st.subheader("Twitter Key Metrics")
#    col7, col8, col9, col10 = st.columns((1,1,1,1))

#    share_of_tweets =twitter_kpis[0].get("share_of_tweets")
#    col7.metric("Share of Tweets",f"{round(share_of_tweets,2)}%")

#    share_unique_users=twitter_kpis[0].get("share_unique_users")
#    col8.metric("Share of unique Users",f"{round(share_unique_users,2)}%")

#    share_of_positive_tweets=twitter_kpis[0].get("share_of_positive_tweets")
#    col9.metric("Share of positive Tweets",f"{round(share_of_positive_tweets,2)}%")

#    share_of_negative_tweets=twitter_kpis[0].get("share_of_negative_tweets")
#    col10.metric("Share of negative Tweets", f"{round(share_of_negative_tweets,2)}%")

st.markdown("""---""")

st.subheader("Todays most 💙 Tweets")
st.text("")
col3, col4,  = st.columns((1,1))
col31, col32, col33, col41, col42, col43 = st.columns((1,1,1,1,1,1))

# Positive Tweet
created_at = famous_tweets.get("pos_most_likes").get('tweet_created_at')[:10]
col3.write(f'**Dieter Bartsch** {created_at}')
col3.write(famous_tweets.get("pos_most_likes").get("text"))
no_likes = famous_tweets.get("pos_most_likes").get("public_metrics.like_count")
no_retweets = famous_tweets.get("pos_most_likes").get("public_metrics.retweet_count")
no_replys = famous_tweets.get("pos_most_likes").get('public_metrics.reply_count')
col31.write(f"🔁 {no_retweets}")
col32.write(f"💬 {no_replys}")
col33.write(f"💙 {no_likes}")


#Negative tweet
created_at = famous_tweets.get("neg_most_likes").get('tweet_created_at')[:10]
col4.write(f'**Anonym** {created_at}')
col4.write(famous_tweets.get("neg_most_likes").get("text"))
no_likes = famous_tweets.get("neg_most_likes").get("public_metrics.like_count")
no_retweets = famous_tweets.get("neg_most_likes").get("public_metrics.retweet_count")
no_replys = famous_tweets.get("neg_most_likes").get('public_metrics.reply_count')
col41.write(f"🔁 {no_retweets}")
col42.write(f"💬 {no_replys}")
col43.write(f"💙 {no_likes}")

st.text("")
st.text("")
st.markdown("""---""")
st.subheader("Todays most 🔁 Tweets")
st.text("")
col5, col6,  = st.columns((1,1))
col51, col52, col53, col61, col62, col63 = st.columns((1,1,1,1,1,1))

# Positive Tweet
created_at = famous_tweets.get("pos_most_rewteets").get('tweet_created_at')[:10]
col5.write(f'**Dieter Bartsch** {created_at}')
col5.write(famous_tweets.get("pos_most_rewteets").get("text"))
no_likes = famous_tweets.get("pos_most_rewteets").get("public_metrics.like_count")
no_retweets = famous_tweets.get("pos_most_rewteets").get("public_metrics.retweet_count")
no_replys = famous_tweets.get("pos_most_rewteets").get('public_metrics.reply_count')
col51.write(f"🔁 {no_retweets}")
col52.write(f"💬 {no_replys}")
col53.write(f"💙 {no_likes}")


#Negative tweet
created_at = famous_tweets.get("neg_most_retweets").get('tweet_created_at')[:10]
col6.write(f'**Anonym** {created_at}')
col6.write(famous_tweets.get("neg_most_retweets").get("text"))
no_likes = famous_tweets.get("neg_most_retweets").get("public_metrics.like_count")
no_retweets = famous_tweets.get("neg_most_retweets").get("public_metrics.retweet_count")
no_replys = famous_tweets.get("neg_most_retweets").get('public_metrics.reply_count')
col61.write(f"🔁 {no_retweets}")
col62.write(f"💬 {no_replys}")
col63.write(f"💙 {no_likes}")


# continue loading the data with your excel file, I was a bit too lazy to build an Excel file :)
df = pd.DataFrame(
    [["Product A", 5.6, 7.8, 5], ["Product B", 5.8, 7.2, 4.9]],
    columns=["Product", "Comfort", "Sound", "Calls"]
)
