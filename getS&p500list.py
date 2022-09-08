import requests
import pandas as pd
import yfinance as yf
import time
# 貼上連結

currentStocks = []
IndustriesClassification = ['Technology', 'Consumer Cyclical', 'Communication Services', 'Financial Services', 'Healthcare', 'Consumer Defensive', 'Energy', 'Industrials', 'Utilities', 'Basic Materials', 'Real Estate', 'Financial']
SP500TechnologyStocks = ['AAPL', 'MSFT', 'NVDA', 'ADBE', 'INTC', 'CRM', 'CSCO', 'AVGO', 'QCOM', 'ACN', 'TXN', 'ORCL', 'AMD', 'IBM', 'NOW', 'INTU', 'FIS', 'MU', 'AMAT',
'LRCX', 'ADSK', 'FISV', 'ADI', 'CTSH', 'KLAC', 'APH', 'TEL', 'SNPS', 'XLNX', 'CDNS', 'MCHP', 'HPQ', 'ANSS', 'MSI', 'GLW', 'SWKS', 'FLT', 'KEYS', 'FTV',
'MXIM', 'VRSN', 'PAYC', 'ZBRA', 'TER', 'CDW', 'FINT', 'QRVO', 'TYL', 'GRMN', 'BR', 'AKAM', 'CTXS', 'WDC', 'HPE', 'ANET', 'STX', 'NTAP',
'TDY', 'LDOS', 'IT', 'JKHY', 'NLOK', 'FFIV', 'IPGP']
SP500ConsumerCyclicalStocks = ['AMZN', 'HD', 'NKE', 'MCD', 'LOW', 'SBUX', 'BKNG', 'TJX', 'GM', 'ROST', 'CMG', 'F', 'EBAY', 'MAR', 'APTV', 'ORLY', 'YUM', 'BLL', 'HLT',
'VFC', 'AZO', 'DHI', 'BBY', 'ETSY', 'LEN', 'IP', 'LVS', 'AMCR', 'TSCO', 'EXPE', 'KMX', 'DRI', 'ULTA', 'DPZ', 'NVR', 'POOL', 'Gpc',
'TIF', 'RCL', 'PKG', 'MGM', 'FBHS', 'PHM', 'WHR', 'HAS', 'WRK', 'CCL', 'AAP', 'WYNN', 'LKQ', 'BWA', 'LB', 'ROL', 'TPR', 'MHK', 'NCLH', 'SEE', 'PVH', 'LEG', 'RL', 'HBI', 'GPS', 'UAA', 'UA']
SP500CommunicationServicesStocks = ['FB', 'GOOGL', 'GOOG', 'DIS', 'VZ', 'NFLX', 'CMCSA', 'T', 'CHTR', 'TMUS', 'ATVI', 'TWTR', 'EA', 'TTWO', 'VIAC', 'OMC', 'LYV', 'LUMN', 'FOXA', 'IPG', 'DISCK', 'DISH', 'NWSA', 'DISCA', 'FOX', 'NWS']
SP500FinancialServicesStocks = ['BRK-B', 'JPM', 'V', 'MA', 'PYPL', 'BAC', 'C', 'WFC', 'BLK', 'MS', 'GS', 'AXP', 'SPGI', 'SCHW', 'CB', 'CME', 'TFC', 'ICE', 'USB', 'PNC',
'MMC', 'PGR', 'AON', 'MCO', 'COF', 'MSCI', 'MET', 'TRV', 'TROW', 'ALL', 'AIG', 'BK', 'PRU', 'AFL', 'WLTW', 'DFS', 'STT', 'AJG', 'FRC', 'AMP', 'MKTX',
'FITB', 'NTRS', 'SIVB', 'SYF', 'HIG', 'MTB', 'KEY', 'RF', 'CFG', 'NDAQ', 'CINF', 'HBAN', 'PFG', 'RJF', 'L', 'CBOE', 'WU', 'RE', 'WRB', 'GL', 'LNC', 'AIZ', 'CMA', 'ZION', 'BEN', 'IVZ', 'PBCT', 'UNM', 'AIV']
SP500HealthcareStocks = ['JNJ', 'UNH', 'PFE', 'MRK', 'ABT', 'ABBV', 'TMO', 'MDT', 'DHR', 'BMY', 'LLY', 'AMGN', 'ISRG', 'CVS', 'ANTM', 'SYK', 'ZTS', 'CI', 'GILD', 'BDX', 'VRTX', 'EW', 'ILMN', 'HUM', 'REGN', 'BSX', 'HCA', 'BAX', 'IDXX', 'BIIB', 'ALGN', 'A', 'CNC', 'ALXN',
'DXCM', 'IQV', 'ZBH', 'RMD', 'WBA', 'MCK', 'MTD', 'CERN', 'VTRS', 'WST', 'LH', 'HOLX', 'TFX', 'COO', 'CTLT', 'INCY', 'DGX', 'PKI', 'CAH', 'VAR', 'WAT', 'STE', 'ABC', 'ABMD', 'BIO', 'XRAY', 'UHS', 'HSIC', 'DVA', 'PRGO']
SP500ConsumerDefensiveStocks = ['PG', 'KO', 'WMT', 'PEP', 'COST', 'PM', 'TGT', 'MDLZ', 'MO', 'CL', 'EL', 'DG', 'KMB', 'SYY', 'STZ', 'GIS', 'MNST', 'ADM', 'DLTR', 'CLX', 'KR', 'MKC', 'KHC', 'HSY', 'CHD', 'TSN', 'CAG', 'K', 'BF-B', 'HRL', 'SJM', 'LW', 'CPB', 'TAP', 'NWL']
SP500EnergyStocks = ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'PSX', 'KMI', 'MPC', 'WMB', 'VLO', 'PXD', 'OKE', 'HAL', 'OXY', 'HES', 'BKR', 'CXO', 'FANG', 'COG', 'DVN', 'APA', 'MRO', 'NOV', 'FTI', 'HFC']
SP500IndustrialsStocks = ['HON', 'UNP', 'UPS', 'BA', 'RTX', 'MMM', 'CAT', 'GE', 'LMT', 'DE', 'ADP', 'FDX', 'CSX', 'ITW', 'NSC', 'GPN', 'EMR', 'NOC', 'ETN', 'WM', 'ROP', 'LHX', 'PH', 'JCI', 'TT', 'CMI',
'VRSK', 'INFO', 'TDG', 'CARR', 'CTAS', 'PAYX', 'PCAR', 'SWK', 'ROK', 'FAST', 'LUV', 'AME', 'OTIS', 'DAL', 'CPRT', 'EFX', 'RSG', 'ODFL', 'KSU', 'GWW', 'DOV', 'XYL', 'IR', 'URI', 'EXPD', 'IEX', 'MAS', 'J', 'UAL', 'WAB', 'AVY', 'CHRW', 'JBHT',
'TXT', 'ALLE', 'HWM', 'PWR', 'SNA', 'PNR', 'AAL', 'AOS', 'RHI', 'HII', 'NLSN', 'ALK', 'FLS']
SP500UtilitiesStocks = ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'XEL', 'ES', 'WEC', 'PEG', 'AWK', 'EIX', 'ED', 'DTE', 'PPL', 'ETR', 'AEE', 'CMS', 'FE', 'AES', 'LNT', 'EVRG', 'ATO', 'CNP', 'PNW', 'NI', 'NRG']
SP500BasicMaterialsStocks = ['LIN', 'SHW', 'APD', 'ECL', 'DD', 'NEM', 'DOW', 'FCX', 'PPG', 'CTVA', 'LYB', 'VMC', 'NUE', 'MLM', 'CE', 'FMC', 'ALB', 'EMN', 'IFF', 'MOS', 'CF']
SP500RealEstateStocks = ['AMT', 'PLD', 'CCI', 'EQIX', 'DLR', 'PSA', 'SBAC', 'SPG', 'WELL', 'WY', 'AVB', 'CBRE', 'O', 'ARE', 'EQR', 'VTR', 'PEAK', 'ESS', 'DRE', 'EXR', 'MAA', 'BXP', 'UDR', 'HST', 'IRM', 'REG', 'KIM', 'FRT', 'VNO', 'AIRC', 'SLG']
#SP500 Data Download
SP500url = 'https://www.slickcharts.com/sp500'
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
sp500_request = requests.get(SP500url, headers = headers)
sp500_data = pd.read_html(sp500_request.text)[0]
# 欄位『Symbol』就是股票代碼
sp500_stock_name = sp500_data.Symbol
# 用 replace 將符號進行替換
sp500_list = sp500_stock_name.apply(lambda x: x.replace('.', '-'))

