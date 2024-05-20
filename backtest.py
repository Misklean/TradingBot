import vectorbt as vbt
import pandas as pd
from alpaca_trade_api.rest import REST, TimeFrame
from strategies.test import init

def backtest(api_key, api_secret_key):
    # Set up Alpaca API client
    api = REST(api_key, api_secret_key, base_url='https://data.alpaca.markets')

    # Download historical data for BTCUSD
    bars = api.get_crypto_bars("BTC/USD", TimeFrame.Minute, start='2024-04-01T00:00:00Z', end='2024-04-08T23:59:59Z').df

    # Ensure the data is in the correct format for vectorbt
    bars.index = pd.to_datetime(bars.index)
    data = bars[['open', 'high', 'low', 'close', 'volume']]

    # Generate signals
    entries, exits = init(data)

    # Run backtest
    pf = vbt.Portfolio.from_signals(
        close=data['close'],
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001
    )

    # Print results
    print(pf.stats())
    pf.plot().show()