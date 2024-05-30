from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String, DateTime, func
from app.database.database import db



class WalletSchema(BaseModel):
    wallet_id: int
    code: str = None
    average_price: float
    number_of_shares: int
    profit: float
    last_update_date: datetime


class WalletModel(db.base):
    ''' Wallet model'''
    __tablename__ = 'wallet'

    wallet_id = Column(Integer(), autoincrement=True, primary_key=True)
    category = Column(String(length=50))
    code = Column(String(length=100))
    average_price = Column(Float(10))
    number_of_shares = Column(Integer)
    profit = Column(Float(10)) #NOTE: Calculo de percentual de rendimento de uma ação: (Preço atual / Preço anterior) x 100 – 100
    last_update_date = Column(DateTime(), server_default=func.now(), onupdate=func.now()) 

    staticmethod
    async def save(wallet_new, db_session):
        db_session.add(wallet_new)
        await db_session.commit()
    