import numpy as np
import talib as ta

class Indicator:
    def __init__(self, data):
        self.data = data
        self.closeList = data['close'].values
        self.highList = data['high'].values
        self.lowList = data['low'].values

    def sma(self, window=20):
        return ta.SMA(self.closeList, window)

    def macd(self):
        macd, macdsignal, macdhist = ta.MACD(self.closeList, fastperiod=12, slowperiod=26, signalperiod=9)
        return macd, macdsignal, macdhist

    def cci(self, timeperiod=14):
        return ta.CCI(self.highList, self.lowList, self.closeList, timeperiod=timeperiod)

    def rsi(self, timeperiod=14):
        return ta.RSI(self.closeList, timeperiod=timeperiod)
