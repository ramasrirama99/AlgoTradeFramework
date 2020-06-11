from datetime import datetime, timedelta
import numpy as np
from algotaf.backend.simulator.config import TIME, DATA, INTERVAL, DAY_INTERVAL
from algotaf.backend.simulator.Portfolio import Portfolio, Interval, HistoryType
from algotaf.backend.simulator.Order import Order
from algotaf.backend.algorithm import Algorithms
from algotaf.other.benchmark import Benchmark


class Bounce(Algorithms):
    """
    Algorithm class for storing algorithm strategies
    """

    def __init__(self, cnn, lstm, ):
        """
        :param name: Name of Algorithm
        """

        self.name = name
        self.portfolio = portfolio
        self.ma_short = {}
        self.ma_long = {}
        self.shortterm = shortterm
        self.longterm = longterm
        wl = self.portfolio.watch_list
        for ticker, val in wl.items():
            ma_short[ticker] = {}
            ma_long[ticker] = {}
            ma_short[ticker][TIME.timestamp] = mean(DATA.get_data_interval(ticker,
                                                                           TIME.timestamp,
                                                                           TIME.timestamp + timedelta(
                                                                               days=self.shortterm),
                                                                           'close',
                                                                           config.DAY_INTERVAL))
            ma_long[ticker][TIME.timestamp] = mean(DATA.get_data_interval(ticker,
                                                                          TIME.timestamp,
                                                                          TIME.timestamp + timedelta(
                                                                              days=self.longterm),
                                                                          'close',
                                                                          config.DAY_INTERVAL))

    def update(self):
        """
        """

        wl = self.portfolio.watch_list
        for ticker, val in wl.items():
            if ticker in ma_short and ticker in ma_long:
                ma_short[TIME.timestamp].append(mean(DATA.get_data_interval(ticker,
                                                                            TIME.timestamp,
                                                                            TIME.timestamp + timedelta(days=20),
                                                                            'close',
                                                                            config.DAY_INTERVAL)))
                ma_long[TIME.timestamp].append(mean(DATA.get_data_interval(ticker,
                                                                           TIME.timestamp,
                                                                           TIME.timestamp + timedelta(days=150),
                                                                           'close',
                                                                           config.DAY_INTERVAL)))
            else:
                ma_short[TIME.timestamp] = mean(DATA.get_data_interval(ticker,
                                                                       TIME.timestamp,
                                                                       TIME.timestamp + timedelta(days=20),
                                                                       'close',
                                                                       config.DAY_INTERVAL))
                ma_long[TIME.timestamp] = mean(DATA.get_data_interval(ticker,
                                                                      TIME.timestamp,
                                                                      TIME.timestamp + timedelta(days=150),
                                                                      'close',
                                                                      config.DAY_INTERVAL))

    def preprocess(self):
        tickers = {}
        wl = self.portfolio.watch_list
        for ticker, val in wl.items():
            tickers[ticker] = []
            data = DATA.get_data_interval(ticker,
                                   TIME.timestamp - timedelta(days=50),
                                   TIME.timestamp,
                                   'close',
                                   INTERVAL)
            train_split = len(data) * 0.9
            test_split = len(data) * 0.1
            train = data[train_split:]
            test = data[:test_split]
            for i, val in enumerate(data):
                window = data[:5]


    def train(self):
        classifier = get_baseline_convolutional_encoder(filters=128, embedding_dimension=64, input_shape=(input_length, 1))
        # Add output classification layer
        classifier.add(Dense(train.num_classes(), activation='softmax'))

        opt = Adam(clipnorm=1.)
        classifier.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])