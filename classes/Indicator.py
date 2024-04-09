import numpy as np
import talib as ta
import pandas as pd
import classes.MarketInfo as mk

class Indicator:
    timeList = []
    openList = []
    highList = []
    lowList = []
    closeList = []
    volumeList = []

    def __init__(self, symbol):
        timeList = []
        openList = []
        highList = []
        lowList = []
        closeList = []
        volumeList = []

        bars = mk.get_symbol_data(symbol)

        for bar in bars:
            timeList.append(bar.timestamp)
            openList.append(bar.open)
            highList.append(bar.high)
            lowList.append(bar.low)
            closeList.append(bar.close)
            volumeList.append(bar.volume)
        
        self.timeList = np.array(timeList)
        self.openList = np.array(openList,dtype=np.float64)
        self.highList = np.array(highList,dtype=np.float64)
        self.lowList = np.array(lowList,dtype=np.float64)
        self.closeList = np.array(closeList,dtype=np.float64)
        self.volumeList = np.array(volumeList,dtype=np.float64)


    def sma(self):
        sma = ta.SMA(self.closeList,20)

        return sma
    
    def macd(self):
        macd, macdsignal, macdhist = ta.MACD(self.closeList, fastperiod=12, slowperiod=26, signalperiod=9)

        return (macd, macdsignal, macdhist)
    
    def cci(self):
        cci = ta.CCI(self.highList, self.lowList, self.closeList, timeperiod=14)

        return cci
    
    def rsi(self):
        rsi = ta.RSI(self.closeList, timeperiod=14)

        return rsi