import pandas as pd
import pickle as pkl
import requests
from bs4 import BeautifulSoup
import re
from bs4.diagnose import diagnose
import time
import os

/Users/albertoferrando/Google\ Drive/Progetti/Investimenti/BorsaReader/Storage/BorsaMilano_dati_aziende.pkl


def read_prices(path_to_folder, ticker):

    file = path_to_folder + ticker + '.MI.csv'
    data = pd.read_csv(file)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', drop=True, inplace=True)

    return data


def read_financials(path_to_file):

    with open(path_to_file, 'rb') as file:
        financials = pkl.load(file)

    return financials

def format_financials_prices(financials, ticker, path_to_folder_prices, interest_ratios):

    try:
        hist_prices = read_prices(path_to_folder=path_to_folder_prices, ticker=ticker)
    except FileNotFoundError:
        print('No price data for company ' + ticker)
        return None

    upper_date = financials[ticker].columns[-1]
    lower_date = financials[ticker].columns[-2]

    prices = hist_prices.loc[(hist_prices.index >= lower_date) & (hist_prices.index <= upper_date), 'Close']
    median_price = prices.median()

    result = financials[ticker].loc[interest_ratios, lower_date]
    result['Price'] = median_price
    result['Company'] = ticker

    return result



