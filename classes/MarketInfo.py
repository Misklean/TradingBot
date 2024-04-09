from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

client = CryptoHistoricalDataClient()

def get_symbol_data(symbol):
    request_params = CryptoBarsRequest(
                    symbol_or_symbols=symbol,
                    timeframe=TimeFrame.Day,
                    start=datetime(2022, 7, 1),
                    end=datetime(2022, 9, 1)
                )

    bars = client.get_crypto_bars(request_params)
    bars.df

    return bars[symbol]

def get_last_value(symbol):
    request_params = CryptoLatestQuoteRequest(symbol_or_symbols=symbol)

    latest_quote = client.get_crypto_latest_quote(request_params)

    return latest_quote[symbol].ask_price