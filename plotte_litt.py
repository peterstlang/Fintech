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

# url = yhf.get_stock("AAPL")
# # soup = yhf.gimme_soup(url)
# soup_w = yhf.gimme_soup_w_start_end(url, start="01-06-2021", end="01-01-2022")
# rows = yhf.soup_to_scrape(soup_w)
# scraped = yhf.scrape_it(rows)
# aapl_df = yhf.dicts_to_df(scraped)


# ### plotting
# cols = list(aapl_df.columns)
# cols = cols[1:7]

# # converts to num
# for i in cols:
#     aapl_df[i] = pd.to_numeric(aapl_df[i])

# plot closing price
# reversing

# aapl_df = aapl_df[::-1]


# aapl_df.plot(x="Date", y="Close", figsize=(10, 6))
# plt.xticks(rotation=45, ha="right")


def execute_scrape(ticker="AAPL"):
    url = yhf.get_stock(ticker)
    soup_w = yhf.gimme_soup_w_start_end(url, start="01-06-2021", end="01-01-2022")
    rows = yhf.soup_to_scrape(soup_w)
    scraped = yhf.scrape_it(rows)
    df = yhf.dicts_to_df(scraped)
    return df


# plot SMA
def plot_SMA(df=None, time_period=10):
    df = df[::-1]
    SMA = str("SMA" + "_" + str(time_period))
    var = df["Close"].rolling(int(time_period)).mean()
    # df.plot(x="Date", y=["Close", SMA], figsize=(8, 8))
    # plt.xticks(rotation=45, ha="right")
    # plt.show()
    df[SMA] = var
    print(df)
    print(var)


# time_list = [5,10,25,50]
# for i in range(len(time_list)):
#     plot_SMA(time_period = time_list[i])

if __name__ == "__main__":
    df = execute_scrape()
    # print(df)
    plot_SMA(df=df, time_period=5)