import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from BackTester import BackTester

def smaXover(col):
    sma_s = col.rolling(50).mean()
    sma_l = col.rolling(100).mean()

    return np.where(sma_s > sma_l, 1, 0)

def emaXover(col):
    ema_s = col.ewm(5, adjust=True).mean()
    ema_l = col.ewm(10, adjust=True).mean()

    return np.where(ema_s > ema_l, 1, 0)

def ideal(col):
    return np.where(col.pct_change() > 0, 1, -1)

test = BackTester('AAPL', ideal, start='2020-01-01').test()
test.displayStats()
test.plotReturns()