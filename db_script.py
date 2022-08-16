# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 01:05:18 2022

@author: peter
"""

#%%

# A script for creating a database



def get_ticker_list():
    import pandas as pd
    payload=pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')
    df = payload[4]

    Tickers = df.Ticker.to_list()
    return Tickers
    

def main():
    # ripper min egen funksjon
    from datetime import date, timedelta
    from backtest import get_data
    from sqlalchemy import create_engine
    
    engine = create_engine('sqlite:///STONKS.db')
    today = date.today()
    daysago = today - timedelta(days = 729)
    
    ticker_list = get_ticker_list()
    
    for symbol in ticker_list:
        df = get_data(symbol, start=daysago, interval='1h')
        df.to_sql(symbol, engine, index=False)
    
    

if __name__ == "__main__":
    main()
