# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 21:24:46 2022

@author: peter
"""

class scraper:
    
    def __init__(self, symbol, startDate, endDate):
        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate
    
        self.url = self.get_stock()
        
    def get_stock(self):
        
        "allows me to easily get any stock I want (from yahoo finance)"
        "without hardcoding the specific link"
        return "https://finance.yahoo.com/quote/" + self.symbol + "/history?p=" + self.symbol
    
if __name__ == "__main__":
    scrp = scraper('AAPL', startDate='01-01-2019', endDate='01-01-2020')
    scrp.get_stock()
    print(scrp.url)
        
    