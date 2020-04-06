import pandas as pd
import pickle as pkl
import numpy as np
from hyperopt import fmin, tpe, Trials, STATUS_OK
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
import pickle



def read_prices(path_to_folder, ticker, stock_exchange='.MI'):

    file = path_to_folder + ticker + stock_exchange + '.csv'
    data = pd.read_csv(file)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', drop=True, inplace=True)

    return data


def read_financials(path_to_file):

    with open(path_to_file, 'rb') as file:
        financials = pkl.load(file)

    return financials

def format_financials_prices(financials, ticker, path_to_folder_prices, interest_ratios, stock_exchange='.MI'):

    try:
        hist_prices = read_prices(path_to_folder=path_to_folder_prices, ticker=ticker, stock_exchange=stock_exchange)
    except FileNotFoundError:
        print('No price data for company ' + ticker)
        return None

    if financials[ticker] is None:
        return None
    else:
        pass

    upper_date = financials[ticker].columns[-1]
    lower_date = financials[ticker].columns[-2]

    prices = hist_prices.loc[(hist_prices.index >= lower_date) & (hist_prices.index <= upper_date), 'Close']
    median_price = prices.median()

    result = financials[ticker].reindex(interest_ratios)[lower_date]
    result['Price'] = median_price
    result['Company'] = ticker

    result.index = pd.Index([x.replace('%', 'perc') for x in result.index])
    result.index = pd.Index([x.replace('\xa0', ' ') for x in result.index])
    result.name = None


    if 'Dividends EUR' in result.index:
        if np.isnan(result['Dividends EUR']):
            result['Dividends EUR'] = 0
        else:
            return result.to_frame().T
    else:
        pass

    return result.to_frame().T



def hyperopt_XGBoost(param_space, X_train, y_train, X_test, y_test, num_eval, metric, trials_path_pickle=None,
                     savepath_trials=None, savepath_model=None, cv=5, type='regression'):

    if trials_path_pickle is not None:
        trials = pickle.load(open(trials_path_pickle, "rb"))
    else:
        trials = Trials()

    if type == 'classification':

        def objective_function(params):
            clf = GradientBoostingClassifier(**params)
            score = cross_val_score(clf, X_train, y_train, cv=cv, scoring=metric).mean()
            return {'loss': -score, 'status': STATUS_OK}
    else:

        def objective_function(params):
            clf = GradientBoostingRegressor(**params)
            score = cross_val_score(clf, X_train, y_train.values.ravel(), cv=cv, scoring=metric).mean()
            return {'loss': -score, 'status': STATUS_OK}

    best_params = fmin(objective_function,
                       param_space,
                       algo=tpe.suggest,
                       max_evals=num_eval,
                       trials=trials,
                       rstate=np.random.RandomState(1))

    for param in best_params.keys():
        if best_params[param].is_integer():
            best_params[param] = int(best_params[param])

    losses = [x['result']['loss'] for x in trials.trials]

    if type == 'classification':
        best_model = GradientBoostingClassifier().set_params(**best_params)
        best_model.fit(X_train, y_train)
        test_score = best_model.score(X_test, y_test)

    else:
        best_model = GradientBoostingRegressor().set_params(**best_params)
        best_model.fit(X_train, y_train.values.ravel())
        test_score = best_model.score(X_test, y_test.values.ravel())




    print("")
    print("##### Results")
    print("Score best parameters: ", min(losses) * -1)
    print("Best parameters: ", best_params)
    print("Test Score: ", test_score)
    print("Parameter combinations evaluated: ", num_eval)

    if savepath_trials is not None:
        pickle.dump(trials, open(savepath_trials, "wb"))
    else:
        pass

    if savepath_model is not None:
        pickle.dump(best_model, open(savepath_model, "wb"))
    else:
        pass

    return (trials, best_model, test_score)
