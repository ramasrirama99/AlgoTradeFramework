import requests
from io import StringIO
import pandas
from fileio import apikey
import csv

API_URL = 'https://www.alphavantage.co/query'

def get_data_for_symbol(parameters):
    response = requests.get(API_URL, params=parameters)
    if response.status_code == 200:
        csv_file = StringIO(response.text)
        tuple_data_list = [tuple(line) for line in csv.reader(csv_file)]
        return tuple_data_list
    else:
        print('Status_code not 200')
        return None


def get_historical_data(symbol, outputsize='compact'):
    parameters = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'outputsize': outputsize,
        'datatype': 'csv',
        'apikey': apikey.API_KEY
    }

    get_data_for_symbol(parameters);



def get_intraday_data(symbol, interval='1min', outputsize='compact'):
    parameters = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval' : interval,
        'outputsize': outputsize,
        'datatype': 'csv',
        'apikey': apikey.API_KEY
    }

    get_data_for_symbol(parameters);

symbol = input("Enter a symbol: ")
get_historical_data(symbol)