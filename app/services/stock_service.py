from typing import List
from datetime import date
from yfinance import Ticker
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from concurrent.futures import ThreadPoolExecutor
from time import monotonic

import yfinance as yf

from app.database.model.stock import StockSchema
from app.database.model.stock import StockModel


class StockService():

    @staticmethod
    def get_ticker(stock_code: str) -> Ticker:
        return yf.Ticker(f'{stock_code}.SA')

    @staticmethod
    async def get_stock(code: str, db: AsyncSession) -> StockSchema:        
        stock_record = (await db.execute(
                            select(StockModel)
                            .where(func.upper(StockModel.code) == code.upper()))
                        ).scalars().one_or_none()
        return stock_record

    @staticmethod
    async def get_all_stocks(db: AsyncSession) -> List[StockSchema]:        
        stocks =  await db.execute(select(StockModel))    
        return stocks.scalars().all()

    @staticmethod
    async def save_stock(stock: StockSchema, db: AsyncSession):
        new_stock = StockModel(code='VALE3', name='test')
        db.add(new_stock)
        await db.commit()

    @staticmethod
    def update_stock_price(stock: StockModel, ticker: Ticker) -> StockModel:
        data = ticker.history()
        last_quote = (data.tail(1)['Close'].iloc[0])
        return StockModel(code=stock.code, price=last_quote)

    @staticmethod
    def get_current_stock_info(stock_code: str, ticker: Ticker) -> StockModel:
        current_price = ticker.info.get('regularMarketPrice')
        stock_name = ticker.info.get('longName')
        # data = ticker.history()
        # current_price = (data.tail(1)['Close'].iloc[0])
        return StockModel(code=stock_code.upper()
                          ,price=current_price
                          ,name=stock_name
                          ,description=stock_name
                          ,effective_date=date.today())

    @staticmethod
    async def get_latest_stock_price(stock_code: str, db: AsyncSession) -> StockSchema:
        ticker = StockService.get_ticker(stock_code)
        stock = await StockService.get_stock(stock_code, db)
        if stock:
            stock = StockService.update_stock_price(stock, ticker)
        else:
            stock = StockService.get_current_stock_info(stock_code, ticker)            
            
        return await StockService.merge_stock_price(stock, db)
        
    @staticmethod
    async def merge_stock_price(stock: StockModel, db: AsyncSession)-> StockSchema:                
        stock = await db.merge(stock)
        await db.commit()
        return stock



        # https://pypi.org/project/yfinance/

        # data = ticker.history()
        # last_quote = (data.tail(1)['Close'].iloc[0])

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')

        # yf.download(f'{stock_code}.SA',period="1h")

        # data1 = yf.download(f'{stock_code}.SA','2022-02-01','2022-02-02')
        # print(data1)

        # tickers_list = ['ITSA4.SA', 'VALE3.SA', 'ENBR3.SA', 'TAEE11.SA']
        # data2 = yf.download(tickers_list,'2022-01-01')['Adj Close']
        # print(data2)
        
