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

#%% creating function for sellsignals

def backtest(df):
    selldates = []
    outcome = []
    
    for i in range(len(df)):
        if df.BuySignal.iloc[i]:
            k = 1
            SL = df.SL.iloc[i]
            TP = df.TP.iloc[i]
            in_position = True
            while in_position:
                looping_high = df.High.iloc[i + k]
                looping_low = df.Low.iloc[i + k]
                if looping_high >= TP:
                    selldates.append(df.iloc[i + k].Date)
                    outcome.append('TP')
                    in_position = False
                elif looping_low <= SL:
                    selldates.append(df.iloc[i + k].Date)
                    outcome.append('SL')
                    in_position = False
                k += 1
    return selldates, outcome


if __name__ == "__main__":
    #Backteste en enkel crossover strategi med
    #skraperen og SMA
    
#%% Lage dataframe

    df = plitt.execute_scrape(start="01-01-2015", end="01-01-2022")
    df = plitt.plotte_prep(df)
    
    #plitt.plot_CMA(df=df, col="Close")
    
    plitt.plot_SMA(df=df, col="Close", time_period=[50,200])
    
    df["SMA_50"] = plitt.calc_SMA(df, "Close", 50)
    df["SMA_200"] = plitt.calc_SMA(df, "Close", 200)
    df['ATR'] = ta.volatility.average_true_range(df.High, df.Low, df.Close)
    df["TP"] = df.Close + (df.ATR * 2)
    df["SL"] = df.Close - (df.ATR * 3)
    
    df.dropna(inplace=True)
    
    crossover = (df["SMA_50"] > df["SMA_200"]) & (df["SMA_50"] > df["SMA_200"]).diff()
    
    df["Cross"] = crossover
    
    df["BuySignal"] = np.where((df.Cross), 1, 0)
    
    df.iloc[0].Date
    
    selldates, outcome = backtest(df)



    