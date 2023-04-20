from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, func, Sequence
from app.database.model.stock import StockModel
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

    wallet_id = Column(Integer(), Sequence('wallet_id_seq'), primary_key=True)
    category = Column(String(length=50))
    code = Column(String(length=100), ForeignKey(StockModel.code), primary_key=True)
    average_price = Column(Float(10))
    number_of_shares = Column(Integer)
    profit = Column(Float(10)) #NOTE: Calculo de percentual de rendimento de uma ação: (Preço atual / Preço anterior) x 100 – 100
    last_update_date = Column(DateTime(), server_default=func.now(), onupdate=func.now()) 