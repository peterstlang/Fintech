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
    #Backteste en enkel crossover strategi med
    #skraperen og SMA
    
#%% Lage dataframe

    df = plitt.execute_scrape(start="01-01-2018", end="01-01-2022")
    df = plitt.plotte_prep(df)
    
    plitt.plot_CMA(df=df, col="Close")
    
    plitt.plot_SMA(df=df, col="Close", time_period=[50,200])
    
    df["SMA_50"] = plitt.calc_SMA(df, "Close", 50)
    df["SMA_200"] = plitt.calc_SMA(df, "Close", 200)
    df['ATR'] = ta.volatility.average_true_range(df.High, df.Low, df.Close)
    df["TP"] = df.Close + (df.ATR * 2)
    df["SL"] = df.Close - (df.ATR * 3)
    
    df.dropna(inplace=True)
    
    crossover = df["SMA_50"] > df["SMA_200"]
    #crossover = crossover.diff()
    
    df["Cross"] = crossover
    


    