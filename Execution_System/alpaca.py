import requests
import alpaca_trade_api as tradeapi
import pandas as pd
import json

APCA_API_KEY_ID = 'PKFKM6KPI1COLEQEMB7Y'
APCA_API_SECRET_KEY = 'GWDe2JErqsrB3A6ScplTdaWjDLelqKNl5Gmz3zcW'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url = APCA_API_BASE_URL)
account = api.get_account()
account.status
assets = api.list_assets()
type(assets)
datalist = []
for i in range(0, len(assets)):
    datalist.append([assets[i].symbol, assets[i].name, assets[i].status, assets[i].tradable])

asset_df = pd.DataFrame(datalist, columns = ['Symbol', 'Name', 'Status', 'Tradable'])
asset_df.set_index('Symbol', inplace = True)

asset_df.loc['GME']

NY = 'America/New_York'
start = pd.Timestamp('2020-08-01', tz = NY).isoformat()
end = pd.Timestamp('2020-08-30', tz = NY).isoformat()
data = api.get_barset(['GME', 'AMC', 'BB'], 'day', start = start, end = end).df
data.head()
