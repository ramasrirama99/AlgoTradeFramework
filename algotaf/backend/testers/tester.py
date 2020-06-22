from abc import ABC, abstractmethod

class StrategyEnvironment(ABC):
	def __init__(self, strategy, portfolio):
		self.strategy = strategy
		self.portfolio = portfolio
		self.strategy.set_up()

	@abstractmethod
	def run(self):
		"""
    	Runs the tester until end time
    	"""
		print('Must implement run method')

	@abstractmethod
	def tick(self):
		"""
		Tells the strategy new data is available and receives orders accordingly
		"""
		print('Must implement tick method')

	def get_portfolio(self):
		self.portfolio.update()
		return self.portfolio

	@abstractmethod
	def get_quote(self, ticker):
		print('Must implement get_quote method')
