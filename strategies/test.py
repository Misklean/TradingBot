import classes.Trading as Trading
import classes.Indicator as ind

rsi_above = []
cci_above = []
macd_above = []

def init(data):
    indicator = ind.Indicator(data)
    
    sma = indicator.sma(window=20)
    macd, macdsignal, _ = indicator.macd()
    cci = indicator.cci(timeperiod=14)
    rsi = indicator.rsi(timeperiod=14)
    
    # Example strategy: Buy when close price is above SMA and MACD line crosses above signal line
    entries = (data['close'] > sma)
    exits = (data['close'] < sma)
    
    return entries, exits
