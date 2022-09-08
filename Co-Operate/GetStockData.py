import pandas as pd
import numpy as np
import StockDataBase as SP500_normal_db #import the Stock List
import Reuters_StockDataBase as db #import the Stock List
import requests
import yfinance as yf
import time

import json
import re

#Url
Url_eps_annual = "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t={}&type=eps-earnings-per-share-diluted&statement=income-statement&freq=A"
Url_eps_quarter = "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t={}&type=eps-earnings-per-share-diluted&statement=income-statement&freq=Q"
#Headers
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

#Global Values
period_to_get = 4

#Get the Revenue and GrossProfit by yfinance Library - return 1. qGpChanged 2. qGpScore 3.qGpTotalScore 4.aGpChanged 5. aGpScore 6. aGpTotalScore 7. qRChanged 8. qRScore 9. qRTotalScore 10. aRChanged 11. aRScore 12. aRTotalScore (All Size = 3)
def getRevenueAndGrossProfit(symbol):
    stockTicker = yf.Ticker(symbol)
    qGpChanged, qGpScore, qGpTotalScore = getQuarterlyGrossProfit(stockTicker)
    aGpChanged, aGpScore, aGpTotalScore = getAnnuallyGrossProfit(stockTicker)
    qRChanged, qRScore, qRTotalScore = getQuarterlyRevenue(stockTicker)
    aRChanged, aRScore, aRTotalScore = getAnnuallyRevenue(stockTicker)
    return qGpChanged, qGpScore, qGpTotalScore, aGpChanged, aGpScore, aGpTotalScore, qRChanged, qRScore, qRTotalScore, aRChanged, aRScore, aRTotalScore

# Get the Quarterly Gross Profit by yfinance financials location - return 1. countingMachine(grossProfit)
def getQuarterlyGrossProfit(stockTicker):
    grossProfit = []
    for i in range(0, 4):
        grossProfit.append(stockTicker.quarterly_financials.loc['Gross Profit', : ][i])
    return countingMachine(grossProfit)
# Get the Annually Gross Profit by yfinance financials location - return 1. countingMachine(grossProfit)
def getAnnuallyGrossProfit(stockTicker):
    grossProfit = []
    for i in range(0, 4):
        grossProfit.append(stockTicker.financials.loc['Gross Profit', : ][i])
    return countingMachine(grossProfit)
# Get the Quarterly Revenue by yfinance financials location - return 1. countingMachine(revenue)
def getQuarterlyRevenue(stockTicker):
    revenue = []
    for i in range(0, 4):
        revenue.append(stockTicker.quarterly_financials.loc['Total Revenue', : ][i])
    return countingMachine(revenue)
# Get the Annually Revenue by yfinance financials location - return 1. countingMachine(revenue)
def getAnnuallyRevenue(stockTicker):
    revenue = []
    for i in range(0, 4):
        revenue.append(stockTicker.financials.loc['Total Revenue', : ][i])
    return countingMachine(revenue)

# Get the Quarterly Eps by request
def getQuarterlyEps(symbol):
    r_quarter = requests.get(Url_eps_quarter.format(symbol), headers=headers)
    time.sleep(1)
    # v2 for quarter
    try:
        data_quarter = json.loads(re.search('chartData = (\[.+?\])', r_quarter.text).group(1))
    except:
        print('Error when getting QuarterlyEps of ' + symbol)
        return
    parsed_data = {x['date']:x['v2'] for x in data_quarter}
    # get values of periods period_to_get
    eps = list(parsed_data.values())[-1*period_to_get:]
    eps.reverse()
    return countingMachine(eps)

# Get the Annually Eps by request
def getAnnuallyEps(symbol):
    r_annual = requests.get(Url_eps_annual.format(symbol), headers=headers)
    time.sleep(1)
    # v1 for annual
    try:
        data_annual = json.loads(re.search('chartData = (\[.+?\])', r_annual.text).group(1))
    except:
        print('Error when getting AnnuallyEps of ' + symbol)
        return
    parsed_data = {x['date']:x['v1'] for x in data_annual}
    # get values of periods period_to_get
    eps = list(parsed_data.values())[-1*period_to_get:]
    eps.reverse()
    return countingMachine(eps)

