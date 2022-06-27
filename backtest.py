# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 21:46:02 2022

@author: peter
"""
import plotte_litt as plitt
import yfinance as yf 
import pandas as pd
import numpy as np
import ta

if __name__ == "__main__":
    df = plitt.execute_scrape(start="01-01-2018", end="01-01-2022")
    df = plitt.plotte_prep(df)
    #plitt.plot_CMA(df=df, col="Close")
    df['ATR'] = ta.volatility.average_true_range(df.High, df.Low, df.Close)