import requests
import json


# Performance over last quarter (profit, total value, liabilities, assets, cash flow, net income)
# Operating vs non-operating revenue
# Performance comparison to previous 4 quarters
# Revenue increase vs decrease (growth)
# Expenses increase vs decrease
# Current stock valuation
# Cash on hand, and assets vs liabilities

# assets, bookvalue, currentassets, currentliabilities, liabilities
# costofrevenue, netcashflow, netcashflowsfinancing, netcaaashflowsinvesting, netcashflowsoperating, revenues
# comprehensiveincome, netincomeloss, operatingincomeloss, nonoperatingincomeloss
# documenttype, sector,
# marketcap, pe, pb, price, sharesoutstanding

# baseline large

# materials: LYB, NEM, SHW
# industrials: DAL, ROK, NOC
# financials: COF, MMC, SPGI
# energy: COP, KMI, CVX
# consumer discretionary: HAS, AMZN, CMG
# information technology: NOW, STX, AMD
# communication services: VZ, TTWO, CHTR
# real estate: DLR, EQIX, CCI
# health care: BIIB, BSX, GILD
# consumer staples: TSN, KO, DG
# utilities: EXC, PEG, WEC

# baseline mid

# materials: EMN, 
# industrials: UAL, ALK
# financials: UNM, AIZ
# energy: HFC, COG
# consumer discretionary: MGM, NCLH, HAS
# information technology: XRX, 
# communication services: VIAC
# real estate: VNO, SLG, AIV
# health care: XRAY, 
# consumer staples: NWL, TAP
# utilities: NRG, PNW

# baseline small

# materials: 
# industrials: VRTS, IAG
# financials: 
# energy: HP
# consumer discretionary: IVR, HSC, EROS
# information technology: ENPH, SMSI
# communication services: 
# real estate: 
# health care: XBIT, KOD, AXSM, KPTII
# consumer staples: TPH
# utilities: 


APIKEY = 'Ynlyb24xMjN0QGdtYWlsLmNvbQ=='
# response = requests.get('https://api.tenquant.io/data?ticker=AAPL&key={}'.format(APIKEY))
response = requests.get('https://api.tenquant.io/historical?ticker=MSFT&date=20190501&key={}'.format(APIKEY))
# response = requests.get('https://api.tenquant.io/earningsreport?ticker=AAPL&key={}'.format(APIKEY))

content = response.json()
print(content)
bookvalue = content['bookvalue']
assets = content['assets']
grossprofit = content['grossprofit']
liabilities = content['liabilities']
marketcap = content['marketcap']
revenues = content['revenues']
netincomeloss = content['netincomeloss']
netcashflow = content['netcashflow']
currentassets = content['currentassets']
currentliabilities = content['currentliabilities']