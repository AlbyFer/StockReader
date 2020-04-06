
from BorsaReader.Model_builder import read_financials, format_financials_prediction
import pickle as pkl


path_to_financials = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/BorsaMilano_dati_aziende.pkl'
path_to_model = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/model_milano_2.pkl'

ticker = 'INDB'



ratios = ["Revenue EUR Mil", "Earnings Per Share EUR", "Dividends EUR", "Shares Mil", "Operating Cash Flow EUR Mil",
          "Working Capital EUR Mil", "Return on Equity %", "Return on Assets %", "Interest Coverage",
          "Cap Ex as a % of Sales", "Total Stockholders' Equity", "Days Sales Outstanding", "Payables Period",
          "Inventory Turnover", "Fixed Assets Turnover", "Current Ratio", "Debt/Equity"]

financials = read_financials(path_to_financials)
single_company = format_financials_prediction(financials, ticker, ratios)

with open(path_to_model, 'rb') as handle:
    model = pkl.load(handle)

estimated_price = model.predict(single_company.values)
print(estimated_price[0])
