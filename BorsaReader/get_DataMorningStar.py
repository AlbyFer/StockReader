from BorsaReader.Extractor_Morningstar import  get_urls, produce_table_wrapper
import pandas as pd
import numpy as np
import pickle as pkl
from selenium.webdriver import Safari

save_path = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/BorsaMilano_dati_aziende.pkl'
tickers_path = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/listino_milano.csv'
base = 'https://www.morningstar.com/stocks/xmil/'

companies = pd.read_csv(tickers_path)

urls = get_urls(base, companies)

companies_data = {}
driver = Safari()
for url in urls:

    print(url)
    company = url.split('/')[5]
    table = produce_table_wrapper(url, driver)
    companies_data[company] = table

with open(save_path, 'wb') as file:
    pkl.dump(companies_data, file)

driver.quit()