#Yahoo Ranking Data Download
Yahoourl = 'https://finance.yahoo.com/screener/predefined/most_actives?offset=0&count=100'
Yahoo_request =  requests.get(Yahoourl, headers = headers)
Yahoo_data = pd.read_html(Yahoo_request.text)[0]
Yahoo_list = Yahoo_data.Symbol

#1. 分別股票種類(已分類完)
def get_sp500_sector_Classification():
    for i in sp500_list:
        print(i)
        try:
            if((yf.Ticker(i).info)['sector']) not in IndustriesClassification:
                IndustriesClassification.append((yf.Ticker(i).info)['sector'])
        except KeyError:
            continue
    print(IndustriesClassification)
    return

#2. 由股票種類得出對應的股票
def get_info_by_sector():
    print("Please choose Stock List")
    print("1. S&P500")
    print("2. Yahoo List(Please change the url in the source code)")
    urlInput = input()
    if (urlInput == "1"):
        Stock_List = sp500_list
    elif (urlInput == "2"):
        Stock_List = Yahoo_list
    else:
        print("Error Input")
        return
    print("Please Input The Require Sector, You can select from below")
    print(time.asctime(time.localtime(time.time())))
    for i in range(len(IndustriesClassification)):
        print(str(i + 1) + ". " + IndustriesClassification[i])
    classificationInput = input()
    for i in Stock_List:
        try:
            if(((yf.Ticker(i).info)['sector']) == IndustriesClassification[int(classificationInput) - 1]):
                currentStocks.append(i)
                print(i)
        except KeyError:
            continue
        time.sleep(1)
    with open("output.txt", "w") as txt:
        for line in currentStocks:
            txt.write("\'" + line + "\', ")
    print(time.asctime(time.localtime(time.time())))
    return

