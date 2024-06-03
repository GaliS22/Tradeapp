import pandas as pd
import seaborn as sns
import streamlit as st
import comtradeapicall as un
import datetime as dt
import json
import functions as fc  # Assuming fc contains the find_country_code function

# Load Country Codes
CountryCode = pd.read_csv(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\CountryCodes.csv', encoding='latin1')

st.write("UNCOMTRADE TRADE PARTNERS DASHBOARD PREVIEW")

flow = st.selectbox('Trade Flow: ', ['Import', 'Export'])

report_country = st.selectbox('Reporting Country: ', CountryCode['text'])

trade_country = st.selectbox('Trade Partner: ', CountryCode['text'])

# Load HS Codes
with open('HS_CODE.json', 'r') as file:
    df_hs = json.load(file)

# Convert JSON data to DataFrame
df = pd.json_normalize(df_hs)

hs_code = st.multiselect('HS Code: ', df['text'])

today = dt.datetime.now()
old_year = dt.date.fromisoformat('2000-12-04').year
jan_1 = dt.date(old_year, 1, 1)
dec_31 = dt.date(today.year, 12, 31)

date_range = st.date_input(
    "Select range",
    (jan_1, dt.date(today.year, 1, 1)),
    jan_1,
    dec_31,
    format="DD.MM.YYYY",
)

# Fetch data button
if st.button('Fetch Data'):
    # Get the codes for the selected countries
    reporter_code = fc.find_country_code(report_country)
    partner_code = fc.find_country_code(trade_country)

    # Handle the case where multiple HS codes are selected
    if hs_code:
        cmd_code = df.loc[df['text'].isin(hs_code), 'code'].tolist()  # Convert HS codes to a list of command codes
        cmd_code_str = ','.join(map(str, cmd_code))
    else:
        cmd_code_str = '91'  # Default HS code if none are selected

    # Ensure period is in the correct format (e.g., YYYYMM)
    period = dt.date(date_range[0].year, date_range[0].month, 1).strftime('%Y%m')

    try:
        # Fetch data from the API
        data = un.previewFinalData(
            typeCode='C',
            freqCode='M',
            clCode='HS',
            period=period,
            reporterCode=reporter_code,
            cmdCode=cmd_code_str,
            flowCode='M',
            partnerCode=partner_code,
            partner2Code=None,
            customsCode=None,
            motCode=None,
            maxRecords=500,
            format_output='JSON',
            aggregateBy=None,
            breakdownMode='classic',
            countOnly=None,
            includeDesc=True
        )

        # Display the fetched data
        st.write(data)
    except Exception as e:
        st.error(f"An error occurred: {e}")
