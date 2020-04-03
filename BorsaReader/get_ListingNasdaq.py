from BorsaReader.Extractor_Nasdaq import  produce_urls_nasdaq, get_tables_nasdaq
import pandas as pd
import pickle as pkl
from selenium.webdriver import Safari


save_path = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/listing_nasdaq.csv'
base = 'http://eoddata.com/stocklist/NASDAQ/'

urls =produce_urls_nasdaq(base)

tables = []
driver = Safari()
for url in urls:

    print(url)
    tables.append(get_tables_nasdaq(url, driver))

tables = pd.concat(tables)
tickers = tables['Code'].to_frame()
tickers.column = 'Ticker'
tickers.to_csv(save_path, index=False)

driver.quit()
