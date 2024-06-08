import pandas as pd
import json


def find_country_code(country_name):
    country_code_df = pd.read_csv(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\CountryCodes.csv', encoding='latin1')
    country_code = country_code_df.loc[country_code_df['text'] == country_name, 'id'].values[0]
    return country_code


with open(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\HS_CODE.json', 'r') as file:
    df_hs = pd.json_normalize(json.load(file))


def find_hs(descriptions):
    hs_codes = []
    for desc in descriptions:
        if desc in df_hs['text'].values:
            hs_code = df_hs.loc[df_hs['text'] == desc, 'id'].values[0]
            hs_codes.append(hs_code)
    # Join the HS codes into a comma-separated string if multiple HS codes are selected
    hs_codes = ','.join(hs_codes) if hs_codes else ''
    return hs_codes
