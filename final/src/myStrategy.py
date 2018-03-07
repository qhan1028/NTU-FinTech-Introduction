#
#   Fintech Final Project: Trading Strategy for SPY
#   myStrategy.py
#
#   Written by Qhan
#   2017.12
#

import argparse
import numpy as np
from Utilities import *
from Indicators import *

def myStrategy(data, start_day=0, capital=1000):
    datalen = len(data)
    close = np.array(data["Adj Close"])

    # select indicators
    select_list = [
        {"type": "ema", "periods": [60, 120, 240], "weight": 1/3},
        {"type": "rsi", "periods": [5, 10], "weight": 1/2},
        {"type": "macd", "periods": [], "weight": 1},
        {"type": "bias", "periods": [5, 10, 20], "weight": 1/3},
        {"type": "sr", "periods": [30, 60, 120, 240], "weight": 1/4}
    ]

    # compute indicators
    decisions, weights = [], []

    for i in select_list:
        if i["type"] in ["ma", "ema", "rsi", "bias", "sr"]:
            for p in i["periods"]:
                decisions.append(eval(i["type"].upper())(close, period=p)[0])
                weights.append(i["weight"])
        elif i["type"] is "kd":
            decisions.append(eval("KD")(data)[0])
            weights.append(i["weight"])
        elif i["type"] is "macd":
            decisions.append(eval("MACD")(close)[0])
            weights.append(i["weight"])

    # merge
    final_decision = MergeDecision(decisions, weights, datalen)

    # evaluate
    assets = Evaluate(close, final_decision, capital, start_day=start_day)
    
    action = final_decision[-1][1]
    print("Strategy: " + ("buy" if action > 0 else "sell"))

    return np.sign(action)

def main(args):
    # read data
    data = ReadData(args.filename)
    datalen = len(data)
    
    # parameters
    days = int(args.first_day)
    start_day = datalen - days if days > 0 else 0
    capital = float(args.capital)
    
    # execute
    myStrategy(data, start_day=start_day, capital=capital)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser("My Strategy")
    parser.add_argument("-i", "--filename", metavar="FILEPATH", default="SPY.csv", help="input data.")
    parser.add_argument("-s", "--first_day", metavar="N", default=400, help="first day for baseline asset.")
    parser.add_argument("-c", "--capital", metavar="N", default=1000, help="initial capital.")
    args = parser.parse_args()
    for k, v in vars(args).items(): 
        title = k.title().replace("_", " ") + ":"
        if k is "first_day" and v != 0: v = "-" + str(v) + ":"
        print(title, v)
    main(args)