#3. 拎單一隻Stock去checking
def get_single_stock_info():
    yfinanceInfo = ['info', 'dividends', 'splits', 'institutional_holders', 'sustainability', 'recommendations', 'calendar']
    print("Please input the Stock Symbol")
    stockInput = input()
    print("Please input the Info from Yfinance")
    for i in range(len(yfinanceInfo)):
        print(str(i + 1) + ". " + yfinanceInfo[i])
    infoInput = input()
    try:
        #print((yf.Ticker(stockInput).info))
        print(getattr(yf.Ticker(stockInput), yfinanceInfo[int(infoInput) - 1]))
    except KeyError:
        print("error")

def debug_mode(stock):
    stock = yf.Ticker(stock)
    print(stock)
    print(stock.quarterly_financials)
    print(stock.info)
    #AAPLstock.quarterly_financials.to_csv('AAPL.csv')
    #TSLAstok = yf.Ticker('TSLA')
    #TSLAstok.financials.to_csv('TSLA.csv')

def main():
    while(1):
        print(" ")
        print("Please input your Request")
        print("1. Get SP500 Industries Classification")
        print("2. Get Data By Industries")
        print("3. Get Single Data")
        print("4. Debug Mode")
        print("Exit. Quit the program")
        fInput = input()
        if(fInput == "1"):
            get_sp500_sector_Classification()
        elif(fInput == "2"):
            get_info_by_sector()
        elif(fInput == "3"):
            get_single_stock_info()
        elif(fInput == "4"):
            debug_mode()
        elif(fInput == "exit"):
            return
'''
with open("output.txt", "w") as txt:
    for line in SP500ConsumerStocks:
        txt.write("\'" + line + "\' ")
'''
val = input("debug stock: ")
debug_mode(val)
