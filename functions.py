import pandas as pd
import numpy as np


df= pd.read_csv(r'C:\Users\Galis\Documents\GitHub\Uncomtrade\CountryCodes.csv', encoding='latin1')

code = ''

def find_country_code(country_name):
    if country_name in df['text'].values:
        code = df.loc[df['text'] == country_name, 'reporterCode'].values[0]
        return code
    else:
        return None



print(find_country_code('France'))




