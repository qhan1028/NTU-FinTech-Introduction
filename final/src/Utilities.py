#
#   Fintech Final Project: Trading Strategy for SPY
#   Utilities.py
#
#   Written by Qhan
#   2017.12
#

import pandas as pd
import numpy as np


def ReadData(filename):
    data = pd.read_csv(filename)
    return data


def Normalize(data):
    return ((data - data.mean()) / data.std())


def Evaluate(close, decision, initCapital, start_day=0):
    total_assets = []
    dec_size = len(decision)
    capital = initCapital
    total = capital
    units, d = 0, 0
    for i, price in enumerate(close):
        if d >= dec_size: break
        if i == int(decision[d][0]):
            action = decision[d][1]
            d += 1
            if i >= start_day:
                if action > 0 and units == 0:
                    units = capital / price
                    capital = 0
                elif action < 0 and units > 0:
                    capital = price * units
                    units = 0
        total = capital + price * units
        total_assets.append(total)
    print("Final Asset:", total)
    return total_assets


def MergeDecision(decisions, weights, max_len):
    merged_decision = np.array([range(max_len), np.zeros(max_len)]).T
    for decision, weight in zip(decisions, weights):
        for d in decision:
            merged_decision[d[0]][1] += d[1] * weight
    return merged_decision


## Test Indicator and Plot Result

def PlotArea(ax, asset_history, baseline):
    for x, y in enumerate(asset_history):
        area = [(x-0.5, baseline), (x-0.5, y), (x+0.5, y), (x+0.5, baseline)]
        if y >= capital:
            poly = Polygon(area, facecolor='C0')
        else:
            poly = Polygon(area, facecolor='C3')
        ax.add_patch(poly)


def TestIndicator(data, indicator, capital=1000, periods=[5, 10, 20, 30, 60, 120, 240], 
                  days='all', savefig=False, showfig=True, start_day=0):
    print("Init Capital:", capital)
    values, assets = [], []
    multiple_periods_indicators = ["ma", "ema", "rsi", "sr", "bias"]
    close = np.array(data["Adj Close"])
    
    if indicator in multiple_periods_indicators:
        for p in periods:
            if indicator == "ma": decision, value = MA(close, p)
            elif indicator == "ema": decision, value = EMA(close, p)
            elif indicator == "rsi": decision, value = RSI(close, p)
            elif indicator == "bias": decision, value = BIAS(close, p)
            elif indicator == "sr": decision, value = SR(close, p)
            else: decision, value = [], []
            values.append(np.array(value))
            assets.append(np.array(Evaluate(close, decision, capital, start_day=start_day)))
    else:
        if indicator == "macd": decision, value = MACD(close)
        elif indicator == "kd": decision, value = KD(data)
        else: decision, value = [], []
        values.append(np.array(value))
        assets.append(np.array(Evaluate(close, decision, capital, start_day=start_day)))

    #
    #   draw values
    #
    plt.figure(figsize=(16, 16))
    plt.subplot(211)
    if len(values) > 1:
        for i, (value, p) in enumerate(zip(values, periods)):
            plt.plot(value[start_day:], label=indicator + str(p), linewidth='0.8')
    else:
        plt.plot(values[0][start_day:], label=indicator, linewidth='0.8')

    if indicator in ["sr", "kd", "macd", "bias"]: plt.axhline(y=0, color='C3')
    elif indicator is "rsi": plt.axhline(y=50, color='C3')
    plt.title(indicator.upper())
    plt.grid(linestyle='--')
    plt.legend()

    #
    #   draw asset history
    #
    plt.subplot(212)
    if len(assets) > 1:
        for i, (asset, p) in enumerate(zip(assets, periods)):
            plt.plot(asset[start_day:], label=indicator+"_asset" + str(p), linewidth='0.8')
    else:
        plt.plot(assets[0][start_day:], label=indicator+"_asset", color='k', linewidth='0.5')
        PlotArea(plt.gca(), assets[0][start_day:], capital)

    plt.axhline(y=capital, color="red")
    plt.title(indicator.upper() + " Assets")
    plt.grid(linestyle='--')
    plt.legend()
    if savefig: plt.gcf().savefig(days + "_" + indicator + ".png")
    if showfig: plt.show()