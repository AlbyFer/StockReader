import pandas as pd
import time




def produce_urls_nasdaq(base):

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    urls = [base + x + '.htm' for x in letters]

    return urls


def get_tables_nasdaq(url, driver):

    time.sleep(7)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    list_tables = pd.read_html(html)

    tickers_table = list_tables[4]

    return tickers_table

