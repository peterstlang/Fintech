# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 21:42:42 2022

@author: peter
"""
# Checking package

# imports
from selenium import webdriver
import time
from bs4 import BeautifulSoup

# from selenium.webdriver.support.ui import select


def get_stock(symbol):
    "allows me to easily get any stock I want (from yahoo finance)"
    "without hardcoding the specific link"
    return "https://finance.yahoo.com/quote/" + symbol + "/history?p=" + symbol

def gimme_soup_w_start_end(url, start="01-01-2018", end="01-01-2020"):
    from selenium.webdriver.common.keys import Keys
    
    chrome_options = webdriver.ChromeOptions(); 
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);

    driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe", 
                              options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(1)
    driver.get(url)
    driver.find_element_by_xpath('//*[@value="agree"]').click()

    time.sleep(1)
    drp = driver.find_element_by_xpath(
        '//div[@class="Pos(r) D(ib) C($linkColor) Cur(p)"]/*[name()="svg"][@data-icon="CoreArrowDown"]'
    )
    drp.click()
    time.sleep(1)

    name_start = driver.find_element_by_name("startDate")
    name_start.clear()
    name_start.send_keys(start)

    name_end = driver.find_element_by_name("endDate")
    name_end.clear()
    name_end.send_keys(end)

    time.sleep(0.5)
    driver.find_element_by_xpath('//span[contains(text(), "Done")]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//span[contains(text(), "Apply")]').click()
    time.sleep(1)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.find_element_by_xpath("//body").send_keys(Keys.CONTROL + Keys.END)
        time.sleep(0.5)
        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )

        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")

    return soup


def soup_to_scrape(soup):

    table = soup.find("table", class_="W(100%) M(0)")
    rows = table.find_all("tr", class_="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)")

    return rows


def scrape_it(rows):
    data_list = []

    for i in range(0, len(rows)):
        try:
            RowDict = {}
            Values = rows[i].find_all("td")

            if len(Values) == 7:
                RowDict["Date"] = Values[0].find("span").text.replace(",", "")
                RowDict["Open"] = Values[1].find("span").text.replace(",", "")
                RowDict["High"] = Values[2].find("span").text.replace(",", "")
                RowDict["Low"] = Values[3].find("span").text.replace(",", "")
                RowDict["Close"] = Values[4].find("span").text.replace(",", "")
                RowDict["Adj Close"] = Values[5].find("span").text.replace(",", "")
                RowDict["Volume"] = Values[6].find("span").text.replace(",", "")

                data_list.append(RowDict)

        except:
            print("Row Number: " + str(i))
        finally:
            i = i + 1

    return data_list


def dicts_to_df(list_of_dicts):
    import pandas as pd

    df = pd.DataFrame(list_of_dicts)
    return df


if __name__ == "__main__":
    url = get_stock("AAPL")
    soup = gimme_soup_w_start_end(url)
    rows = soup_to_scrape(soup)
    scraped = scrape_it(rows)
    df_unflipped = dicts_to_df(scraped)
