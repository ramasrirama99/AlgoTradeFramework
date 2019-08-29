import psycopg2
import backend.db.db_wrapper as db
from backend import config


class HistoricalData:

    def __init__(self):
        self.conn = psycopg2.connect(dbname='algotaf',
                                     user=config.USERNAME,
                                     password=config.PASSWORD,
                                     host=config.BACKUP_HOSTNAME)
        self.tickers = {}

    def populate_data(self, tickers):
        for ticker in tickers:
            self.tickers[ticker] = {}

            table_name = 'data_daily_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            columns = ('open',
                       'high',
                       'low',
                       'close',
                       'adjusted_close',
                       'volume',
                       'dividend_amount',
                       'split_coefficient')

            for row in raw_data:
                self.tickers[ticker][row[0]] = {}
                for i, col in enumerate(row[1:]):
                    self.tickers[ticker][row[0]][columns[i]] = col

            table_name = 'data_intraday_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            columns = ('open',
                       'high',
                       'low',
                       'close',
                       'volume')
            for row in raw_data:
                self.tickers[ticker][row[0]] = {}
                for i, col in enumerate(row[1:]):
                    self.tickers[ticker][row[0]][columns[i]] = col

    def get_data(self, ticker, timestamp, attribute):
        if ticker in self.tickers and \
                timestamp in self.tickers[ticker] and \
                attribute in self.tickers[ticker][timestamp]:
            return self.tickers[ticker][timestamp][attribute]
        return None

    def get_diff(self, ticker, timestamp1, timestamp2, attribute1, attribute2):
        data1 = self.get_data(ticker, timestamp1, attribute1)
        data2 = self.get_data(ticker, timestamp2, attribute2)
        if data1 is not None and data2 is not None:
            return data2 - data1
        return 0
