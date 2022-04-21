from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy import Column, Float, String, DateTime, Date, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import db


class StockSchema(BaseModel):
    code: str
    effective_date: date = None
    price: float = None
    name: str = None
    description: str = None
    last_update_date: datetime = None

    class Config:
        orm_mode = True


class StockModel(db.base):
    __tablename__ = 'stock'

    code = Column(String(length=100), primary_key=True)
    effective_date = Column(Date())
    price = Column(Float(10))
    name = Column(String(length=500))
    description = Column(String(length=500))
    last_update_date = Column(DateTime(), server_default=func.now())

    @staticmethod
    async def get_stock(code: str, db: AsyncSession) -> StockSchema:        
        stock_record = (await db.execute(
                            select(StockModel)
                            .where(func.upper(StockModel.code) == f'{code.upper()}.SA'))
                        ).scalars().one_or_none()
        return stock_record
    
    @staticmethod
    async def get_all_stocks(db: AsyncSession) -> list[StockSchema]:        
        stocks =  await db.execute(select(StockModel))    
        return stocks.scalars().all()
    
    @staticmethod
    async def get_stocks_codes(db: AsyncSession) -> list[StockSchema]:        
        stocks =  await db.execute(select(StockModel.code))  
        return stocks.scalars().all()
    
    @staticmethod
    async def save_stock(stock: StockSchema, db: AsyncSession):
        new_stock = StockModel(**stock)
        db.add(new_stock)
        await db.commit()
    
    @staticmethod
    async def merge_stock_price(stock, db: AsyncSession) -> StockSchema:                
        return await db.merge(stock)
    
    @staticmethod
    async def db_commit(db: AsyncSession) -> StockSchema:                
        return await db.commit()
