import sqlite3 as sql
import requests
from io import StringIO
import pandas
import apikey
# import config

API_URL = 'https://www.alphavantage.co/query'


def get_historical_data_for_ticker(symbol, function='TIME_SERIES_DAILY_ADJUSTED', outputsize='compact'):
    parameters = {
        'function': function,
        'symbol': symbol,
        'outputsize': outputsize,
        'datatype': 'csv',
        'apikey': apikey.API_KEY
    }

    response = requests.get(API_URL, params=parameters)
    if response.status_code == 200:
        cols = pandas.read_csv(StringIO(response.text))
        cols.insert(0, 'Ticker', symbol)
        return cols
    else:
        raise RequestFailed("Status_code was not 200")


# ticker = input("Input a ticker\n")

# csv_file = get_historical_data_for_ticker(ticker, apikey.API_KEY, outputsize='full')

# print(csv_file)
