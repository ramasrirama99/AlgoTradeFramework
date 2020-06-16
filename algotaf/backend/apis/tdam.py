from tda import auth, client
from datetime import datetime, timedelta
import json
from algotaf.backend.fileio import tdam_keys


def authenticate_client(token_path, api_key, redirect_url):
    try:
        c = auth.client_from_token_file(token_path, api_key)
    except FileNotFoundError:
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        with webdriver.Chrome(ChromeDriverManager().install()) as driver:
            c = auth.client_from_login_flow(
                driver, api_key, redirect_url, token_path)
    return c


# print(get_daily_adjusted('AAPL'))
# c = authenticate_client(tdam_keys.TOKEN_PATH, tdam_keys.CLIENT_ID, tdam_keys.REDIRECT_URL)
# r = c.search_instruments(symbols=['AAPl'], projection=client.Client.Instrument.Projection.FUNDAMENTAL)
# assert r.ok, r.raise_for_status()
# data = r.json()
# print(data)

# print(json.dumps(r.json(), indent=4))

'''
candles: data
symbol: AAPL
empty: False
'''



# r = c.get_option_chain('AAPL',
#         contract_type=client.Client.Options.ContractType('CALL'),
#         strike_range=client.Client.Options.StrikeRange('OTM'),
#         strike_count=50,
#         strike_from_date=datetime.today() + timedelta(days=7),
#         strike_to_date=datetime.today() + timedelta(days=30),
#         option_type=client.Client.Options.Type('ALL'))
# assert r.ok, r.raise_for_status()
# chain = r.json()
# calls = chain['callExpDateMap']
# price = chain['underlyingPrice']
# candidates = {}
# for date, dateval in calls.items():
# 	for strike, strikeval in dateval.items():
# 		if strikeval[0]['totalVolume'] > 50 and not strikeval[0]['inTheMoney'] and strikeval[0]['strikePrice'] >= price * 1.05 and strikeval[0]['strikePrice'] <= price * 1.15:
# 			candidates['{}-{}'.format(date, strike)] = strikeval[0]

# print(json.dumps(candidates, indent=4))
# for key, val in candidates.items():
# 	days = val['daysToExpiration']
# 	bid = val['bid']
# 	ask = val['ask']
# 	last = val['last']
# 	strike = val['strikePrice']
# 	bestcase = (strike + last - price) / price
# 	worstcase = (last) / price
# 	compound1 = 1 + bestcase
# 	compound2 = 1 + worstcase
# 	yearend = (compound1 ** (365/days/8)) + (compound2 ** (365/days/8*7))
# 	worstyearend = (compound2 ** (365/days))
# 	print(key)
# 	print(last)
# 	print(bestcase)
# 	print(worstcase)
# 	print(yearend)
# 	print(worstyearend)
# 	print()