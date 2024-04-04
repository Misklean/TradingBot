from time import sleep
from datetime import datetime
import classes.Trading as Trading
import classes.Logger as lg

td = Trading.Trading()
sym = []
positions = []
sell_orders = []

def check_pos():
  for pos in positions:
    #print(f"{pos['sym']} | {pos['qty']} | {pos['loss']} | {pos['profit']}")
    value = td.get_last_value(pos['sym'])

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

def paper_trading():
  symbol = 'BTC/USD'

  while True:

    #if td.time_to_market_close() > 120:
    if len(positions) == 0:
      order = td.buy_order(symbol)
      positions.append(order)

    check_pos()
    sleep(60)
    #break

paper_trading()