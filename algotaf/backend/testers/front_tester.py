import os
import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime
from alpaca_trade_api import REST

os.environ['APCA_API_KEY_ID'] = 'AKYKO5J4G4C4S1SECH81'
os.environ['APCA_API_SECRET_KEY'] = 'jj4D0a9jWLO8t6vDiF7DM1jCzaFRO5bnbfEHevDH'
api = REST()
start = pd.Timestamp(2019, 1, 1, 12).isoformat()
end = pd.Timestamp(2020, 1, 1, 12).isoformat()
# print(api.get_aggs('AAPL',1,'minute','2020-01-01','2020-01-20')[0])
# print(api.get_aggs('GRPN',1,'day','2020-06-05','2020-06-13'))
    # data = api.get_aggs(parameters['symbol'],
    #        multiplier=parameters['multiplier'],
    #        timespan=parameter['timespan'],
    #        _from=parameters['_from'],
    #        to=parameters['to']).df
thing = api.get_aggs('ABT',1,'minute','2000-01-01','2100-01-01').df
print(thing.columns)
print(thing.index[0])
print(thing.index[len(thing) - 1])
# print(datetime.fromtimestamp(thing.df.columns))
# print(api.get_aggs('AMD',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('AMZN',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('FB',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('MSFT',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('WORK',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('DLPN',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('MVIS',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('AMS',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('USL',1,'minute','2015-01-15','2020-01-20')[0])
# print(api.get_aggs('GDX',1,'minute','2015-01-15','2020-01-20')[0])
# account = api.get_account()
# print(account)
# print(api.list_positions())