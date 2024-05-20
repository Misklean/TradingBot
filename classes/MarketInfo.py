from enum import Enum
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

client = CryptoHistoricalDataClient()

class TimeFrameEnum(Enum):
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'

def get_symbol_data(symbol, custom_timeframe):
    # Determine the start date based on the custom_timeframe
    end_date = datetime.now()

    if custom_timeframe == TimeFrameEnum.MINUTE:
        print("MINUTES")
        start_date = end_date - timedelta(minutes=50)
        timeframe = TimeFrame.Minute
    elif custom_timeframe == TimeFrameEnum.HOUR:
        print("HOUR")
        start_date = end_date - timedelta(hours=50)
        timeframe = TimeFrame.Hour
    elif custom_timeframe == TimeFrameEnum.DAY:
        print("DAY")
        start_date = end_date - timedelta(days=50)
        timeframe = TimeFrame.Day

    request_params = CryptoBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start_date,
        end=end_date
    )

    bars = client.get_crypto_bars(request_params)
    bars_df = bars.df

    # Ensure we only return the last 50 rows, as the API might return more data
    if len(bars_df) > 50:
        bars_df = bars_df.tail(50)

    return bars_df

def get_last_value(symbol):
    request_params = CryptoLatestQuoteRequest(symbol_or_symbols=symbol)

    latest_quote = client.get_crypto_latest_quote(request_params)

    return latest_quote[symbol].ask_price