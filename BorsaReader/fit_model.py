import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from hyperopt import hp
from hyperopt.pyll.base import scope
from BorsaReader.Model_builder import hyperopt_XGBoost



### ================================================================================================================ ###
### ITALIAN DATA

save_trials_name = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/trials_milano_2.pkl'
save_model_name = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/model_milano_2.pkl'

mib_companies = pd.read_csv('/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/Obs_mat.csv')
mib_companies = mib_companies.loc[:, mib_companies.columns != 'R&D'].dropna()

renamed_columns = ['Company', 'Revenue', 'Earnings Per Share', 'Dividends',
       'Shares Mil', 'Operating Cash Flow Mil', 'Working Capital Mil',
       'Return on Equity perc', 'Return on Assets perc', 'Interest Coverage',
       'Cap Ex as a perc of Sales', "Total Stockholders' Equity",
       'Days Sales Outstanding', 'Payables Period', 'Inventory Turnover',
       'Fixed Assets Turnover', 'Current Ratio', 'Debt/Equity',
       'Price']

mib_companies.columns = renamed_columns

ind_vars = ['Revenue', 'Earnings Per Share', 'Dividends',
       'Shares Mil', 'Operating Cash Flow Mil', 'Working Capital Mil',
       'Return on Equity perc', 'Return on Assets perc', 'Interest Coverage',
       'Cap Ex as a perc of Sales', "Total Stockholders' Equity",
       'Days Sales Outstanding', 'Payables Period', 'Inventory Turnover',
       'Fixed Assets Turnover', 'Current Ratio', 'Debt/Equity']

target = ['Price']

param_hyperopt= {'learning_rate': hp.loguniform('learning_rate', np.log(0.01), np.log(1)),
                 'max_depth': scope.int(hp.quniform('max_depth', 5, 15, 1)),
                 'n_estimators': scope.int(hp.quniform('n_estimators', 5, 700, 1)),}

X_train, X_test, y_train, y_test = train_test_split(mib_companies[ind_vars], mib_companies[target], test_size=0.30)
trials, model, test_score = hyperopt_XGBoost(param_hyperopt, X_train, y_train, X_test, y_test, 20,
                                             'neg_root_mean_squared_error', savepath_trials=save_trials_name,
                                             savepath_model=save_model_name, cv=3, trials_path_pickle=None)


mib_companies['PredictedPrice'] = model.predict(mib_companies[ind_vars])
mib_companies['Delta'] = (mib_companies['Price'] - mib_companies['PredictedPrice'])/mib_companies['Price']
mib_companies.sort_values(by='Delta', ascending=True)


### ================================================================================================================ ###
### NASDAQ DATA






