from BorsaReader.Extractor_Prices_Yahoo import  get_urls, get_prices_csv
import pandas as pd
import numpy as np
import pickle as pkl
from selenium.webdriver import Safari

tickers_path = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/listino_milano.csv'

companies = pd.read_csv(tickers_path)
urls = get_urls(companies)

driver = Safari()
for url in urls:

    print(url)
    try:
        get_prices_csv(url, driver)
    except:
        print('Problem downloading data')

driver.quit()
