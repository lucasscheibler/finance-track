from app.database.database import db
from sqlalchemy import Column, Float, String, DateTime, Date
from datetime import datetime, date
from pydantic import BaseModel


class StockModel(db.base):
    __tablename__ = 'stock'

    code = Column(String(length=100), primary_key=True)
    effective_date = Column(Date())
    price = Column(Float(10))
    name = Column(String(length=500))
    description = Column(String(length=500))
    last_update_date = Column(DateTime(), default=datetime.utcnow())


class StockSchema(BaseModel):
    code: str
    effective_date: date = None
    price: float = None
    name: str = None
    description: str = None
    last_update_date: datetime = None

    class Config:
        orm_mode = True