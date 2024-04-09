import classes.Trading as Trading

rsi_above = []
cci_above = []
macd_above = []

def init(td, symbol):
    sma = td.sma(symbol)
    rsi = td.rsi(symbol)
    cci = td.cci(symbol)
    (macd, macdsignal, macdhist) = td.macd(symbol)

    print(macdhist)

    return True