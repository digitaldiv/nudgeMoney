from models.portfolio import FinanceData, HistoricalData
import pandas as pd
from app import db
import numpy as np
import requests as req
import datetime

def db_seed_test (dFile):
    fd1=FinanceData (
        Symbol='ABC',
        Name='XYZ',
        Sector='TTTTTTT',
        Price=1,
        PricePerEarnings=0,
        Dividend_Yield=0,
        EarningsPerShare=0,
        P52_Week_Low=0,
        P52_Week_High=0,
        Market_Cap=0,
        EBITDA=0,
        PricePerSales=0,
        PricePerBook=0,
        SEC_Filings=0
    )
    db.session.add(fd1)
    db.session.commit()

def db_seed (dataFile):
    #dataFile = r'/Users/divpithadia/Downloads/s-and-p-500-companies-financials_zip-2/data/constituents-financials_csv.csv'
   
    df = pd.read_csv(dataFile)
    print( f'Read the file with rows : {df.shape[0]}')
    #print(df)
    #df = df0.where(pd.notnull(df0), None)
    for i in range(0, df.shape[0]):
        ppb= df.iloc[i, 12]
        ppb = 0 if (ppb is None or np.isnan(ppb)) else ppb

        ppe = df.iloc[i, 4]
        ppe = 0 if (ppe is None or np.isnan(ppe)) else ppe

        fd1= FinanceData (
                Symbol=df.iloc[i, 0],
                Name=df.iloc[i, 1],
                Sector=df.iloc[i, 2],
                Price=df.iloc[i, 3],
                PricePerEarnings=ppe,
                Dividend_Yield=df.iloc[i, 5],
                EarningsPerShare=df.iloc[i, 6],
                P52_Week_Low=df.iloc[i, 7],
                P52_Week_High=df.iloc[i, 8],
                Market_Cap=int(df.iloc[i, 9]),
                EBITDA=int(df.iloc[i, 10]),
                PricePerSales=df.iloc[i, 11],
                PricePerBook=ppb,
                SEC_Filings=df.iloc[i, 13]
                )
        db.session.add(fd1)
        db.session.commit() 

def get_historical_data  ():
    all_tickers = FinanceData.query.all()
    #tickers = [ 'COF'] # ,'DIS','SQ','INTC','MSFT','CRM','CMG','NKE','AMD','UA' ]
    for ticker in all_tickers:
        print( f'Getting Data file for {ticker.Symbol}')
        get_history(ticker.Symbol)

    
def get_history(ticker):
    link = (f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=252374400&period2=1618444800&interval=1d&events=history&crumb=BkT/GAawAXc")
    myfile = req.get(link)

    """     counter = 0
    for lines in myfile.content:
        counter+=1
        if counter > 1:
            finance_data = line.split(',')
            trade_date = finance_data[0]
            y,m,d = trade_date.split('-')
            new_trade_date = datetime.date(int(y),int(m),int(d))
            close_price = float(finance_data[4])
            volume = int(finance_data[6].strip('\n')) """

    open(f'/Volumes/Div2021/snpdata/{ticker}.csv', 'wb').write(myfile.content)
        # https://query1.finance.yahoo.com/v7/finance/download/DIS?period1=-252374400&period2=1618444800&interval=1d&events=history&includeAdjustedClose=true


def get_history2(ticker):
    link = (f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=252374400&period2=1618444800&interval=1d&events=history&crumb=BkT/GAawAXc")
    myfile = req.get(link)

    #print(myfile.content)
    lines = myfile.content.decode().split('\n')
    

    #all_lines = lines.split('\n')

    counter = 0
    for line in lines: #myfile.content:
        print(line)
        counter+=1
        if counter > 1:
            finance_data = line.split(',')
            trade_date = finance_data[0]
            y,m,d = trade_date.split('-')
            new_trade_date = datetime.date(int(y),int(m),int(d))
            close_price = float(finance_data[4])
            volume = int(finance_data[6].strip('\n')) 

            hd = HistoricalData (
                Symbol = ticker,
                TradeDate = trade_date,
                OpenPrice = finance_data[1],
                HiPrice = finance_data[2],
                LoPrice = finance_data[3],
                ClosePrice = close_price,
                AdjClosePrice = finance_data[5],
                Volume  = volume
            )
            db.session.add(hd)
            db.session.commit()
    #open(f'/Volumes/Div2021/snpdata/{ticker}.csv', 'wb').write(myfile.content)
    # https://query1.finance.yahoo.com/v7/finance/download/DIS?period1=-252374400&period2=1618444800&interval=1d&events=history&includeAdjustedClose=true

