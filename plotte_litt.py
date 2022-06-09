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


# plot SMA
def plot_SMA(df=None, time_period=[10]):
    SMA_list = ["Close"]
    for i in range(len(time_period)):
        SMA = str("SMA" + "_" + str(time_period[i]))
        df[SMA] = df.Close.rolling(int(time_period[i])).mean()
        #df[SMA] = MY_OWN_SMA(df = df, Window = time_period[i])
        SMA_list.append(SMA)
    
    df.plot(x="Date", y=SMA_list, figsize=(8, 8))
    
    plt.xticks(rotation=45, ha="right")
    plt.show()

def MY_OWN_SMA(df = None, col = "Close", Window = 3):
    df = plotte_prep(df=df)
    MAlist = df[col].tolist()
    MAlist.reverse()
    print(MAlist)
    sma = [np.nan] * (Window - 1)
    i = 0
    while i < len(MAlist) - Window + 1:
        avg = sum(MAlist[i:i+Window])/Window
        sma.append(avg)
        i += 1
    return sma

if __name__ == "__main__":
    df = execute_scrape()

    preppa_df = plotte_prep(df=df)

    # print(df)
    plot_SMA(df=preppa_df, time_period=[5,10,25])
    
    #fixedquestionmark = EMA(df=preppa_df)
    #mySMA_5 = SMA(df=preppa_df, Window = 5)
    #pandasSMA_5 = preppa_df["SMA_5"].to_list()
    #for i, j in zip(mySMA_5, pandasSMA_5):
    #    print(i, j)
    
    