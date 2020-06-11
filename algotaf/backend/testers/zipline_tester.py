from datetime import datetime
from algotaf.backend.simulator.config import TIME, INTERVAL
from algotaf.backend.simulator.Portfolio import Portfolio, Interval
from algotaf.backend.simulator.Order import Order
from algotaf.other.benchmark import Benchmark

from zipline.api import order, record, symbol
from zipline import run_algorithm


def initialize(context):
    pass


def handle_data(context, data):
    order(symbol('AAPL'), 10)
    record(AAPL=data.current(symbol('AAPL'), 'price'))


def analyze():



def main():
    run_algorithm(start=datetime(), end=datetime(), initialize=initialize, capital_base=5000.00, handle_data=handle_data, analyze=analyze)





if __name__ == '__main__':
    main()
