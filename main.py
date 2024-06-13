import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import comtradeapicall as un
import datetime as dt
import functions as fc
import json
import os

# Define the base directory for relative paths
base_dir = os.path.dirname(__file__)
country_code_path = os.path.join(base_dir, 'data', 'CountryCodes.csv')
hs_code_path = os.path.join(base_dir, 'data', 'HS_CODE.json')

st.markdown(
    """
    <style>
    .main {
        background: url("https://www.shutterstock.com/image-photo/aerial-drone-photo-huge-container-600nw-1840604107.jpg");
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
CountryCode = pd.read_csv(country_code_path, encoding='latin1')

# Custom title with color
st.markdown(
    """
    <h1>UN COMTRADE TRADE PARTNERS DATA</h1>
    """,
    unsafe_allow_html=True
)
# Load HS Code Data
with open(hs_code_path, 'r') as file:
    df_hs = json.load(file)

# Convert JSON data to DataFrame
df = pd.json_normalize(df_hs)

# Year and month range selection
today = dt.datetime.now()
years = list(range(2010, today.year))
months = list(range(1, 13))

# Choose Import or Export
flow = st.selectbox(':orange[Trade Flow: ]', ['Import', 'Export'])

# Design of layout
col1, col2 = st.columns(2)


with col1:

    # col1 - Selection of reporing country start and end month
    report_country = st.selectbox(':orange[Reporting Country: ]', CountryCode['text'])
    start_month = st.selectbox(':orange[Start Month]', months)
    end_month = st.selectbox(':orange[End Month]', months)


with col2:
    # col2 - Selection of trade country start and end year
    trade_country = st.selectbox(':orange[Trade Partner: ]', CountryCode['text'])
    start_year = st.selectbox(':orange[Start Year]', years)
    end_year = st.selectbox(':orange[End Year]', years)

# Combine year and month to form period
start_period = f"{start_year}{start_month:02d}"
end_period = f"{end_year}{end_month:02d}"

# Map flow to the appropriate flow code
flow_dict = {'Import': 'M', 'Export': 'X'}
flow_code = flow_dict[flow]

# Code from functions class to find country codes of selected countries
reporter_code = str(fc.find_country_code(report_country))
partner_code = str(fc.find_country_code(trade_country))

# creating range of dates list using function from functions class
periods = fc.generate_periods(start_period, end_period)

# HS Code multiple selection
hs_code_desc = st.multiselect(':orange[Choose Specific HS Codes or Products:] ', df['text'])


# Convert HS code descriptions to HS codes
hs_code = fc.find_hs(hs_code_desc)

# Obtain from UN Comtrade API
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
        ).head(500)
        
        df_data = pd.DataFrame(data)
        st.write(df_data[['period', 'reporterDesc', 'flowDesc', 'partnerDesc', 'cmdCode', 'fobvalue', 'cifvalue']].drop_duplicates())

        # Creating Visualizations
        if not df_data.empty:

            # Set the dark theme
            sns.set_theme(style="darkgrid")
            plt.style.use('dark_background')

            # Creating Visualizations
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.lineplot(data=df_data, x='period', y='fobvalue', hue='cmdCode', ax=ax)
            ax.set_title(f'{report_country}: {trade_country} - FOB Value of {flow}s of {hs_code_desc} in US$', fontsize=18, color='white')
            ax.set_xlabel('Time', fontsize=14, color='white')
            ax.set_ylabel('Trade Value (excluding shipping and insurance)', fontsize=14, color='white')
            plt.xticks(rotation=45, fontsize=14, color='white')
            plt.yticks(color='white')

            formatter = lambda x, _: f'{int(x):,}'
            ax.yaxis.set_major_formatter(formatter)

            st.pyplot(fig)

            fig2, ax2 = plt.subplots(figsize=(12, 8))
            sns.lineplot(data=df_data, x='period', y='cifvalue', hue='cmdCode', ax=ax2)
            ax2.set_title(f'{report_country}: {trade_country} - CIF Value of {flow}s of {hs_code_desc} in US$', fontsize=18, color='white')
            ax2.set_xlabel('Time', fontsize=14, color='white')
            ax2.set_ylabel('Trade Value (including taxes, shipping, and insurance)', fontsize=14, color='white')
            plt.xticks(rotation=45, fontsize=14, color='white')
            plt.yticks(color='white')

            ax2.yaxis.set_major_formatter(formatter)
            st.pyplot(fig2)
    except Exception as e:
        st.write("The maximum number of records (500) has been reached")
