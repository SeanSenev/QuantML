### STEPS FOR MOVING AVERAGE TRADES
# SETUP API
# GRAB LIST OF POSITIONS
# GRAB LIST OF ALL ASSETS
# FILTER LIST FOR ACTIVE STOCKS
# GRAB PREVIOUS DAY O,H,L,C,V
# FILTER LIST FOR LOW ENOUGH COST STOCKS
# GRAB PRICE HISTORY FOR LIST OF STOCKS
	# PUT EACH STOCK INTO SEPARATE DATAFRAME
# CALCULATE 5 DAY AND 30 DAY AVERAGE
# IF 5 DAY > 30 DAY -> BUY
	# IF NOT -> SELL OR IGNORE

# UPDATES: EVENTUALLY CHANGE ALPACA_TRADE_API TO V 1.0

import requests
import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

APCA_API_KEY_ID = 'PKFKM6KPI1COLEQEMB7Y'
APCA_API_SECRET_KEY = 'GWDe2JErqsrB3A6ScplTdaWjDLelqKNl5Gmz3zcW'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

# Setting up API and account details
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url = APCA_API_BASE_URL, api_version = 'v2')
account = api.get_account()
account.status
api.list_positions()

# Getting all assets
assets = api.list_assets()#status = "active", asset_class = "us_equity")
assets[0]

datalist = []
# for i in range(0, len(assets)):
for counter, value in enumerate(assets):
    datalist.append([assets[counter].symbol, assets[counter].name, assets[counter].status, assets[counter].tradable, assets[counter].easy_to_borrow]) # Append all data to list
datalist

# Maybe can skip this stuff with updated list assets
asset_df = pd.DataFrame(datalist, columns = ['symbol', 'name', 'status', 'tradable', 'easy_to_borrow']) # Create dataframe from list of stock data
asset_df.set_index('symbol', inplace = True) # Set index of dataframe to Symbol
# asset_df.index.values[0:10]
canTrade = asset_df[asset_df['tradable'] == True] # Check if asset is tradable
canTrade
canTradeNumber = len(canTrade)
canTradeNumber

trial = canTrade[0:10]

# NOT WORKING - Update: For every asset get one day bar, put into list, make list into DF

api.get_bars("AAPL", TimeFrame.Hour, "2021-02-08", "2021-0208", limit = 10, adjustment = 'raw')

bar_iter = api.get_bars_iter("AAPL", TimeFrame.Hour, "2021-02-08", "2021-02-08", limit=10, adjustment='raw')
aapl
barsets
type(aapl)

stonklist = {}
for counter, value in enumerate(trial.index):
	# stonklist.append(api.get_barset(trial.index[counter], 'day', start = end, end = end)._raw)
	stonklist|api.get_barset(trial.index[counter], 'day', start = end, end = end)._raw
stonklist
stonkdf = pd.DataFrame.from_dict(stonklist)#, columns = ['symbol', 'close', 'high', 'low', 'open', 't', 'volume'])
stonkdf

# Setting up times
NY = 'America/New_York'
start = pd.Timestamp('2021-02-01', tz = NY).isoformat() # Update with get current time stamp maybe
end = pd.Timestamp('2021-02-26', tz = NY).isoformat()
minus_time = (pd.Timestamp('2021-02-26', tz = NY) - pd.Timedelta(150, unit = 'D')).isoformat()
yesterday = (api.get_clock().timestamp.date() - pd.Timedelta(1, unit = 'D')).isoformat()

# Grabbing open, high, low, close, volume intro dataframe
counter = 0
data = api.get_barset(canTrade.index[counter:counter+99], 'day', start = end, end = end).df # Update: find way to get all tickers in list (can do max 100)
data.head()
melted = pd.melt(data) # reshape dataframe to be more stacked
melted.head()
goodTable = melted.pivot(index = "variable_0", columns = "variable_1", values = "value") # format dataframe to look good
goodTable = goodTable.rename_axis("ticker")
goodTable = goodTable.rename_axis("stats", axis = "columns")
goodTable.head()
len(goodTable)

# Find assets under max price with min daily volume
tradeWorthy = goodTable[(goodTable['close'] < 50) & (goodTable['volume'] > 100000)] # Edit these values for what reasonable
len(tradeWorthy)
tradeWorthy.head()


aapl_data = api.get_barset('AAPL', 'day', start = minus_time, end = end).df
aapl_data

# Simple Moving Average Calculations
fiveDayMA = aapl_data['AAPL']['close'].rolling(5).mean()[99] # Update: Get last index programatically
fiftyDayMA = aapl_data['AAPL']['close'].rolling(50).mean()[99]

if fiveDayMA > fiftyDayMA:
	api.submit_order(
		symbol = 'AAPL',
		side = 'buy',
		type = 'market',
		qty = '50', # Do some calculation to get max amount under some percentage of current cash
		time_in_force = 'day'
	)
