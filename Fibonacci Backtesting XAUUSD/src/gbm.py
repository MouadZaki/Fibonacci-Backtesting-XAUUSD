import numpy as np
import pandas as pd

def calc_log_returns(price_series: pd.Series):
    return np.log(price_series / price_series.shift(1)).dropna()

def estimate_gbm_params(price_series: pd.Series):
    log_ret = calc_log_returns(price_series)
    mu = log_ret.mean()
    sigma = log_ret.std()
    return mu, sigma
