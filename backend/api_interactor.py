import requests
from io import StringIO
import pandas
from backend.fileio import apikey

API_URL = 'https://www.alphavantage.co/query'


def get_historical_data_for_ticker(ticker, function='TIME_SERIES_DAILY_ADJUSTED', outputsize='compact'):
    parameters = {
        'function': function,
        'ticker': ticker,
        'outputsize': outputsize,
        'datatype': 'csv',
        'apikey': apikey.API_KEY
    }

    response = requests.get(API_URL, params=parameters)
    if response.status_code == 200:
        cols = pandas.read_csv(StringIO(response.text))
        cols.insert(0, 'Ticker', ticker)
        return cols
    else:
        print('Status_code not 200')


def get_intraday_data(ticker, function='TIME_SERIES_INTRADAY', outputsize='compact'):
    parameters = {
        'function': function,
        'ticker': ticker,
        'outputsize': outputsize,
        'datatype': 'csv',
        'apikey': apikey.API_KEY
    }

    response = requests.get(API_URL, params=parameters)
    if response.status_code == 200:
        cols = pandas.read_csv(StringIO(response.text))
        cols.insert(0, 'Ticker', ticker)
        return cols
    else:
        print('Status_code not 200')

# ticker = input("Input a ticker\n")

# csv_file = get_historical_data_for_ticker(ticker, apikey.API_KEY, outputsize='full')

# print(csv_file)
