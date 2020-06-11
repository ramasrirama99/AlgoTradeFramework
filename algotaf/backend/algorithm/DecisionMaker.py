from datetime import datetime, timedelta
from algotaf.backend.simulator.config import TIME, DATA, INTERVAL, DAY_INTERVAL, MINUTE_WINDOW
from algotaf.backend.algorithm.Bounce import Bounce
import algotaf.backend.models.CNN as CNN
import algotaf.backend.models.LSTM as LSTM
import algotaf.backend.experiments.train as train
import algotaf.backend.experiments.dataproc as dataproc
from algotaf.other.benchmark import Benchmark

# decision maker picks an algorithm out of a list and the corresponding data processing parameters
# it also decides on which model(s) to use for the corresponding algorithms

class DecisionMaker:
    """
    Algorithm class for storing algorithm strategies
    """

    def __init__(self,
                 portfolio,
                 algorithm,
                 model,
                 interval=INTERVAL,
                 window=MINUTE_WINDOW,
                 num_days=50,
                 train_split=0.8,
                 test_split=0.2):
        """
        :param name: Name of Algorithm
        """

        self.portfolio = portfolio
        self.algorithm = algorithm
        self.model = model
        self.interval = interval
        self.window = window
        self.num_days = num_days
        self.dataset = {}
        self.train_set = {}
        self.test_set = {}
        self.train_split = train_split
        self.test_split = test_split

    def update_data(self):
        for ticker, val in self.portfolio.watch_list.items():
            self.dataset[ticker] = DATA.get_data_interval(ticker,
                                                          TIME.timestamp - timedelta(days=self.num_days),
                                                          TIME.timestamp,
                                                          'close',
                                                          INTERVAL)

        self.train_set, self.test_set = dataproc.process_data(self.dataset)

    def make_decision(self):
        if self.algorithm is 'bounce':
            train.train_model(LSTM.model())
            train.train_model(CNN.model())
            Bounce()

