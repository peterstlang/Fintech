# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 21:46:02 2022

@author: peter
"""

#%% imports

import plotte_litt as plitt
import yfinance as yf 
import pandas as pd
import numpy as np
import ta

#%% creating function for sellsignals

def crossover_strategy(df, fast=50, slow=200):
    #creating strings for column frames
    df_copy = df.copy()
    
    SMA_fast = "SMA_" + str(fast)
    SMA_slow = "SMA_" + str(slow)
    
    # creating columns and dropping nans

    df_copy[SMA_fast] = ta.trend.sma_indicator(close = df_copy.Close, window=fast)
    df_copy[SMA_slow] = ta.trend.sma_indicator(close = df_copy.Close, window=slow)
    df_copy['ATR'] = ta.volatility.average_true_range(df_copy.High, df_copy.Low, df_copy.Close)
    df_copy["TP"] = df_copy.Close + (df_copy.ATR * 2)
    df_copy["SL"] = df_copy.Close - (df_copy.ATR * 3)
    df_copy.dropna(inplace=True)
    
    df_copy["BuySignal"] = ((df_copy["SMA_50"] > df_copy["SMA_200"]) & (df_copy["SMA_50"] > df_copy["SMA_200"]).diff()).astype(int)
    
    return df_copy
    

#%% backtest strategy
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
                if i + k == len(df):
                    break
                looping_high = df.High.iloc[i + k]
                looping_low = df.Low.iloc[i + k]
                if looping_high >= TP:
                    selldates.append(df.iloc[i + k].name)
                    outcome.append('TP')
                    in_position = False
                elif looping_low <= SL:
                    selldates.append(df.iloc[i + k].name)
                    outcome.append('SL')
                    in_position = False
                k += 1

    return selldates, outcome

#%%
def sellsignal_df(df, selldates, outcome):
    df_copy = df.copy()
    
    df_copy.loc[selldates, "SellSignal"] = 1
    df_copy.loc[selldates, "Outcome"] = outcome
    
    df_copy.SellSignal = df_copy.SellSignal.fillna(0).astype(int)
    
    mask = df_copy[(df_copy.BuySignal == 1) | (df_copy.SellSignal == 1)]
    mask_2 = mask[(mask.BuySignal.diff() == 1) | (mask.SellSignal.diff() == 1)]
    
    return mask_2
    
#%% teste med cola
    #Backteste en enkel crossover strategi med
    #skraperen og SMA
    


# =============================================================================
#     df = plitt.execute_scrape(ticker="KO", start="01-01-2015", end="01-01-2022")
#     df = plitt.plotte_prep(df)
#     
#     #plitt.plot_CMA(df=df, col="Close")
#     
#     #plitt.plot_SMA(df=df, col="Close", time_period=[50,200])
#     
#     df["SMA_50"] = plitt.calc_SMA(df, "Close", 50)
#     df["SMA_200"] = plitt.calc_SMA(df, "Close", 200)
#     df['ATR'] = ta.volatility.average_true_range(df.High, df.Low, df.Close)
#     df["TP"] = df.Close + (df.ATR * 2)
#     df["SL"] = df.Close - (df.ATR * 3)
#     
#     df.dropna(inplace=True)
#     
#     crossover = (df["SMA_50"] > df["SMA_200"]) & (df["SMA_50"] > df["SMA_200"]).diff()
#     
#     
#     df["BuySignal"] = crossover.astype(int)
#      
#     df.iloc[0].name
#     
#     selldates, outcome = backtest(df)
#     
#     df.loc[selldates, "SellSignal"] = 1
#     df.loc[selldates, "Outcome"] = outcome
#     
#     df.SellSignal = df.SellSignal.fillna(0).astype(int)
#     
#     mask = df[(df.BuySignal == 1) | (df.SellSignal == 1)]
#     mask2 = mask[(mask.BuySignal.diff() == 1) | (mask.SellSignal.diff() == 1)]
#     
#     mask2.Outcome.value_counts()
# 
# =============================================================================
#%%
def full_backtest(ticker_list=None, start=None, end=None, interval=None, 
                  fast=50, slow=200):

    outcome_dict = {}
    
    for i in range(len(ticker_list)):
        df = yf.download(tickers=ticker_list[i], start=start, end=end, interval=interval)
        df = crossover_strategy(df=df, fast=fast, slow=slow)
        selldates, outcome = backtest(df=df)
        df = sellsignal_df(df, selldates, outcome)
        winrate = df.Outcome.value_counts()[0] / df.Outcome.value_counts().sum()
        
        outcome_dict[ticker_list[i]] = outcome, winrate
        
        
    return outcome_dict
        #return df
        
        



#%% hovedprogram

if __name__ == "__main__":
    #lettere å bruke yf enn min egen hehe
    
    import yfinance as yf
    
# =============================================================================
#     df = yf.download(tickers='AAPL', start='2021-01-01', interval='1h')
#     df = crossover_strategy(df=df, fast=50, slow=200)
#     selldates, outcome = backtest(df)
#     df = sellsignal_df(df, selldates, outcome)
# =============================================================================
    

# =============================================================================
#     test_var = df_1.Outcome.value_counts()
#     sum(test_var)
#     test_wr = 4/6
#     wr = df_1.Outcome.value_counts()[0] / df_1.Outcome.value_counts().sum()
#     test_wr == wr
#     
#     
#     vals = [[1,2,3], [4,5,6]]
#     tickers = ['KO', 'AAPL']
#     outcome_dict = {}
#     winrate = 0.5
#     for i in range(len(tickers)):
#         outcome_dict[tickers[i]] = vals[i], winrate
# 
#     outcome_dict.items()
# 
#     for k, v in outcome_dict.items():
#         print(v)
# =============================================================================

    ticker_list = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOG', 'GOOGL',
                   'META']
    
    dict_ = full_backtest(ticker_list=ticker_list, start='2021-01-01', interval='1h')


    