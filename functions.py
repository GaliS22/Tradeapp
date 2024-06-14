import pandas as pd
import json
import datetime as dt
import os

# Define the base directory for relative paths
base_dir = os.path.dirname(__file__)
country_code_path = os.path.join(base_dir, 'data', 'CountryCodes.csv')
hs_code_path = os.path.join(base_dir, 'data', 'HS_CODE.json')

# Function to find country code
def find_country_code(country_name):
    country_code_df = pd.read_csv(country_code_path, encoding='latin1')
    country_code = country_code_df.loc[country_code_df['text'] == country_name, 'id'].values[0]
    return country_code

# Load HS Code Data

with open(hs_code_path, 'r') as file:
    df_hs = pd.json_normalize(json.load(file))

# Function to find HS codes and create list
def find_hs(descriptions):
    hs_codes = []
    for desc in descriptions:
        if desc in df_hs['text'].values:
            hs_code = df_hs.loc[df_hs['text'] == desc, 'id'].values[0]
            hs_codes.append(hs_code)
    # Join the HS codes into a comma-separated string if multiple HS codes are selected
    hs_codes = ','.join(hs_codes) if hs_codes else ''
    return hs_codes

# Function to generate periods
def generate_periods(start, end):
    periods = []
    start_date = dt.datetime.strptime(start, "%Y%m")
    end_date = dt.datetime.strptime(end, "%Y%m")
    while start_date <= end_date:
        periods.append(start_date.strftime("%Y%m"))
        start_date += pd.DateOffset(months=1)
    return ','.join(periods)

