from typing import List
from datetime import date
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

import yfinance as yf

from app.database.model.stock import StockSchema
from app.database.model.stock import StockModel


class StockService():

    @staticmethod
    async def get_stocks(code: str, db: AsyncSession) -> List[StockSchema]:        
        stock_record = await db.execute(select(StockModel).where(StockModel.code == code))
        return stock_record.scalars().all()

    @staticmethod
    async def save_stock(stock: StockSchema, db: AsyncSession):
        new_stock = StockModel(code='VALE3', name='test')
        db.add(new_stock)
        await db.commit()

    @staticmethod
    async def get_latest_stock_price(stock_code: str) -> StockSchema:
        ticker_yahoo = yf.Ticker(f'{stock_code}.SA')
        data = ticker_yahoo.history()
        last_quote = (data.tail(1)['Close'].iloc[0])
        print(f'{stock_code}.SA',last_quote)
        stock = StockModel(code=stock_code, price=last_quote, effective_date=date.today())
        return stock
        
    @staticmethod
    async def get_stock_price(stock_code: str, db: AsyncSession)-> StockSchema:                
        stock = await StockService.get_latest_stock_price(stock_code)
        stock = await db.merge(stock)
        await db.commit()
        return stock

        # data1 = yf.download(f'{stock_code}.SA','2022-02-01','2022-02-02')
        # print(data1)

        # tickers_list = ['ITSA4.SA', 'VALE3.SA', 'ENBR3.SA', 'TAEE11.SA']
        # data2 = yf.download(tickers_list,'2022-01-01')['Adj Close']
        # print(data2)
        
