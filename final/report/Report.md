# Fintech Final Project

## Trading Strategy for SPY

* b03902089 資工四 林良翰

## Introduction

* Data Set : https://finance.yahoo.com/quote/SPY/history?p=SPY
* Start from 1993.1.29 to 2017.12.27
  <img src="all_value.png" width="350px"> 

## Program Demonstration

* Environment: Mac OS Sierra 10.12.6

* Language & Version: Python 3.6.2

* Packages:

  * argparse
  * numpy >= 1.13.1
  * talib >= 0.4.10
  * matplotlib >= 2.0.2 (optional)

*  Installation
    ```brew install python3```
    ```pip3 install [package_name]```

*  Program Usage

    *  Files: `Indicators.py`, `Utilities.py`, `myStrategy.py`

    * Execute: ```python3 myStrategy.py```

    * Coding Example:

        ```python
        import pandas as pd
        pastData = pd.read_csv('SPY.csv')
        from myStrategy import myStrategy        
        action = myStrategy(pastData)
        ```

## Baseline Methods

| Moving Average (MA)<br><img src="all_ma.png", width="280px"/> | Exponential Moving Average (EMA)<br><img src="all_ema.png", width="280px"/> |
| :--------------------------------------- | :--------------------------------------- |
| <b>Stochastic Oscillator (KD)</b><br><img src="all_kd.png", width="280px"/> | <b>Relative Strength Index (RSI)</b><br><img src="all_rsi.png", width="280px"/> |
| <b>MA Convergence / Divergence (MACD)</b><br><img src="all_macd.png" width="280px"> | <b>Rate of Change (BIAS)</b><br><img src="all_bias.png" width="280px"> |
| <b>Sharpe Ratio (SR)</b><br><img src="all_sr.png" width="280px"> | Note:<br />1. Upper graph is the value of indicators.<br />2. Bottom graph is the asset histories.<br />3. Some indicators have different periods. |

## Analysis

* Initial capital: 1000
* Start investment at different day, ending at 2017.12.27
* Some indicators have no different periods.
  * Start at first day (1993.1.29)
    <img src="all_analysis.png">
  * Start at last 400-th day (2016.5.26)
    <img src="400_analysis.png">
  * Start at last 120-th day (2017.7.7)<img src="120_analysis.png">

## Experiments

* Ensemble all indicators (in Analysis), initial capital = 1000, starting from last 400-th day.
  <img src="eval_all.png", width="400px"> <b>Final Earn = 122.46</b>


* Select some indicators, initial capital = 1000, starting from last 400-th day.

  * EMA60, EMA120, EMA240
  * RSI5, RSI10
  * MACD
  * BIAS5, BIAS10
  * SR30, SR60, SR120, SR240

    <img src="eval_spec.png" width="400px"> <b>Final Earn = 233.36</b>

## Conclusions

* Some indicators are not worth referencing.
  * MA & EMA with period ≤ 20
  * KD
  * BIAS > 30
  * RSI > 30
* There is no perfect indicators that always have correct action (sell / buy) advice.