from datetime import datetime
from yfinance import Ticker
import yfinance as yf

from app.database.model.stock import StockModel, StockSchema


class StockMarketService():

    @staticmethod
    def get_ticker(stock_code: str) -> Ticker:
        return yf.Ticker(f'{stock_code}.SA')

    @staticmethod
    def get_latest_stock_price(ticker: Ticker):
        data = ticker.history()
        return data.tail(1)['Close'].iloc[0]

    @staticmethod
    def set_latest_price(ticker_data, ticker: str):
        last_quote = ticker_data.tail(1)[ticker].iloc[0]
        stock = StockModel(code=ticker, price=last_quote, last_update_date=datetime.now())
        return stock