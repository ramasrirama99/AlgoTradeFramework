from abc import ABC, abstractmethod

class Strategy(ABC):
	@abstractmethod
	def set_up(self):
		print('Must implement set_up method')

	@abstractmethod
	def get_orders(self):
		print('Must implement get_orders method')