from datetime import datetime, date

from sqlalchemy.ext.asyncio import AsyncSession
from yfinance import Ticker

from app.services.stock_market_service import StockMarketService
from app.database.model.stock import StockSchema
from app.database.model.stock import StockModel


class StockService():

    @staticmethod
    async def get_stock(stock_code: str, db: AsyncSession) -> StockSchema:
        return await StockModel.get_stock(stock_code, db)

    @staticmethod
    async def get_all_stocks(db: AsyncSession) -> list[StockSchema]:
        return await StockModel.get_all_stocks(db)

    @staticmethod
    async def update_stock_price(stock: StockModel, ticker: Ticker) -> StockModel:
        last_quote = StockMarketService.get_latest_stock_price(ticker)
        return StockModel(code=stock.code, price=last_quote, last_update_date=datetime.now())

    @staticmethod
    def get_current_stock_info(stock_code: str, ticker: Ticker) -> StockModel:
        current_price = ticker.info.get('regularMarketPrice')
        stock_name = ticker.info.get('longName')
        return StockModel(code=f'{stock_code.upper()}.SA'
                          ,price=current_price
                          ,name=stock_name
                          ,description=stock_name
                          ,effective_date=date.today()
                          ,last_update_date=datetime.now())

    @staticmethod
    async def get_latest_stock_price(stock_code: str, db: AsyncSession) -> StockSchema:
        ticker = StockMarketService.get_ticker(stock_code)
        stock = await StockModel.get_stock(stock_code, db)
        if stock:
            stock = await StockService.update_stock_price(stock, ticker)
        else:
            stock = StockService.get_current_stock_info(stock_code, ticker)            
            
        stock = await StockModel.merge_stock_price(stock, db)
        await StockModel.db_commit(db)
        return stock        

    @staticmethod
    async def update_all_stocks_price(db: AsyncSession) -> list[StockSchema]:
        tickers_list = await StockModel.get_stocks_codes(db)
        ticker_data = StockMarketService.download_tickers(tickers_list)
        updated_stocks = []        
        for ticker in tickers_list:
            stock = StockMarketService.set_latest_price(ticker_data, ticker)
            stock = await StockModel.merge_stock_price(stock, db)
            updated_stocks.append(stock)        

        await StockModel.db_commit(db)
        return updated_stocks

    
