from binance.spot import Spot
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from .models import Trade

async def get_data(binance_client: Spot, symbol: str, interval: str, limit: int) -> pd.DataFrame:
    df = pd.DataFrame(binance_client.klines(symbol=symbol, interval=interval, limit=limit))
    df = df.iloc[:, :9]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_av', 'Trades']

    # drop unnecessary columns
    df = df.drop(['Close_time', 'Quote_av', 'Trades'], axis=1)

    # convert to datetime
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')

    # set index
    df = df.set_index('Time')
    # convert to float
    df = df.astype(float)

    return df

async def get_trades(session: AsyncSession, history: str, qty: int) -> list:
    history_calc = None
    timeframe_calc = None
    
    buy_orders = []
    sell_orders = []
    
    #get utc time
    time = datetime.datetime.utcnow()
    # minus 5 hours to get new york time
    time = time - datetime.timedelta(hours=5)
    # remove microseconds
    time_now = time.replace(microsecond=0)
    
    if history.endswith("m"):
        history_calc = int(history[:-1])
        timeframe_calc = "minutes"
    elif history.endswith("h"):
        history_calc = int(history[:-1])
        timeframe_calc = "hours"
    elif history.endswith("d"):
        history_calc = int(history[:-1])
        timeframe_calc = "days"
    elif history.endswith("w"):
        timeframe_calc = "weeks"
        history_calc = int(history[:-1])
    
    
    # print(history_calc)
    # print(timeframe_calc)
    
    # print(time_now - datetime.timedelta(**{timeframe_calc: history_calc}))
    
    
    sql = select(Trade).where(Trade.timestamp >= time_now - datetime.timedelta(**{timeframe_calc: history_calc})).order_by(Trade.qty.desc()).limit(qty)
    result = await session.execute(sql)
    trades = result.scalars().all()
    
    for trade in trades:
        
        # if side is buy append to buy_orders, else append to sell_orders
        if trade.side == "BUY":
            buy_orders.append(trade)
        elif trade.side == "SELL":
            sell_orders.append(trade)
        else:
            pass
    
    # print(f"buy_orders: {len(buy_orders)}")
    # print(f"sell_orders: {len(sell_orders)}")
    
    return buy_orders, sell_orders

async def calculate_time_periods(timeframe, history) -> int:
  timeframe_calc = None
  history_calc = None
  
  if timeframe.endswith("m"):
      timeframe_calc = int(timeframe[:-1])
  elif timeframe.endswith("h"):
      timeframe_calc = int(timeframe[:-1]) * 60
  elif timeframe.endswith("d"):
      timeframe_calc = int(timeframe[:-1]) * 60 * 24
  elif timeframe.endswith("w"):
      timeframe_calc = int(timeframe[:-1]) * 60 * 24 * 7
  
  if history.endswith("m"):
      history_calc = int(history[:-1])
  elif history.endswith("h"):
      history_calc = int(history[:-1]) * 60
  elif history.endswith("d"):
      history_calc = int(history[:-1]) * 60 * 24
  elif history.endswith("w"):
      history_calc = int(history[:-1]) * 60 * 24 * 7
  
  # Calculate the number of time periods in the interval
  num_periods = history_calc / timeframe_calc

  return int(num_periods)