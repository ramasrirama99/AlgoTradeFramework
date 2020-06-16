import csv
import requests
import yfinance as yf
from datetime import datetime, timedelta
from io import StringIO
from tda import auth, client
from algotaf.backend.fileio import apikey
from algotaf.backend.fileio import tdam_keys
from algotaf.other.benchmark import Benchmark
from algotaf.backend.apis.tdam import authenticate_client

API_URL = 'https://www.alphavantage.co/query'
BENCH = Benchmark()


def create_tuple_csv(csv_file, timestamp_type):
    """
    Creates list of tuples of data from CSV file
    :param csv_file: CSV file of API call data
    :param timestamp_type: date or datetime
    :return: List of tuples of data
    """

    tuple_data_list = []

    for i, line in enumerate(csv.reader(csv_file)):
        row = []

        for j, elem in enumerate(line):

            if i == 0:
                row.append(elem)
            elif j == 0:
                if timestamp_type == 'date':
                    row.append(datetime.strptime(elem, '%Y-%m-%d').date())
                elif timestamp_type == 'datetime':
                    row.append(datetime.strptime(elem, '%Y-%m-%d %H:%M:%S'))
            else:
                row.append(float(elem))

        tuple_data_list.append(tuple(row))

    return tuple_data_list


def create_tuple_json(data, timestamp_type):
    tuple_data_list = []
    for i, record in enumerate(data):
        row = []
        row.append(datetime.fromtimestamp(record['datetime']/1000.0))
        row.append(record['open'])
        row.append(record['high'])
        row.append(record['low'])
        row.append(record['close'])
        row.append(record['volume'])
        if timestamp_type == client.Client.PriceHistory.FrequencyType.DAILY:
            row.append(datetime.fromtimestamp(record['datetime']/1000.0).date())
        elif timestamp_type == client.Client.PriceHistory.FrequencyType.EVERY_MINUTE:
            row.append(datetime.fromtimestamp(record['datetime']/1000.0))
        tuple_data_list.append(tuple(row))
    return tuple_data_list


def create_tuple_pandas(data, timestamp_type, bulk=False, tickers=[]):
    columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
    if bulk:
        all_actions = []
        all_data_list = []
        for stock in tickers:
            stock_records = data[stock.upper()]
            tuple_data_list = []
            actions = {'Dividends': True, 'Stock Splits': True}
            for i, record in stock_records.iterrows():
                row = []
                if timestamp_type == '1d':
                    row.append(i.to_pydatetime().date())
                elif timestamp_type == '1m':
                    row.append(i.to_pydatetime())
                for col in columns:
                    if col in record:
                        row.append(record[col])
                    else:
                        actions[col] = False
                tuple_data_list.append(tuple(row))
            all_actions.append(actions)
            all_data_list.append(tuple_data_list)
        return all_data_list, all_actions
    else:
        actions = {'Dividends': True, 'Stock Splits': True}
        tuple_data_list = []
        for i, record in data.iterrows():
            row = []
            if timestamp_type == '1d':
                row.append(i.to_pydatetime().date())
            elif timestamp_type == '1m':
                row.append(i.to_pydatetime())
            for col in columns:
                if col in record:
                    row.append(record[col])
                else:
                    actions[col] = False
            tuple_data_list.append(tuple(row))
        return tuple_data_list, actions


def get_data_yfinance(parameters, bulk=False):
    data = yf.download(tickers=parameters['symbols'],
        period=parameters['period'],
        interval=parameters['interval'],
        group_by=parameters['group_by'],
        auto_adjust=parameters['auto_adjust'],
        prepost=parameters['prepost'],
        threads=parameters['threads'],
        proxy=parameters['proxy'],
        actions=parameters['actions'])
    return create_tuple_pandas(data, parameters['interval'], bulk=bulk, tickers=parameters['symbols'])


def get_data_alphavantage(parameters, timestamp_type):
    """
    Get data from API call given the following parameters
    :param parameters: API call parameters
    :param timestamp_type: date or datetime
    :return: List of tuples of data
    """

    BENCH.mark('API call')

    response = requests.get(API_URL, params=parameters)

    BENCH.mark('API call')

    if response.status_code == 200:

        BENCH.mark('Convert to csv')

        csv_file = StringIO(response.text)

        BENCH.mark('Convert to csv')

        BENCH.mark('Convert to tuple')

        tuple_data_list = create_tuple_csv(csv_file, timestamp_type)

        BENCH.mark('Convert to tuple')

        return tuple_data_list
    else:
        print('Status_code not 200')
        return None


def get_data_tdameritrade(parameters):
    c = authenticate_client(tdam_keys.TOKEN_PATH, tdam_keys.CLIENT_ID, tdam_keys.REDIRECT_URL)
    r = c.get_price_history(parameters['symbol'],
        period_type=parameters['period_type'],
        period=parameters['period'],
        frequency_type=parameters['frequency_type'],
        frequency=parameters['frequency'])
    assert r.ok, r.raise_for_status()
    data = r.json()
    return create_tuple_json(data['candles'], parameters['frequency_type'])


def get_daily_adjusted(symbol, api_name, bulk=False):
    """
    Get data from API call for daily data
    :param symbol: Symbol name
    :param outputsize: Output size of API data
    :return: List of tuples of data
    """
    actions = None
    if api_name == 'alphavantage':
        parameters = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'full',
            'datatype': 'csv',
            'apikey': apikey.API_KEY
        }
        data = get_data_alphavantage(parameters, 'date')
    elif api_name == 'tdameritrade':
        parameters = {
            'period_type':client.Client.PriceHistory.PeriodType.YEAR,
            'period':  client.Client.PriceHistory.Period.TWENTY_YEARS,
            'frequency_type': client.Client.PriceHistory.FrequencyType.DAILY,
            'frequency': client.Client.PriceHistory.Frequency.DAILY,
            'apikey': tdam_keys.CLIENT_ID,
            'symbol': symbol.upper()
        }
        data = get_data_tdameritrade(parameters)
    elif api_name == 'yfinance':
        parameters = {
            'symbols': symbol,
            'period': 'max',
            'interval': '1d',
            'group_by': 'ticker',
            'auto_adjust': True,
            'prepost': True,
            'threads': True,
            'proxy': None,
            'actions': True,
        }
        data, actions = get_data_yfinance(parameters, bulk=bulk)
    return data, actions


def get_intraday(symbol, api_name):
    """
    Get data from API call for intraday data
    :param symbol: Symbol name
    :param interval: Time interval for data
    :param outputsize: Output size of API data
    :return:
    """
    if api_name == 'alphavantage':
        parameters = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': '1min',
            'outputsize': 'full',
            'datatype': 'csv',
            'apikey': apikey.API_KEY
        }
        data.append(get_data_alphavantage(parameters, 'datetime'))
    elif api_name == 'tdameritrade':
        parameters = {
            'period_type':client.Client.PriceHistory.PeriodType.DAY,
            'period':  client.Client.PriceHistory.Period.TEN_DAYS,
            'frequency_type': client.Client.PriceHistory.FrequencyType.MINUTE,
            'frequency': client.Client.PriceHistory.Frequency.EVERY_MINUTE,
            'apikey': tdam_keys.CLIENT_ID,
            'symbol': symbol
        }
        data = get_data_tdameritrade(parameters)
    elif api_name == 'yfinance':
        parameters = {
            'symbols': symbol,
            'period': '5d',
            'interval': '1m',
            'group_by': 'ticker',
            'auto_adjust': True,
            'prepost': True,
            'threads': True,
            'proxy': None,
            'actions': False,
        }
        data = get_data_yfinance(parameters)
    return data
