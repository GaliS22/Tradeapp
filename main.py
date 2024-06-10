import pandas as pd
import seaborn as sns
import streamlit as st
import comtradeapicall as un
import datetime as dt
import functions as fc
import json
import requests
import matplotlib.pyplot as plt

st.markdown(
    """
    <style>
    .main {
        background: url("https://www.czarnikow.com/wp-content/uploads/2020/12/freightliner-1182x810.png");
        background-size: cover;
        color: white;
    }
    h1 {
        color: #FF8C00;  /* Darker orange color */
        text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;  /* Black outline */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Load Country Codes
CountryCode = pd.read_csv(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\CountryCodes.csv', encoding='latin1')

# Custom title with darker orange color
st.markdown(
    """
    <h1>UNCOMTRADE TRADE PARTNERS DATA</h1>
    """,
    unsafe_allow_html=True
)
# Load HS Codes
with open(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\HS_CODE.json', 'r') as file:
    df_hs = json.load(file)

# Convert JSON data to DataFrame
df = pd.json_normalize(df_hs)

# Year and month range selection
today = dt.datetime.now()
years = list(range(2010, today.year + 1))
months = list(range(1, 13))

flow = st.selectbox('Trade Flow: ', ['Import', 'Export'])

col1, col2 = st.columns(2)

# Trade Flow selection
with col1:

# Reporting and Trade Partner Country selection
    report_country = st.selectbox('Reporting Country: ', CountryCode['text'])
    start_month = st.selectbox('Start Month', months)
    end_month = st.selectbox('End Month', months)


with col2:
    trade_country = st.selectbox('Trade Partner: ', CountryCode['text'])
    start_year = st.selectbox('Start Year', years)
    end_year = st.selectbox('End Year', years)

# Combine year and month to form period
start_period = f"{start_year}{start_month:02d}"
end_period = f"{end_year}{end_month:02d}"

# Map flow to the appropriate flow code
flow_dict = {'Import': 'M', 'Export': 'X'}
flow_code = flow_dict[flow]
reporter_code = str(fc.find_country_code(report_country))
partner_code = str(fc.find_country_code(trade_country))

periods = fc.generate_periods(start_period, end_period)

# HS Code selection
hs_code_desc = st.multiselect('Choose Specific HS Codes or Products: ', df['text'])


# Function to find HS codes
def find_hs(descriptions):
    hs_codes = []
    for desc in descriptions:
        if desc in df['text'].values:
            hs_code = df.loc[df['text'] == desc, 'id'].values[0]
            hs_codes.append(hs_code)
    return ','.join(hs_codes) if hs_codes else ''


# Convert HS code descriptions to HS codes
hs_code = find_hs(hs_code_desc)

# Fetch and display data from UN Comtrade
if st.button('Fetch UN Comtrade Data'):
    try:
        data = un.previewFinalData(
            typeCode='C',
            freqCode='M',
            clCode='HS',
            period=periods,
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
        st.write(data)
        df_data = pd.DataFrame(data)
        if not df_data.empty:
            fig, ax = plt.subplots()
            sns.lineplot(data=df_data, x='period', y='fobvalue', hue="cmdCode", ax=ax)
            ax.set_title(f'{report_country} and {trade_country} -{flow}s')
            plt.xticks(rotation=45)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")