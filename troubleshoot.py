import json
import numpy
import requests
import time
import datetime as datetime
from tos_credentials import client_id as client_id
import pandas
import statistics
import matplotlib.pyplot as plt
from black_scholes_calculator_2 import bs_call
from historical_volatility import volatility_historical

count = 0

df = pandas.read_csv('tickers_td_haugen_op_value_14.csv')
out = 0
inside = 0

for i in range(len(df['symbol'])):
    strike_list = []
    strike = 1.00
    days = 1.00
    i_rate = 1.00
    price = 1.00
    dummy = 0.0 
    ask_bid_diff = 0.0
    symbol = df['symbol'][i]
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
                'fromDate':'2020-01-13',
                'toDate': '2020-01-20',

                }

    response_1 = requests.get(API_URL_1, data_1)

    symbol_1 = response_1.json()
    if 'status' not in symbol_1.keys():
		df = df.drop([i])
		out+=1
		time.sleep(0.25)
    if 'status' in symbol_1.keys():
		if symbol_1['status'] == "SUCCESS":
			inside +=1
			price = float(symbol_1['underlyingPrice'])
			#print "Price is:", price

			#Find the closest strike price in the money
			for l in symbol_1['callExpDateMap']:
				for m in symbol_1['callExpDateMap'][l]:
					dummy = float(m)
					if dummy < price:
						strike_list.append(dummy)
					
			if len(strike_list) != 0.0:
				strike = numpy.max(strike_list)

			# ~ print "Strike is:", strike
			for j in symbol_1['callExpDateMap']:
				# ~ print symbol_1['callExpDateMap'].keys()
				expiration = j
				for k in symbol_1['callExpDateMap'][j]:
					days = float(symbol_1['callExpDateMap'][j][k][0]['daysToExpiration'])
					
				i_rate = float(symbol_1['interestRate'])
				
				volatility_td = float(symbol_1['callExpDateMap'][j][k][0]['volatility'])
				#theoretical_val = float(symbol_1['callExpDateMap'][j][k][0]['theoreticalOptionValue'])
			if strike >1:
				theoretical_val = float(symbol_1['callExpDateMap'][expiration][str(strike)][0]['ask'])
				ask_bid_diff = abs(float(symbol_1['callExpDateMap'][expiration][str(strike)][0]['bid'])/float(symbol_1['callExpDateMap'][expiration][str(strike)][0]['ask']))*100
			else:
				theoretical_val = 0.0
			
			volatility_td = volatility_td/100.0
			haugen_vol = float(df['haugen_vol'][i])
			
			if price != 0 and ask_bid_diff < 20 and ask_bid_diff != 0:
				df['haugen_val'][i] = float(bs_call(price, strike, days/365.0, i_rate, haugen_vol))	
				df['td_val'][i] = theoretical_val
				if df['td_val'][i] != 0:
					df['pct_diff'][i] = (df['haugen_val'][i]/df['td_val'][i])
					df['strike'][i] = float(strike)
					df['price'][i] = price
				# ~ print "haugen_val:", df['haugen_val'][i]
				# ~ print "td_val:", df['td_val'][i]
				# ~ print "pct_change:", df['pct_diff'][i]
			time.sleep(0.25)
	
    if 'status' in symbol_1.keys():
	    if symbol_1['status'] != "SUCCESS":
			df = df.drop([i])
			out +=1
			#print out
			
print "number of symbols dropped:", out
print "number of symbols in:", inside
print "total is:", (out + inside)

with open('trouble_shoot_15_ask_bid_2_3.csv', 'w') as file:
	df.to_csv(file, index = False)















