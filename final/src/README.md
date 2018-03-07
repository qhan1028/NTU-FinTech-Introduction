# Fintech 2017 Final Project
## Trading Strategy for SPY

* b03902089 資工四 林良翰

0. Environment: Mac OS Sierra 10.12.6
1. Language & Version: Python 3.6.2
2. Packages:
    * argparse
    * numpy >= 1.13.1
    * talib >= 0.4.10
    * matplotlib >= 2.0.2 (optional)
3. Installation
    ```brew install python3```
    ```pip3 install [package_name]```
4. Program Usage
    * Execute: ```python3 myStrategy.py```
    * Help Message: ```python3 myStrategy.py -h```
    * Import Function:
        ```python3
        import pandas as pd
        pastData=pd.read_csv('SPY.csv')
        
        from myStrategy import myStrategy        
        action = myStrategy(pastData)
        ```
5. Notices
    * Please place the SPY.csv into the same directory
    * SPY.csv need to have completed data since 1993 or at least 2007
