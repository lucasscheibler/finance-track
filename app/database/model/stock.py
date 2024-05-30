from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy import Column, Float, String, DateTime, Date, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import db


class StockSchema(BaseModel):
    '''Stock schema'''
    code: str
    effective_date: date = None
    price: float = None
    name: str = None
    description: str = None
    last_update_date: datetime = None

    class Config:
        from_attributes = True


class StockModel(db.base):
    '''Stock model'''
    __tablename__ = 'stock'

    code = Column(String(length=100), primary_key=True)
    effective_date = Column(Date())
    price = Column(Float(10))
    name = Column(String(length=500))
    description = Column(String(length=500))
    last_update_date = Column(DateTime(), server_default=func.now())

    @staticmethod
    async def get_stock(code: str, db_session: AsyncSession) -> StockSchema:
        """It gets the Stock info for a given Stock code

        Args:
            code (str): Stock code
            db (AsyncSession): database async session

        Returns:
            StockSchema: stock schema
        """
        stock_record = (
                        await db_session.execute(
                            select(StockModel)
                            .where(func.upper(StockModel.code) == f'{code.upper()}.SA'))
                        ).scalars().one_or_none()
        return stock_record
    
    @staticmethod
    async def get_all_stocks(db_session: AsyncSession) -> list[StockSchema]:
        """It returns all Stocks from database

        Args:
            db (AsyncSession): database async session

        Returns:
            list[StockSchema]: _description_
        """      
        stocks =  await db_session.execute(select(StockModel))    
        return stocks.scalars().all()
    
    @staticmethod
    async def get_stocks_codes(db_session: AsyncSession) -> list[StockSchema]:
        """It returns all Stock codes from database

        Args:
            db (AsyncSession): database async session

        Returns:
            list[StockSchema]: _description_
        """
        stocks =  await db_session.execute(select(StockModel.code))  
        return stocks.scalars().all()
    
    @staticmethod
    async def save_stock(stock: StockSchema, db_session: AsyncSession):
        """It saves a Stock into database

        Args:
            stock (StockSchema): Stock schema
            db (AsyncSession): database async session
        """
        new_stock = StockModel(**stock)
        db_session.add(new_stock)
        await db_session.commit()
    
    @staticmethod
    async def merge_stock_price(stock, db_session: AsyncSession) -> StockSchema:
        """It inserts/updates stock model into database

        Args:
            stock (model): Stock model
            db (AsyncSession): database async session

        Returns:
            StockSchema: Stock schema
        """
        return await db_session.merge(stock)
    
    @staticmethod
    async def db_commit(db_session: AsyncSession) -> StockSchema:
        """It commits the database transaction and returns

        Args:
            db (AsyncSession): database async session object

        Returns:
            StockSchema: Stock schema
        """
        return await db_session.commit()
