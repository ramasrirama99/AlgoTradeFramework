import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from algotaf.backend.db.db_wrapper import get_data_interval, connect


def csv_daily_data(conn, ticker, start_date, end_date, path):
    
    data = get_data_interval(conn, 'data_daily_{}'.format(ticker), start_date, end_date)
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend', 'split'])
    df = df.drop(['adjusted_close'], axis=1).set_index('date')
    print(df)
    df.to_csv('{}/daily/{}.csv'.format(path, ticker), header=True, index=True)


def csv_intraday_data(conn, ticker, start_date, end_date, path):
    
    data = get_data_interval(conn, 'data_intraday_{}'.format(ticker), start_date, end_date)
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df = df.set_index('date')
    df['dividend'] = 0
    df['split'] = 1
    print(df)
    df.to_csv('{}/intraday/{}.csv'.format(path, ticker), header=True, index=True)


def bundler():
    def ingest(environ,
               asset_db_writer,
               minute_bar_writer,
               daily_bar_writer,
               adjustment_writer,
               calendar,
               start_session,
               end_session,
               cache,
               show_progress,
               output_dir):

        metadata_dtype = [
            ('symbol', 'object'),
            ('asset_name', 'object'),
            ('start_date', 'datetime64[ns]'),
            ('end_date', 'datetime64[ns]'),
            ('first_traded', 'datetime64[ns]'),
            ('auto_close_date', 'datetime64[ns]'),
            ('exchange', 'object')]


        ticker_list = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo',
                       'bp', 'unh', 'cvs', 'tpr']
        conn = connect()
        metadata = pd.DataFrame(np.empty(len(ticker_list), dtype=metadata_dtype))
        start_date = datetime(2020, 2, 14, 9, 31, 0)
        end_date = datetime(2020, 2, 28, 16, 0, 0)

        for i, ticker in enumerate(ticker_list):
            intraday = get_data_interval(conn, 'data_intraday_{}'.format(ticker), start_date, end_date)
            daily = get_data_interval(conn, 'data_daily_{}'.format(ticker), start_date.date(), end_date.date())

            metadata.iloc[i] = ticker, ticker, start_date, end_date, start_date, end_date + timedelta(days=1), 'NYSE'
            # print(metadata.iloc[i])

            df = pd.DataFrame(intraday, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            df = df.set_index('date')
            df1 = pd.DataFrame(daily, columns=['date', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend', 'split'])
            df1 = df1.drop(['adjusted_close'], axis=1).set_index('date')

            try:
                minute_bar_writer.write([(i, df)], show_progress=True)
            except Exception as e:
                print(e)
            try:
                daily_bar_writer.write([(i, df1)], show_progress=True)
            except Exception as e:
                print(e)

        asset_db_writer.write(equities=metadata)
        print(metadata)
        adjustment_writer.write()

    return ingest



def main():
    conn = connect()
    csv_daily_data(conn, 'aapl', datetime(1998, 1, 2), datetime(2020, 2, 20), '/mnt/c/Users/byron.LAPTOP-6A9A5QNU/Desktop/GitHub/algotrade/data')
    csv_intraday_data(conn, 'aapl', datetime(2020, 2, 14, 9, 31, 0), datetime(2020, 2, 28, 16, 0, 0), '/mnt/c/Users/byron.LAPTOP-6A9A5QNU/Desktop/GitHub/algotrade/data')


if __name__ == '__main__':
    main()
