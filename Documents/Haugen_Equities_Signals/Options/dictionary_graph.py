import json
import numpy
import requests
import time
import datetime as datetime
from tos_credentials import client_id as client_id
from black_scholes_calculator_2 import bs_call
from historical_volatility import volatility_historical
import pandas
import statistics
import matplotlib.pyplot as plt

date_1 = time.strptime('2019-12-01 12:50:00.00', '%Y-%m-%d %H:%M:%S.%f')
date_2 = time.strptime('2019-12-31 18:00:00.00', '%Y-%m-%d %H:%M:%S.%f')
start_date = str(int(time.mktime(date_1))) + ('000')

current_time = datetime.datetime.now()
dummy = time.strptime(str(current_time), '%Y-%m-%d %H:%M:%S.%f')
now = str(int(time.mktime(dummy))) + ('000')

count = 0

df = pandas.read_csv('tickers_td_vol.csv')

for i in range(1):
    symbol = 'CRX'
    print symbol
    count = 1
    API_URL_1 = r"https://api.tdameritrade.com/v1/marketdata/chains"
    data_1 = {
                'apikey': client_id,
                'symbol': symbol,
                'contractType': 'CALL',
                # ~ 'strikeCount':'5',
                # ~ 'includeQuotes':'FALSE',
                'strategy':'ANALYTICAL',
                'range':'NTM',
                'fromDate':'2020-01-08',
                'toDate': '2020-01-20',

                }

    response_1 = requests.get(API_URL_1, data_1)

    symbol_1 = response_1.json()
    if symbol_1['status'] == "SUCCESS":
		print symbol_1
		
    for j in symbol_1['callExpDateMap']:
		expiration = j
		for k in symbol_1['callExpDateMap'][j]:
			days = float(symbol_1['callExpDateMap'][j][k][0]['daysToExpiration'])
		price = float(symbol_1['underlyingPrice'])
		i_rate = float(symbol_1['interestRate'])
		
		volatility_td = float(symbol_1['callExpDateMap'][j][k][0]['volatility'])
		theoretical_val = symbol_1['callExpDateMap'][j][k][0]['theoreticalOptionValue']







