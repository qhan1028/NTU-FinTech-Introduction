#
#   Fintech Final Project: Trading Strategy for SPY
#   Indicators.py
#
#   Written by Qhan
#   2017.12
#

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import talib as ta

#
#   Moving Average
#
def MA(close, period):
    decision = []
    MAs = ta.MA(close, period)
    for i in range(period, close.size):
        if close[i] > MAs[i]:
            decision.append([i, 1])
        else:
            decision.append([i, -1])
    return decision, MAs


def EMA(close, period): # exponential
    decision = []
    EMAs = ta.MA(close, period, matype=1)
    for i in range(period, close.size):
        if close[i] > EMAs[i]:
            decision.append([i, 1])
        else:
            decision.append([i, -1])
    return decision, EMAs


#
#   Stochastic Oscillator
#
def KD(data):
    high, low, close = np.array(data["High"]), np.array(data["Low"]), np.array(data["Close"])
    K, D = ta.STOCH(high, low, close)
    decision = []
    for i, (k, d) in enumerate(zip(K, D)):
        if k > d:
            decision.append([i, 1])
        else:
            decision.append([i, -1])
    return decision, K - D


#
#   Relative Strength Index
#
def RSI(close, period, upper=70, bottom=30):
    decision = []
    RSIs = ta.RSI(close, period)
    for i in range(period, RSIs.size):
        if RSIs[i] >= upper:
            decision.append([i, -1])
        elif RSIs[i] <= bottom:
            decision.append([i, 1])
        else:
            decision.append([i, 0])
    return decision, RSIs

            
#
#   Moving Average Convergence / Divergence
#
def MACD(close):
    decision = []
    diff, diff_ema, macd_hist = ta.MACD(close)
    for i in range(26, close.size):
        if macd_hist[i] > 0:
            decision.append([i, 1])
        else:
            decision.append([i, -1])
    return decision, macd_hist
            

#
#   Bias Ratio (Rate of Change)
#
def BIAS(close, period, upper=1, bottom=-1):
    decision = []
    BIAS = np.array(ta.ROC(close, period))
    real_bias = BIAS[period:]
    mean, std = np.mean(real_bias), np.std(real_bias)
    upper = mean + upper * std
    bottom = mean + bottom * std
    for i in range(period, BIAS.size):
        if BIAS[i] > upper:
            decision.append([i, -1])
        elif BIAS[i] < bottom:
            decision.append([i, 1])
        else:
            decision.append([i, 0])
    return decision, BIAS


#
#   Sharpe Ratio
#
def SR(close, period, upper=0.001, bottom=-0.001):
    decision = []
    ratios = []
    for i in range(period, close.size):
        mu = 0
        sigma = 0
        deltaS = []
        for j in range(i-period, i):
            ds = close[j+1] - close[j]
            mu += (ds / close[j])
            deltaS.append(ds)
        mu /= period
        for j, ds in zip(range(i-period, i), deltaS):
            sigma += (ds / close[j] - mu) ** 2
        sigma = (sigma / period) ** (1/2)
        ratio = mu / sigma
        ratios.append(ratio)
        if ratio > upper:
            decision.append([i, 1])
        elif ratio < bottom:
            decision.append([i, -1])
        else:
            decision.append([i, 0])
    return decision, ratios