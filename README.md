This repository contains a Python script leveraging aiogram and the Binance API (python-binance) to draw the largest trades on a chart as support and resistance levels.
Overview

The script includes functionalities to:

    Receive user input for timeframe, history, and quantity of trades.
    Retrieve historical trading data from Binance using the python-binance library.
    Calculate support and resistance lines based on retrieved trade orders.
    Generate a candlestick chart using mplfinance library.
    Display the chart to the user via Telegram using aiogram.

Usage

    Dependencies Installation:
    Ensure you have the required libraries installed. Use pip to install the necessary dependencies:

    bash

    pip install aiogram mplfinance python-binance SQLAlchemy

    Setup API Keys:
    To use the Binance API, you'll need API keys from Binance. Insert your API keys in the designated place within the code.

    Run the Script:
    Run the Python script and interact with it via a Telegram bot. Use the command /start to begin, and follow the format: timeframe/history/trade_qty.

    Interacting with the Bot:
        Send the bot a message in the format specified above (timeframe/history/trade_qty).
        The bot will fetch data from Binance, calculate support and resistance lines, and display a candlestick chart.

Important Notes

    Data Privacy: Ensure your API keys are kept secure and not shared publicly.
    Error Handling: The script includes basic error handling for exceptions. Modify it as per your requirement.


License

This project is licensed under the MIT License - see the LICENSE file for details.