

import pandas as pd
from bs4 import BeautifulSoup
import time



def get_urls(base_url, tickers):

    urls = [base_url + x + '/quote' for x in tickers['Ticker']]

    return urls


def get_tables(url, driver):

    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")

    ratios_link = soup.find_all('a', class_='mds-link ng-binding')[0]['href']
    ratios_link = 'https:' + ratios_link

    driver.get(ratios_link)
    time.sleep(4)
    html = driver.page_source
    list_tables = pd.read_html(html, na_values='—')

    del list_tables[3]
    
    return list_tables


def format_tables(table):

    table = table.iloc[lambda x: x.index % 2 != 0]
    try:
        table.drop('TTM', axis=1, inplace=True)
    except KeyError:
        pass
    try:
        table.drop('Latest Qtr', axis=1, inplace=True)
    except KeyError:
        pass

    table.set_index(list(table)[0], inplace=True)
    table.index.name = None
    columns = pd.to_datetime(table.columns.values)
    table.columns = columns


    return table


def produce_table_wrapper(url, driver):

    try:
        tables = get_tables(url, driver)
    except:
        print('No data on company')
        return None

    all_tables = []
    for table in tables:
        all_tables.append(format_tables(table))

    all_tables = pd.concat(all_tables, axis=0, sort=True)

    return all_tables