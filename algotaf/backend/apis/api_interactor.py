import csv
import requests
import yfinance as yf
import pandas as pd
from alpaca_trade_api import REST
from datetime import datetime, timedelta
from io import StringIO
from tda import auth, client
from algotaf.backend.fileio import apikey, tdam_keys, alpaca_keys
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
        if timestamp_type == client.Client.PriceHistory.FrequencyType.DAILY:
            row.append(datetime.fromtimestamp(record['datetime']/1000.0).date())
        elif timestamp_type == client.Client.PriceHistory.FrequencyType.EVERY_MINUTE:
            row.append(datetime.fromtimestamp(record['datetime']/1000.0))
        row.append(record['open'])
        row.append(record['high'])
        row.append(record['low'])
        row.append(record['close'])
        row.append(record['volume'])
        row.append(0)
        row.append(0)
        tuple_data_list.append(tuple(row))
    return tuple_data_list


def create_tuple_alpaca(data, timestamp_type, dividends=None, splits=None):
    columns = data.columns
    tuple_data_list = []
    for i, record in data.iterrows():
        row = []
        if timestamp_type == 'date':
            timestamp = i.to_pydatetime().date()
            row.append(timestamp)
        elif timestamp_type == 'datetime':
            timestamp = i.to_pydatetime()
            row.append(timestamp)
        for col in columns:
            if col in record:
                row.append(record[col])
        if timestamp_type == 'date':
            if dividends and timestamp in dividends:
                row.append(dividends[timestamp])
            else:
                row.append(0)
            if splits and timestamp in splits:
                row.append(splits[timestamp])
            else:
                row.append(1)
        tuple_data_list.append(tuple(row))
    return tuple_data_list


def create_dict_actions(dividends, splits):
    dividend_dict = {}
    split_dict = {}

    if dividends is not None:
        for data in dividends:
            payday = datetime.strptime(data._raw['paymentDate'], '%m/%d/%Y').date()
            dividend_amount = data._raw['amount']
            dividend_dict[payday] = dividend_amount

    if splits is not None:
        for data in splits:
            payday = datetime.strptime(data._raw['paymentDate'], '%Y-%m-%d').date()
            split_coefficient = 1 / data._raw['ratio']
            split_dict[payday] = split_coefficient

    return dividend_dict, split_dict


def get_data_yfinance(parameters):
    data = yf.download(tickers=parameters['symbols'],
        period=parameters['period'],
        interval=parameters['interval'],
        group_by=parameters['group_by'],
        auto_adjust=parameters['auto_adjust'],
        prepost=parameters['prepost'],
        threads=parameters['threads'],
        proxy=parameters['proxy'],
        actions=parameters['actions'])
    return create_tuple_pandas(data, 'date')


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
        frequency=parameters['frequency'],
        need_extended_hours_data=parameters['need_extended_hours_data'])
    assert r.ok, r.raise_for_status()
    data = r.json()
    return create_tuple_json(data['candles'], parameters['frequency_type'])


def get_data_alpaca(parameters):
    dividends = None
    splits = None
    api = REST(alpaca_keys.APCA_API_KEY_ID, alpaca_keys.APCA_API_SECRET_KEY)
    data = api.get_aggs(parameters['symbol'],
           multiplier=parameters['multiplier'],
           timespan=parameters['timespan'],
           _from=parameters['_from'],
           to=parameters['to']).df
    if parameters['timestamp_type'] == 'date':
        dividends, splits = get_actions_alpaca(parameters['symbol'])
    return create_tuple_alpaca(data, parameters['timestamp_type'], dividends=dividends, splits=splits)


def get_actions_alpaca(symbol):
    api = REST(alpaca_keys.APCA_API_KEY_ID, alpaca_keys.APCA_API_SECRET_KEY)
    dividend_data = api.polygon.dividends(symbol)
    split_data = api.polygon.splits(symbol)
    return create_dict_actions(dividend_data, split_data)


def get_daily(symbol, api_name):
    """
    Get data from API call for daily data
    :param symbol: Symbol name
    :param outputsize: Output size of API data
    :return: List of tuples of data
    """
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
            'symbol': symbol.upper(),
            'need_extended_hours_data': False
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
        data = get_data_yfinance(parameters)
    elif api_name == 'alpaca':
        parameters = {
            'symbol': symbol.upper(),
            'multiplier': 1,
            'timespan': 'day',
            '_from': '1900-01-01',
            'to': '2100-01-01',
            'timestamp_type': 'date'
        }
        data = get_data_alpaca(parameters)
    return data


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
            'symbol': symbol,
            'need_extended_hours_data': True
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
    elif api_name == 'alpaca':
        parameters = {
            'symbol': symbol.upper(),
            'multiplier': 1,
            'timespan': 'minute',
            '_from': '2000-01-01',
            'to': '2100-01-01',
            'timestamp_type': 'datetime'
        }
        data = get_data_alpaca(parameters)
    return data
