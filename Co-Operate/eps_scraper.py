# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 18:10:49 2021

@author: ttk96
"""

import pandas as pd
import numpy as np
import time
#import Reuters_StockDataBase as db #import the Stock List
import requests
import re
import json

def get_eps(stock):
    r_annual = requests.get(url_eps_annual.format(stock), headers=headers)
    time.sleep(3)
    r_quarter = requests.get(url_eps_quarter.format(stock), headers=headers)
    time.sleep(3)
    
    # get data
    # v1 for annual
    data_annual = json.loads(re.search('chartData = (\[.+?\])', r_annual.text).group(1))
    # v2 for quarter
    data_quarter = json.loads(re.search('chartData = (\[.+?\])', r_quarter.text).group(1))
    
    return (data_annual, data_quarter)
    

url_eps_annual = "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t={}&type=eps-earnings-per-share-diluted&statement=income-statement&freq=A"
url_eps_quarter = "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t={}&type=eps-earnings-per-share-diluted&statement=income-statement&freq=Q"

headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

stocks = ['goog']

parsed_data_annual = {}
parsed_data_quarter = {}

for stock in stocks:
    
    # get eps
    data_annual, data_quarter = get_eps(stock)
    
    # add to result
    parsed_data_annual[stock] = {x['date']:x['v1'] for x in data_annual}  
    parsed_data_quarter[stock] = {x['date']:x['v2'] for x in data_quarter}
    
df_annual = pd.DataFrame.from_dict(parsed_data_annual, orient = 'index')
df_quarter = pd.DataFrame.from_dict(parsed_data_annual, orient = 'index')

with pd.ExcelWriter('EPS.xlsx', mode='w') as writer:
    df_annual.to_excel(writer, sheet_name='annual')
    df_quarter.to_excel(writer, sheet_name='quarter')
    
if __name__ == "__main__":
    stock = input('Enter stock code: ')
    