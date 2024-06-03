import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import comtradeapicall as un
import datetime as dt
import functions as fc
import json



CountryCode = pd.read_csv(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\CountryCodes.csv', encoding='latin1')

st.write("UNCOMTRADE TRADE PARTNERS DASHBOARD PREVIEW")

flow = st.selectbox('Trade Flow: ', ['Import','Export'])

report_country = st.selectbox('Reporting Country: ', CountryCode.text)

trade_country = st.selectbox('Trade Partner: ', CountryCode.text)

with open('HS_CODE.json', 'r') as file:
    df_hs = json.load(file)

# Convert JSON data to DataFrame
df = pd.json_normalize(df_hs)

hs_code = st.multiselect('HS Code: ',df.text)

today = dt.datetime.now()
old_year= dt.date.fromisoformat('2000-12-04').year
jan_1= dt.date(old_year, 1,1)
dec_31 = dt.date(today.year, 12,31)

d= st.date_input( "Select range",
    (jan_1, dt.date(today.year, 1,1)),
    jan_1,
    dec_31,
    format="DD.MM.YYYY",)


df=pd.DataFrame(un.previewFinalData(typeCode='C', freqCode='M', clCode='HS', period='202205',
                                        reporterCode=fc.find_country_code(report_country), cmdCode='91', flowCode='M', partnerCode=fc.find_country_code(trade_country),
                                        partner2Code=None,
                                        customsCode=None, motCode=None, maxRecords=500, format_output='JSON',
                                        aggregateBy=None, breakdownMode='classic', countOnly=None, includeDesc=True))
