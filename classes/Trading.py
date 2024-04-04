from time import sleep
from datetime import datetime
import pytz

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetAssetsRequest, StopLimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, AssetClass, OrderClass, PositionSide, OrderStatus
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest

import classes.Logger as lg

API_KEY = '' # replace with your API
API_SECRET_KEY = ''
ALPACA_URL = 'https://paper-api.alpaca.markets'
initial_portfolio = 100000

class Trading:

    client = CryptoHistoricalDataClient()
    trading_client = TradingClient(API_KEY, API_SECRET_KEY, paper=True)

    def convert_to_local_time(self, tz):
        tz_local = tz.astimezone(pytz.timezone('Europe/Paris'))
        datetime_obj = datetime.strptime(str(tz_local), "%Y-%m-%d %H:%M:%S.%f%z")
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")


    def get_profit(self, balance):
        return {
            'portfolio': float(balance) - initial_portfolio,
            'percent': (float(balance) - initial_portfolio) / initial_portfolio * 100
        }

    def get_last_value(self, symbol):
        # single symbol request
        request_params = CryptoLatestQuoteRequest(symbol_or_symbols=symbol)

        latest_quote = self.client.get_crypto_latest_quote(request_params)

        return latest_quote[symbol].ask_price
    
    def log_if_filled(self, order):
        if self.is_filled(order[0]):
            pos = self.get_order_by_id(order[0])
            symbol = pos.symbol
            loss = pos.filled_avg_price
            balance = self.trading_client.get_account().portfolio_value

            if (order[1] == 1):
                lg.log_loss(symbol, loss, self.get_profit(balance), self.convert_to_local_time(pos.filled_at))
            else:
                lg.log_profit(symbol, loss, self.get_profit(balance), self.convert_to_local_time(pos.filled_at))

            return True
        return False
    
    def is_filled(self, id):
        pos = self.get_order_by_id(id)
        return pos.status == OrderStatus.FILLED
    
    def get_order_by_id(self, id):
        return self.trading_client.get_order_by_id(id)
    
    def sell_order(self, symbol, qty):
        market_order_data = MarketOrderRequest(
                            symbol=symbol,
                            qty=qty,
                            side=OrderSide.SELL,
                            time_in_force=TimeInForce.GTC
        )

        market_order = self.trading_client.submit_order(
                        order_data=market_order_data
        )

        return market_order.id

    def buy_order(self, symbol):
        market_order_data = MarketOrderRequest(
                            symbol=symbol,
                            notional=initial_portfolio / 100,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.IOC
        )

        market_order = self.trading_client.submit_order(
                        order_data=market_order_data
        )

        order_id = market_order.id

        last_value = float(self.get_order_by_id(order_id).filled_avg_price)
        profit_price = last_value + ((last_value / 100) * 2)
        loss_price = last_value - (last_value / 100)
        filled_qty = float(self.get_order_by_id(order_id).filled_qty)

        lg.log_buy(symbol, last_value, loss_price, profit_price, self.convert_to_local_time(self.get_order_by_id(order_id).filled_at))

        res = {
            'sym': symbol,
            'qty': filled_qty - (filled_qty * 0.0025),
            'loss': loss_price,
            'profit': profit_price
        }

        return res
    
    def get_all_symbols(self):
        search_params = GetAssetsRequest(asset_class=AssetClass.CRYPTO)

        assets = self.trading_client.get_all_assets(search_params)
        res = []

        for asset in assets:
            res.append(asset.symbol)
        
        return res
    
    def time_to_market_close(self):
        clock = self.trading_client.get_clock()
        time_left = (clock.next_close - clock.timestamp).total_seconds()

        lg.log_time_until_market_close(datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S"), time_left)
        return time_left


    def wait_for_market_open(self):
        clock = self.trading_client.get_clock()
        lg.log_time_until_market_open(datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S"), clock)
        if not clock.is_open:
            time_to_open = (clock.next_open - clock.timestamp).total_seconds()
            sleep(round(time_to_open))