#The Main function to get and cal the stock data - return 1. normalArrays(Size = 14) 2. totalArrays(Size = 8)
def getStockDataMain(symbol):
    normalArrays = []
    totalArrays = []
    qGpChanged, qGpScore, qGpTotalScore, aGpChanged, aGpScore, aGpTotalScore, qRChanged, qRScore, qRTotalScore, aRChanged, aRScore, aRTotalScore = getRevenueAndGrossProfit(symbol)
    #EPS
    qEpsChanged, qEpsScore, qEpsTotalScore = getQuarterlyEps(symbol)
    aEpsChanged, aEpsScore, aEpsTotalScore = getAnnuallyEps(symbol)
    #input the data into an array
    for i in range(0, period_to_get - 1 - 1):
        array = [symbol, i + 1, qGpScore[i], qGpChanged[i], aGpScore[i], aGpChanged[i], qRScore[i], qRChanged[i], aRScore[i], aRChanged[i], qEpsScore[i], qEpsChanged[i], aEpsScore[i], aEpsChanged[i]]
        normalArrays.append(array)
    totalArray = [symbol, qGpTotalScore, aGpTotalScore, qRTotalScore, aRTotalScore, qEpsTotalScore, aEpsTotalScore]
    totalArray.append(calSum((totalArray)))
    totalArrays.append(totalArray)
    return normalArrays, totalArrays

#Pass the data - return 1. Percentage Changed(Size = 3) 2. Score(Size = 3) 3.totalScore(Size = 1)
#def countingMachine(data):
#    #return empty array if no data
#    if not data or (len(data) < period_to_get):
#        return [None]*period_to_get, [None]*period_to_get, None
#    else:
#        score = []
#        changedPercentage = []
#        #Calculate the change
#        for i in range(0, period_to_get - 1):
#            Changed = ((data[i] - data[i + 1]) / data[i + 1] - 0.0000001) * 100
#            if (data[i + 1] < 0 and data[i] > 0) or (data[i + 1] < 0 and data[i] < 0 and data[i] < data[i + 1]):
#                Changed *= -1
#            changedPercentage.append(round(Changed, 2))
#        #Calculate the Score
#        score = [2**((period_to_get-1)-1-index) if change >= 0 else 0 for index, change in enumerate(changedPercentage)]
#        # sum of score
#        totalScore = sum(score)
#        return changedPercentage, score, totalScore

## New version
def countingMachine(data, period_to_get = period_to_get, get_score = False):
    #return empty array if no data
    if not data or (len(data) < period_to_get):
        return [None]*period_to_get, [None]*period_to_get, None
    else:
        score = []
        changedPercentage = []
        #Calculate the change
        for i in range(0, period_to_get - 1):
            Changed = ((data[i] - data[i + 1]) / data[i + 1] - 0.0000001) * 100
            if (data[i + 1] < 0 and data[i] > 0) or (data[i + 1] < 0 and data[i] < 0 and data[i] < data[i + 1]):
                Changed *= -1
            changedPercentage.append(round(Changed, 2))

        # get score of percentage change
        if not get_score:
            return countingMachine(changedPercentage, period_to_get-1, get_score = True)

        #Calculate the Score
        score = [2**((period_to_get-1)-1-index) if change > 0 else 0 for index, change in enumerate(changedPercentage)]
        # sum of score
        totalScore = sum(score)
        return changedPercentage, score, totalScore

#Calculate the sum of the multiple ddata type array - return 1. Sum of the Array(Size = 1)
def calSum(array):
    sum = 0
    for i in array:
        if i is not None and type(i) == int:
            sum += i
    return sum
#Get the Stocks Symbol from the xlsx - return 1. List of the Symbol(Size = Symbols amount from the Xlsx)
def getStockDataFromXlsx(market):
    marketStocksXlsx = market + ".xlsx"
    stocksList = pd.read_excel(marketStocksXlsx)
    return stocksList['Symbol'].tolist()

def main():
    normalDataFrameCols = ["Stock", "Period", "Quarterly Gross Profit Score", "Quarterly Gross Profit Changed %", "Annual Gross Profit Score", "Annual Gross Profit Changed %", "Quarterly Revenue Score", "Quarterly Revenue Changed %", "Annual Revenue Score", "Annual Revenue Changed %", "Quarterly EPS Score", "Quarterly EPS Changed %", "Annual EPS Score", "Annual EPS Changed %"]
    totalDataFrameCols = ["Stock", "Total Quarterly Gross Profit Score", "Total Annual Gross Profit Score", "Total Quarterly Revenue Score", "Total Annual Revenue Score", "Total Quarterly EPS Score", "Total Annual EPS Score", "Total Score"]
    market = input("Enter the market(AMEX, NYSE, NASDAQ): ")
    stockList = getStockDataFromXlsx(market)
    normalArrays = []
    totalArrays = []
    for stock in (stockList):
        print("Working on stock: " + str(stock))
        try:
            mainArray = getStockDataMain(stock)
            normalArrays +=  mainArray[0]
            totalArrays += mainArray[1]
        except:
            print("Skipped: " + str(stock))
    normalDataOutput = pd.DataFrame(normalArrays, columns = normalDataFrameCols)
    totalScoreOutput = pd.DataFrame(totalArrays, columns = totalDataFrameCols)
    normalDataOutput.to_csv(str(market) + "_Score" + ".csv", index = False)
    totalScoreOutput.to_csv(str(market) + "_TotalScore" + ".csv" , index = False)
    return

main()
