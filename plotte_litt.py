# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 21:45:37 2022

@author: peter
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import yhf_scraper as yhf

def plotte_prep(df=None):
    cols = list(df.columns)
    cols = cols[1:7]

    df = df[::-1]

    for i in cols:
        df[i] = pd.to_numeric(df[i])
    return df


def execute_scrape(ticker="AAPL"):
    url = yhf.get_stock(ticker)
    soup_w = yhf.gimme_soup_w_start_end(url, start="01-06-2021", end="01-01-2022")
    rows = yhf.soup_to_scrape(soup_w)
    scraped = yhf.scrape_it(rows)
    df = yhf.dicts_to_df(scraped)
    return df

#calculate simple moving average
def calc_SMA(df = None, col = None, Window = None):
    df = plotte_prep(df=df)
    ColList = df[col].tolist()
    ColList.reverse()
    sma = [np.nan] * (Window - 1)
    i = 0
    while i < len(ColList) - Window + 1:
        avg = sum(ColList[i:i+Window])/Window
        sma.append(avg)
        i += 1
    return sma

# calculate cumulative moving average
def calc_CMA(df = None, col = None, Window = None):
    df = plotte_prep(df=df)
    ColList = df[col].tolist()
    ColList.reverse()
    cumsum = []
    
    i = 1
    start = 0
    while i < len(ColList) + 1:
        avg = sum(ColList[start:i])/i
        cumsum.append(avg)
        i += 1
    return cumsum

# calculate exponential moving average
def calc_EMA(df = None, col = None, days = 10, smoothening = 2):
    df = plotte_prep(df=df)
    ColList = df[col].tolist()
    ColList.reverse()
    SMA = sum(ColList[:days])/days
    EMA_lst = [np.nan]*(days - 1) + [SMA]
    
    for i in range(len(ColList[:days]), len(ColList)):
        EMA = (ColList[i] * (smoothening/(1 + days))) + \
        (EMA_lst[i-1] * (1 - (smoothening/(1 + days)))) 
        EMA_lst.append(EMA)
    
    return EMA_lst
        
# plot for moving average
def plot_MA(df=None, func=None, col=None, time_period=None):
    MA_list = [col]
    for i in range(len(time_period)):
        SMA = str("SMA" + "_" + str(time_period[i]))
        #df[SMA] = df.Close.rolling(int(time_period[i])).mean()
        df[SMA] = func(df = df, col=col, Window = time_period[i])
        MA_list.append(SMA)
    
    df.plot(x="Date", y=MA_list, figsize=(8, 8))
    
    plt.xticks(rotation=45, ha="right")
    plt.show()

# plot for cumulative moving average
def plot_CMA(df=None, col=None):
    df["CMA"] = calc_CMA(df=df, col=col)
    df.plot(x="Date", y=["Close", "CMA"], figsize=(8, 8))
    
    plt.xticks(rotation=45, ha="right")
    plt.show()

if __name__ == "__main__":
    #df = execute_scrape()

    #preppa_df = plotte_prep(df=df)

    # print(df)
    plot_MA(df=preppa_df, col="Close", func=calc_SMA, time_period=[5,10,25])
    plot_CMA(df=preppa_df, col="Close")
    
    
    
    #fixedquestionmark = EMA(df=preppa_df)
    #mySMA_5 = SMA(df=preppa_df, Window = 5)
    #pandasSMA_5 = preppa_df["SMA_5"].to_list()
    #for i, j in zip(mySMA_5, pandasSMA_5):
    #    print(i, j)

    
    
    