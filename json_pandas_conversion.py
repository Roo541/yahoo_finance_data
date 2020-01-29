import numpy as np
import matplotlib as plt
import datetime as datetime
import pandas as pd
import math
import time
import statistics 
from datetime import timedelta
import copy
import QuantLib as ql
import json
import requests
from authentication import api_key as api_key
from pandas.io.json import json_normalize

symbol = 'INTC'

API_URL_1 = r"https://eodhistoricaldata.com/api/options/%s" % symbol

data_1 = {
          'api_token': api_key,
          'from': '2020-01-24',
          'to': '2020-01-31',
                
		}

session = requests.Session()
r = session.get(API_URL_1, params = data_1)
data = r.json()

print (data['data'][0]['options']['CALL'][0]['updatedAt'])
index = []
ask = []
bid = []
theoretical = []
strike = []
for i in range(len(data['data'])):
	for j in range(len(data['data'][i]['options']['CALL'])):
		index.append((data['data'][i]['expirationDate'], data['data'][i]['options']['CALL'][j]['strike']))
		ask.append(data['data'][i]['options']['CALL'][j]['ask'])
		bid.append(data['data'][i]['options']['CALL'][j]['bid'])
		theoretical.append(data['data'][i]['options']['CALL'][j]['theoretical'])
		strike.append(data['data'][i]['options']['CALL'][j]['strike'])

print (len(index), len(ask), len(bid), len(theoretical))	
df_final = pd.DataFrame(list(zip(ask, bid, theoretical,)), columns = ['Ask', 'Bid', 'Theoretical'], index=index)

print (df_final[-100:-50])












