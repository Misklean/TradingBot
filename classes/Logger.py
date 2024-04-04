def log_buy(symbol, last, loss, profit, date):
    print(f"[BUY]    {date} - {symbol} buy: {last}. Loss: {loss} - Profit: {profit}")

def log_loss(symbol, loss, balance, date):
    print(f"[SELL]   {date} - {symbol} stop_loss:   {loss}     portfolio: {balance['portfolio']} precent_loss: {balance['percent']}")

def log_profit(symbol, profit, balance, date):
    print(f"[SELL]   {date} - {symbol} take_profit: {profit}.  portfolio: {balance['portfolio']} precent_loss: {balance['percent']}")

def log_compute_sell_orders(symbol, price, loss, profit, date):
    print(f"[UPDATE] {date} - {symbol} price: {price} - stop_loss: {loss} - take_profit: {profit}")

def log_time_until_market_close(date, clock):
    print(f"[MARKET] {date} - {clock} seconds left until market closes")

def log_time_until_market_open(date, clock):
    print(f"[MARKET] {date} - {clock} seconds left until market opens")