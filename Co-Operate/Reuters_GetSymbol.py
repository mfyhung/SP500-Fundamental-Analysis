# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 00:15:15 2020

@author: ttk96
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import time
import StockDataBase as db #import the Stock List

chromeDriverPATH = "chromedriver.exe"
driver = webdriver.Chrome(chromeDriverPATH)
url_base = 'https://www.reuters.com/search/news?blob={}'

dict_old = db.SP500
import copy
dict_new = copy.deepcopy(dict_old)

for industry, stocks in dict_old.items():
    
    new_list = []
    
    for stock in stocks:
        driver.get(url_base.format(stock.replace('-', '')))
        try:
            symbol = driver.find_element_by_xpath("//div[@class='search-stock-ticker']/a").get_attribute('href').rpartition('/')[-1]
            new_list.append(symbol)
        except:
            new_list.append(stock)
        time.sleep(3)
        
    dict_new[industry] = new_list
    print('Updates ' + industry)
    
with open('Reuters_StockDataBase.txt', 'w') as f:
    import json
    f.write(json.dumps(dict_new, indent=4, sort_keys=True))