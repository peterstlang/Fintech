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
        SMA_list.append(SMA)
    
    df.plot(x="Date", y=SMA_list, figsize=(8, 8))
    
    plt.xticks(rotation=45, ha="right")
    plt.show()


if __name__ == "__main__":
    df = execute_scrape()

    preppa_df = plotte_prep(df=df)

    # print(df)
    plot_SMA(df=preppa_df, time_period=[5,10,25])
