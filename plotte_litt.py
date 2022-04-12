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

url = yhf.get_stock('AAPL')
#soup = yhf.gimme_soup(url)
soup_w = yhf.gimme_soup_w_start_end(url, start='01-06-2021', end='01-01-2022')  
rows = yhf.soup_to_scrape(soup_w)
scraped = yhf.scrape_it(rows)
aapl_df = yhf.dicts_to_df(scraped)


### plotting
cols = list(aapl_df.columns)
cols = cols[1:7]

# converts to num
for i in cols:
    aapl_df[i] = pd.to_numeric(aapl_df[i])
    
# plot closing price
# reversing

aapl_df = aapl_df[::-1]


aapl_df.plot(x='Date', y='Close', figsize=(10,6))
plt.xticks(rotation = 45, ha = 'right')

#plot SMA
def plot_SMA(df=aapl_df, time_period=10):
    SMA = str('SMA' + '_' + str(time_period))
    df[SMA] = df.Close.rolling(int(time_period)).mean()
    df.plot(x = 'Date', y = ['Close', SMA], figsize = (8,8))
    plt.xticks(rotation = 45, ha = 'right')

plot_SMA()



