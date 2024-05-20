from time import sleep
from datetime import datetime
import classes.Trading as Trading
import classes.Logger as lg
import strategies.test as tst
import classes.MarketInfo as mk
from classes.MarketInfo import TimeFrameEnum

sym = []
positions = []
sell_orders = []

def check_pos(td):
  for pos in positions:
    #print(f"{pos['sym']} | {pos['qty']} | {pos['loss']} | {pos['profit']}")

    value = mk.get_last_value(pos['sym'])

    lg.log_compute_sell_orders(pos['sym'], value, pos['loss'], pos['profit'], datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S"))

    if (value >= pos['profit']):
      sell_orders.append((td.sell_order(pos['sym'], pos['qty']), 0))
      positions.remove(pos)

    elif (value < pos['loss']):
      sell_orders.append((td.sell_order(pos['sym'], pos['qty']), 1))
      positions.remove(pos)

  for sell in sell_orders[:]:
    if (td.log_if_filled(sell)):
      sell_orders.remove(sell)

def paper_trading(api_key, api_secret_key):
    td = Trading.Trading(api_key, api_secret_key)
    symbol = 'BTC/USD'
    
    while True:
        if td.time_to_market_close() > 120:
            data = mk.get_symbol_data(symbol, TimeFrameEnum.MINUTE)
            entries, exits = tst.init(data)
            
            print(entries.iloc[-1])
            if entries.iloc[-1]:  # Check the last entry signal
                order = td.buy_order(symbol)
                positions.append(order)

        check_pos(td)
        sleep(60)