#Imports
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
st.text(prediction)
