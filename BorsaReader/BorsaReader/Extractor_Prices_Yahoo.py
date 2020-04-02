import pandas as pd
import time


def get_urls(tickers, base_url= 'https://query1.finance.yahoo.com/v7/finance/download/'):

    urls = [base_url + x + '.MI?period1=1427932800&period2=1585785600&interval=1mo&events=history' for x in tickers['Ticker']]

    return urls

def get_prices_csv(url, driver):

    driver.get(url)
    time.sleep(5)

    return None