import csv, requests

from datetime import datetime
from io import StringIO

from fileio import apikey

API_URL = 'https://www.alphavantage.co/query'


def create_tuple(csv_file):
    tuple_data_list = []
    for i, line in enumerate(csv.reader(csv_file)):
        row = []
        for j, elem in enumerate(line):

            if i == 0:
                row.append(elem)

            elif j == 0:
                row.append(datetime.strptime(elem, '%Y-%m-%d').date())

            else:
                row.append(float(elem))

        tuple_data_list.append(tuple(row))
    return tuple_data_list


def get_data_for_symbol(parameters):
    response = requests.get(API_URL, params=parameters)
    if response.status_code == 200:
        csv_file = StringIO(response.text)
        return create_tuple(csv_file)

    else:
        print('Status_code not 200')
        return None


def get_daily_adjusted(symbol, outputsize='compact'):
    parameters = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'outputsize': outputsize,
        'datatype': 'csv',
        'apikey': apikey.API_KEY
    }

    return get_data_for_symbol(parameters);



def get_intraday(symbol, interval='1min', outputsize='compact'):
    parameters = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval' : interval,
        'outputsize': outputsize,
        'datatype': 'csv',
        'apikey': apikey.API_KEY
    }

    return get_data_for_symbol(parameters);