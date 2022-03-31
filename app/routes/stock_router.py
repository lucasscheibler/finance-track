from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.database.database import get_session
from app.database.model.stock import StockSchema
from app.services.stock_service import StockService

stock_router = APIRouter()


@stock_router.get("/{code}", response_model=List[StockSchema])
async def get_stocks(code: str, db: AsyncSession = Depends(get_session)) -> List[StockSchema]:
    return await StockService.get_stocks(code, db)


@stock_router.get("/{code}/refresh")
async def get_update_stock_price(code: str, db: AsyncSession = Depends(get_session)):
    return await StockService.get_stock_price(code, db)


# @stock_router.get("/items/{item_id}")
# async def read_user_item(
#     item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
# ):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item


# @stock_router.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


# @item_router.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}