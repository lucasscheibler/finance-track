from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, func, Sequence
from app.database.model.wallet import WalletModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import db


class TransactionSchema(BaseModel):
    ''' Transaction schema'''
    transaction_id: int
    wallet_id: int
    category: Optional[str]
    code: Optional[str]
    action: Optional[str]
    broker: Optional[str] 
    effective_date: Optional[date] 
    num_shares: Optional[int] 
    price: Optional[float] 
    total: Optional[float] 
    last_update_date: datetime 


class TransactionModel(db.base):
    ''' Transaction model'''
    __tablename__ = 'transaction'
    
    transaction_id = Column(Integer(), Sequence('transaction_id_seq'), primary_key=True)
    wallet_id = Column(Integer(), ForeignKey(WalletModel.wallet_id))
    category = Column(String(length=100))
    code = Column(String(length=100))
    action = Column(String(length=100))
    broker = Column(String(length=100))
    effective_date = Column(Date())
    num_shares = Column(Integer())
    price = Column(Float(10))
    total = Column(Float(10))
    last_update_date = Column(DateTime(), server_default=func.now())

    @staticmethod
    async def save(transaction, db_session: AsyncSession):
        """It saves the transaction into databasetime

        Args:
            transaction (TransactionModel)): transaction model
            db_session (AsyncSession): database session
        """        
        db_session.add(transaction)
        await db_session.commit()