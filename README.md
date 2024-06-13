# Uncomtrade

UN Comtrade Trade Partners Data Viewer

Overview
The UN Comtrade Trade Partners Data Viewer is a Streamlit-based application.
It allows you to look at the trade and trade value(CIF - including shipping and insurance costs or FOB - excluding shipping and insurance costs) of two countries based on the following parameters:
- Import or export
- Reporting country (importing or exporting country)
- Trade partner
- Range of dates: months and years(from 2010 until 2023)
- one or more product by search term/scroll down or HS CODE (Harmonized code 2,4, 6- a standardized numerical method of classifying traded products globally )

The result: Click the "Fetch UN Comtrade Data" button to fetch and display the following data.:
- A detailed table of the trade information
- a visualization depicting trade value in US$ of chosen products during the period of time chosen

The Data:
- Based on UN Comtrade - The United Nations Comtrade database aggregates detailed global annual and monthly trade statistics by product and trading partner for use by governments, academia, research institutes, and enterprises. Data compiled by the United Nations Statistics Division covers approximately 200 countries and represents more than 99% of the world's merchandise trade.
- The data is obtained using their API python package

Functions Class:
- special functions to convert the selected data into th API format:
  - find_country_code
  - find_hs
  - generate_periods


Attention:
* If product is not selected all products will appear
* Sometimes the cif value is null or fob value is null (depends on countries and whether it is import/export)
* This API can extract up to 500 records. If there are more an error will appear

License
This project is licensed under the MIT License. See the LICENSE file for details.

Examples:
1. Exports from China to USA of Vacuum Cleaners (8508) 07/2022-04-2023
2. Imports to Israel from Colombia of Fish and Coffee (03, 090111) 03/2019-05/2019
3. Imports to France from Morocco of Onions (0703) 08/2021-03/2022

