import pandas as pd
import seaborn as sns
import numpy as py
import streamlit as st
import comtradeapicall as un
import requests
st.write("UNCOMTRADE TRADE PARTNERS DASHBOARD")
df= pd.DataFrame("CountryCodes.csv")
st.selectbox("choose country: ",df.reporterDesc)

print(result)

