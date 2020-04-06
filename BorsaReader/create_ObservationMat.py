import pandas as pd

from BorsaReader.Model_builder import read_financials, format_financials_prices


ratios = ["Revenue USD Mil", "Earnings Per Share USD", "Dividends USD", "Shares Mil", "Operating Cash Flow USD Mil",
          "Working Capital USD Mil", "Return on Equity %", "Return on Assets %", "Interest Coverage",
          "Cap Ex as a % of Sales", "Total Stockholders' Equity", "Days Sales Outstanding", "Payables Period",
          "Inventory Turnover", "Fixed Assets Turnover", "Current Ratio", "Debt/Equity", "R&D"]

path_to_financials = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/Nasdaq_companies_data.pkl'
path_to_folder_prices = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/Prezzi/'
path_to_save = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/Obs_mat_nasdaq.csv'

financials = read_financials(path_to_financials)

data = []
for ticker in financials.keys():
    print('Executing company ' + ticker)
    data.append(format_financials_prices(financials, ticker, path_to_folder_prices, ratios, stock_exchange=''))

obs_mat = pd.concat(data, axis=0)
obs_mat.set_index('Company', drop=True, inplace=True)
obs_mat.to_csv(path_to_save)
