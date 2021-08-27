#Imports
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import requests
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

# Current poll from DAWUM API OR Delphi API
# Dummy values (to be updated)
AFD_poll = 10.61
CDU_poll = 21.97
FDP_poll = 10.33
GRUENE_poll = 19.69
LINKE_poll = 7.11
SPD_poll = 19.59
OTHER_poll = 10.7

# Engineered Twitter Feautres (KPIs) via Delphi API

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
using a state-of-the art deep learning algorithm trained on current polls and Twitter data.
'''


'''
## Delphi model forecast vs. current poll
'''
col1, col2,  = st.columns((1,1))

# data
label = ["Others", "Linken", "SPD", "Grünen", "FDP", "CDU/CSU", "AFD"]
val = [OTHER_forecast, LINKE_forecast, SPD_forecast, GRUENE_forecast, FDP_forecast, CDU_forecast, AFD_forecast]
# append data and assign color
label.append("")
val.append(sum(val))  # 50% blank
colors = ['grey', 'purple', 'red', 'green', "yellow", "black", "blue"]

#Create plot
fig1 = plt.figure(figsize=(8,6),dpi=100)
wedges, labels=plt.pie(val, wedgeprops=dict(width=0.4,edgecolor='w'), labels=label, colors=colors)
wedges[-1].set_visible(False)

col1.subheader("Delphi model forecast")
col1.pyplot(fig1)
col2.subheader("#Current poll as of XX.XX.XXXX")
col2.markdown("Some random text about our forecast")


# Ideas for dashboard
## Show our poll forecast in comparison to the most recent poll (can just call the other api)
## Show possible cooalitionen based on the scores per party
## Show engineered twitter feature per party per day
## Show most liked/ retweeted positive and negative tweet per party

'''
## Most popular tweets
'''

with st.expander('Most Likes'):
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

with st.expander('Most Retweets'):
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

#fig = px.bar(df, x="Product", y=["Comfort", "Sound", "Calls"], barmode='group', height=400)
# st.dataframe(df) # if need to display dataframe
#st.plotly_chart(fig)
