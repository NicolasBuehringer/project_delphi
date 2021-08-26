#Imports
import matplotlib.pyplot as plt
import streamlit as st
import requests

#Set page layout to wide
st.set_page_config(layout="wide")

'''
# German Federal Election forecast
'''

url = "https://delphi-xq2dtozlga-ew.a.run.app/"

response = requests.get(url).json()
prediction = response["greeting"]
st.markdown(prediction)

'''
## Diagram
'''
col1, col2,  = st.columns((1,1))

# data
label = ["CDU/CSU", "SPD", "Grünen", "FDP", "Linken", "AFD"]
val = [0.25,.25,0.3, 0.1, 0.05, 0.05]

# append data and assign color
label.append("")
val.append(sum(val))  # 50% blank
colors = ['black', 'red', 'green', 'yellow', "purple", "blue"]

fig1 = plt.figure(figsize=(8,6),dpi=100)
#ax1 =

# plot
#ax1.figure(figsize=(8,6),dpi=100)

wedges, labels=plt.pie(val, wedgeprops=dict(width=0.4,edgecolor='w'),labels=label, colors=colors)
# I tried this method
wedges[-1].set_visible(False)

col1.markdown("Our prediction")
col1.pyplot(fig1)
col2.markdown("Some random text")
