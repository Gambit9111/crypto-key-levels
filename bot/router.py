from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
import mplfinance as mpf
import matplotlib.pyplot as plt
import os

from binance.spot import Spot

from sqlalchemy.ext.asyncio import AsyncSession

import asyncio

from .functions import get_data, calculate_time_periods, get_trades

router = Router(name="main-router")

symbol = "SOLUSDT"




@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    
    await message.answer("format: timeframe/history/trade_qty/  15min candles/ 1 day history / 3 highest qty trades")


@router.message()
async def echo(message: Message, session: AsyncSession) -> None:
    await message.answer("pulling data...")
    
    timeframe, history, qty = message.text.split("/")
    
    periods = await calculate_time_periods(timeframe, history)
    
    try:
        
        buy_orders, sell_orders = await get_trades(session, history, int(qty))
        
        # Assume that 'support' and 'resistance' are lists of y-values for the support and resistance lines
        support = []
        resistance = []
        
        # fill support and resistance lists
        for order in buy_orders:
            support.append(order.price)
        
        for order in sell_orders:
            resistance.append(order.price)
        
        binance_client = Spot()
        frame = await get_data(binance_client, symbol, timeframe, periods)
        
        # Define a list of color codes for support and resistance lines
        support_colors = ['green'] * len(support)
        resistance_colors = ['red'] * len(resistance)
        
        # Combine the support and resistance lists
        hlines_values = support + resistance
        
        # Combine the colors for support and resistance lines
        hlines_colors = support_colors + resistance_colors
        
        # Convert the lists to a dictionary
        hlines = dict(hlines=hlines_values, colors=hlines_colors, linestyle='-.')
        
        # Create a figure
        fig = plt.figure(figsize=(16,9))
        
        mpf.plot(frame, type='candle', style='yahoo', volume=False, savefig=f'{message.from_user.id}.png', figsize=(16,9), hlines=hlines, tight_layout=True, xrotation=0, datetime_format='%d-%m-%Y %H:%M:%S', ylabel='Price (USDT)', ylabel_lower='Volume (USDT)', title=f'{symbol} {timeframe} {history}')
        photo = FSInputFile(f'{message.from_user.id}.png')
        await message.answer_photo(photo=photo)
        os.unlink(f'{message.from_user.id}.png')
    
    except Exception as e:
        await message.answer(f"error: {e}")
        return