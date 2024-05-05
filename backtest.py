import vectorbt as vbt

def backtest(api_key, api_secret_key):
    vbt.settings.data['alpaca']['key_id'] = api_key
    vbt.settings.data['alpaca']['secret_key'] = api_secret_key

    data = vbt.AlpacaData.download_symbol("BTC/USD", start='2024-04-01', end='2024-04-08', timeframe="1m")

    print(data)