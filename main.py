import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import comtradeapicall as un
import datetime as dt
import functions as fc
import json

# Load Country Codes
CountryCode = pd.read_csv(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\CountryCodes.csv', encoding='latin1')

st.write("UNCOMTRADE TRADE PARTNERS DASHBOARD PREVIEW")

# Trade Flow selection
flow = st.selectbox('Trade Flow: ', ['Import', 'Export'])

# Map flow to the appropriate flow code
flow_dict = {'Import': 'M', 'Export': 'X'}
flow_code = flow_dict[flow]

# Reporting and Trade Partner Country selection
report_country = st.selectbox('Reporting Country: ', CountryCode['text'])
trade_country = st.selectbox('Trade Partner: ', CountryCode['text'])

# Load HS Codes
with open(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\HS_CODE.json', 'r') as file:
    df_hs = json.load(file)

# Convert JSON data to DataFrame
df = pd.json_normalize(df_hs)

# HS Code selection
hs_code_desc = st.multiselect('HS Code: ', df['text'])

# Convert HS code descriptions to HS codes
hs_code = fc.find_hs(hs_code_desc)

# Date range selection
today = dt.datetime.now()
old_year = dt.date.fromisoformat('2015-12-04').year
jan_1 = dt.date(old_year, 1, 1)
dec_31 = dt.date(today.year, 12, 31)

# Date input with the correct format
d = st.date_input('Select date', jan_1)
d_format = d.strftime('%Y%m')


# Get the country codes for the selected countries
reporter_code = str(fc.find_country_code(report_country))
partner_code = str(fc.find_country_code(trade_country))

# Fetch data when the button is clicked
if st.button('Fetch Data'):
    try:
        data = un.previewFinalData(
            typeCode='C',
            freqCode='M',
            clCode='HS',
            period=d_format,
            reporterCode=reporter_code,
            cmdCode=hs_code,
            flowCode=flow_code,
            partnerCode=partner_code,
            partner2Code=None,
            customsCode=None,
            motCode=None,
            maxRecords=500,
            format_output='JSON',
            countOnly=None,
            includeDesc=True
        )

        # Display the fetched data
        st.dataframe(data)
    except Exception as e:
        st.error(f"An error occurred: {e}")
