import classes.Trading as Trading
import classes.Indicator as ind

rsi_above = []
cci_above = []
macd_above = []

def init(td, symbol):
    indicator = ind.Indicator(symbol)

    sma = indicator.sma()
    rsi = indicator.rsi()
    cci = indicator.cci()
    (macd, macdsignal, macdhist) = indicator.macd()

    print(sma)

    return True