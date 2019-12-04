import psycopg2
from algotaf.backend.db import db_wrapper as db
from algotaf.backend import config


class HistoricalData:
    """
    Class for historical data pulled from database
    """

    def __init__(self):
        self.conn = psycopg2.connect(dbname='algotaf',
                                     user=config.USERNAME,
                                     password=config.PASSWORD,
                                     host=config.BACKUP_HOSTNAME)
        self.tickers = {}

    def populate_data(self, tickers):
        """
        Populates data structure in class with daily and intraday database records
        :param tickers: Ticker list
        """

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
        """
        Gets the data for a ticker at a timestamp for an attribute
        :param ticker: Ticker name
        :param timestamp: Datetime
        :param attribute: Attribute or column to query
        :return: Data or None
        """

        if ticker in self.tickers and \
                timestamp in self.tickers[ticker] and \
                attribute in self.tickers[ticker][timestamp]:
            return self.tickers[ticker][timestamp][attribute]
        return None

    def get_data_interval(self, ticker, timestamp1, timestamp2, attribute, interval):
        """
        Gets the data for a ticker at a timestamp for an attribute
        :param ticker: Ticker name
        :param timestamp: Datetime
        :param attribute: Attribute or column to query
        :return: Data or None
        """

        data = []
        timestamp = timestamp1
        if ticker in self.tickers:
            while timestamp <= timestamp2:
                if attribute in self.tickers[ticker][timestamp]:
                    data.append(self.tickers[ticker][timestamp][attribute])
                timestamp += interval
        if len(data) == 0:
            return None
        return self.tickers[ticker][timestamp][attribute]

    def get_diff(self, ticker, timestamp1, timestamp2, attribute1, attribute2):
        """
        Get the difference between the data of a ticker with two different timestamps and attributes
        :param ticker: Ticker name
        :param timestamp1: Starting datetime
        :param timestamp2: Ending datetime
        :param attribute1: Starting attribute or column to query
        :param attribute2: Ending attribute or column to query
        :return:
        """

        data1 = self.get_data(ticker, timestamp1, attribute1)
        data2 = self.get_data(ticker, timestamp2, attribute2)
        if data1 is not None and data2 is not None:
            return data2 - data1
        return 0
