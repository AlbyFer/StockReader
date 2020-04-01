import pandas as pd
import requests
from bs4 import BeautifulSoup
import re



def get_tickers_single_page(url):

    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all('div', class_='c-chart-table sortable-table')
    classes = soup.find_all('div', class_='c-row c-row--azioni c-row--record')

    single_letter = []
    for i in range(0, len(classes)):
        single_letter.append(classes[i]['id'])

    return single_letter

def produce_urls(base):

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', '', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'Z']

    urls = [base + '/' + x for x in letters]

    return urls

def find_listing_milano(base, save_path=None):

    urls = produce_urls(base)

    all_results = []
    for url in urls:
        all_results = all_results + get_tickers_single_page(url)

    all_results = [re.sub('.MI', '', x) for x in all_results]

    all_results = pd.DataFrame({'Ticker': all_results})

    if save_path:
        all_results.to_csv(save_path, index=False)

    return all_results
