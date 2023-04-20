from datetime import datetime
from time import sleep
from yfinance import Ticker

from fastapi.logger import logger
import yfinance as yf

from app.database.model.stock import StockModel


class StockMarketService():
    '''Stock Service class'''

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
    
    @staticmethod
    def download_tickers(tickers_list: list):
        retry = 0

        while retry <= 5:
            try:
                ticker_data = yf.download(tickers_list, period='1h')['Adj Close']
                if ticker_data.empty:
                    raise Exception('No data found.')
                return ticker_data

            except Exception as error:
                logger.error(f'Error when trying to fetch ticker data: {str(error)}')
                retry += 1
                logger.error(f'Retry: {str(retry)}...')
                sleep(3)
            