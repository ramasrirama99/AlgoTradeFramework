from algotaf.backend.strategies.strategy import Strategy
from datetime import datetime, timedelta
from algotaf.backend.simulator.Portfolio import Portfolio, Interval
from algotaf.backend.simulator.Order import Order
from algotaf.backend.testers.back_tester import Backtester
from algotaf.backend.strategies.crossover_strategy import CrossoverStrategy
import numpy as np
import matplotlib.pyplot as plt

TICKERS_SHORT = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo',
                 'bp', 'unh', 'cvs', 'tpr']
TEST_STOCK = 'msft'


class BuyAndHoldStrategy(Strategy):
	def __init__(self, percentage_to_invest=0.2):
		if percentage_to_invest > 1:
			print("Cannot invest more than 100%")
			percentage_to_invest = 0.2
		self.percentage_to_invest = percentage_to_invest
		self.interval = Interval.DAY


	def set_up(self):
		self.curr_date = self.env.get_time().date()

	def get_orders(self):
		if self.env.portfolio.total_equity == 0:
			return []
		current_percent = 1-self.env.portfolio.funds/self.env.portfolio.total_equity
		if current_percent < self.percentage_to_invest:
			quote = self.env.get_quote(TEST_STOCK, daily=True)
			if not quote['open'] or not quote['close']:
				return []
			price = (quote['open'] + quote['close']) / 2
			available_funds = self.percentage_to_invest * self.env.portfolio.funds - current_percent * self.env.portfolio.funds
			if price == 0:
				print("Price is somehow 0")
				return []
			num_shares = available_funds//price
			print(num_shares, current_percent)
			return [Order(TEST_STOCK, self.env.get_time(), None, buy=True, limit=False, limit_price=0, shares=num_shares)]
		return []



def main():
	strat = BuyAndHoldStrategy(0.5)
	portfolio = Portfolio('BuyNHold')
	env = Backtester(strat, portfolio, start_time=datetime(2003, 6, 10, 0, 0, 0), end_time=datetime(2019, 8, 23, 20, 0, 0))
	env.run()
	a = plt.plot(portfolio.equity_times, portfolio.equity_history, label='{}%BuyNHold'.format(strat.percentage_to_invest * 100))

	strat = CrossoverStrategy(short_period=40, long_period=200)
	portfolio = Portfolio('CrossoverStrategy')
	env = Backtester(strat, portfolio, start_time=datetime(2003, 6, 10, 0, 0, 0), end_time=datetime(2019, 8, 23, 20, 0, 0))
	env.run()

	b = plt.plot(portfolio.equity_times, portfolio.equity_history, label='CrossoverStrategy')
	plt.xlabel('timestamps')
	plt.ylabel('Portfolio equity')
	plt.title('{}'.format(TEST_STOCK.upper()))
	plt.legend(loc="upper left")
	plt.show()
	plt.savefig('results.png')

if __name__ == "__main__":
	main()
