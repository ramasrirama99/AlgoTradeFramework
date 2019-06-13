import sqlalchemy
import psycopg2
import pandas as pd
import config
from fileio import apikey
import alpha_vantage
from pprint import pprint
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.cryptocurrencies import CryptoCurrencies


def store_ticker_in_db(conn, ts, ti, cc, t_l, c_l):
    for ticker in t_l:
        try:
            data_daily = ts.get_daily_adjusted(symbol=ticker, outputsize='full')[0]
            data_daily.columns = ['open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend', 'split_coefficient']
            data_daily.to_sql('data_daily_' + ticker.lower(), conn, if_exists='replace')
        except Exception as error:
            print(str(error))
        try:
            data_intraday = ts.get_intraday(symbol=ticker, interval='5min', outputsize='full')[0]
            data_intraday.columns = ['open', 'high', 'low', 'close', 'volume']
            data_intraday.to_sql('data_intraday_' + ticker.lower(), conn, if_exists='replace')
        except Exception as error:
            print(str(error))
        try:
            data_ema = ti.get_ema(symbol=ticker, interval='5min', time_period=50)[0]
            data_ema.columns = ['ema']
            data_ema.to_sql('data_ema_' + ticker.lower(), conn, if_exists='replace')
        except Exception as error:
            print(str(error))
        try:
            data_macd = ti.get_macd(symbol=ticker, interval='5min')[0]
            data_macd.columns = ['macd_signal', 'macd', 'macd_hist']
            data_macd.to_sql('data_macd_' + ticker.lower(), conn, if_exists='replace')
        except Exception as error:
            print(str(error))
        try:
            data_stoch = ti.get_stoch(symbol=ticker, interval='5min', slowdmatype=1)[0]
            data_stoch.columns = ['slowd', 'slowk']
            data_stoch.to_sql('data_stoch_' + ticker.lower(), conn, if_exists='replace')
        except Exception as error:
            print(str(error))
        try:
            data_rsi = ti.get_rsi(symbol=ticker, interval='5min', time_period=50)[0]
            data_rsi.columns = ['rsi']
            data_rsi.to_sql('data_rsi_' + ticker.lower(), conn, if_exists='replace')
        except Exception as error:
            print(str(error))

    # for ticker in c_l:
    #     try:
    #         data_daily = cc.get_digital_currency_daily(symbol=ticker, market='USD')[0]
    #         data_daily.columns = ['open', 'open1', 'high', 'high1', 'low', 'low1', 'close', 'close1', 'volume', 'cap']
    #         data_daily.drop(['open1', 'high1', 'low1', 'close1'], axis=1)
    #         data_daily.to_sql('daily_' + ticker.lower(), conn, if_exists='replace')
    #     except Exception as error:
    #         print(str(error))

    #     try:
    #         data_intraday = cc.get_digital_currency_intraday(symbol=ticker, market='USD')[0]
    #         data_intraday.columns = ['open', 'high', 'low', 'close', 'volume']
    #         data_intraday.to_sql('intraday_' + ticker.lower(), conn, if_exists='replace')
    #     except Exception as error:
    #         print(str(error))
    #     try:
    #         data_ema = ti.get_ema(symbol=ticker, interval='5min', time_period=50)[0]
    #         data_ema.columns = ['ema']
    #         data_ema.to_sql('ema_' + ticker.lower(), conn, if_exists='replace')
    #     except Exception as error:
    #         print(str(error))
    #     try:
    #         data_macd = ti.get_macd(symbol=ticker, interval='5min')[0]
    #         data_macd.columns = ['macd_signal', 'macd', 'macd_hist']
    #         data_macd.to_sql('macd_' + ticker.lower(), conn, if_exists='replace')
    #     except Exception as error:
    #         print(str(error))
    #     try:
    #         data_stoch = ti.get_stoch(symbol=ticker, interval='5min', slowdmatype=1)[0]
    #         data_stoch.columns = ['slowd', 'slowk']
    #         data_stoch.to_sql('stoch_' + ticker.lower(), conn, if_exists='replace')
    #     except Exception as error:
    #         print(str(error))
    #     try:
    #         data_rsi = ti.get_rsi(symbol=ticker, interval='5min', time_period=50)[0]
    #         data_rsi.columns = ['rsi']
    #         data_rsi.to_sql('rsi_' + ticker.lower(), conn, if_exists='replace')
    #     except Exception as error:
    #         print(str(error))


def main():
    try:
        with open('fileio/sensitive_data.txt') as sensitive:
            user = sensitive.readline().strip()
            password = sensitive.readline().strip()
        with open('fileio/db_host.txt') as host:
            hostname = host.readline().strip()
    except Exception as error:
        print(str(error))

    try:
        # conn = psycopg2.connect(dbname='algotaf', user=user, password=password, host=hostname)
        conn = sqlalchemy.create_engine('postgresql+psycopg2://' + user + ':' + password + '@' + hostname + ':5432/algotaf')
    except Exception as error:
        print(str(error))

    ts = TimeSeries(key=apikey.API_KEY, output_format='pandas')
    ti = TechIndicators(key=apikey.API_KEY, output_format='pandas')
    cc = CryptoCurrencies(key=apikey.API_KEY, output_format='pandas')
    # ticker_list = config.TICKERS
    t_l = ['AAPL', 'AMZN', 'MSFT']
    c_l = ['BTC', 'LTC', 'ETH']

    store_ticker_in_db(conn, ts, ti, cc, t_l, c_l)


if __name__ == '__main__': main()
