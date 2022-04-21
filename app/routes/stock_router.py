from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_session
from app.database.model.stock import StockSchema
from app.services.stock_service import StockService

stock_router = APIRouter()


@stock_router.get("/", response_model=list[StockSchema], tags=["Stock"])
async def get_all_stocks(db: AsyncSession = Depends(get_session)) -> list[StockSchema]:
    """ It returns a list of stocks

    Args:
        db (AsyncSession): database session 

    Returns:
        List[StockSchema]: list of stock schema
    """
    return await StockService.get_all_stocks(db)


@stock_router.post("/refresh",response_model=list[StockSchema], tags=["Stock"])
async def update_all_stock_prices(db: AsyncSession = Depends(get_session)) -> list[StockSchema]:
    """It updates and returns all stocks information 

    Args:
        code (str): stock code
        db (AsyncSession): databse session

    Returns:
        StockSchema: stock schema
    """
    return await StockService.update_all_stocks_price(db)


@stock_router.get("/{code}", response_model=StockSchema, tags=["Stock"])
async def get_stock(code: str, db: AsyncSession = Depends(get_session)) -> StockSchema:
    """It returns the stock information for a given stock code

    Args:
        code (str): stock code
        db (AsyncSession): database session

    Raises:
        HTTPException: raises this exception if given stock code is not found

    Returns:
        StockSchema: stock schema
    """
    stock = await StockService.get_stock(code, db)
    if not stock:
            raise HTTPException(status_code=404, detail='Stock not found')
    return stock


@stock_router.get("/{code}/refresh",response_model=StockSchema, tags=["Stock"])
async def get_updated_stock_price(code: str, db: AsyncSession = Depends(get_session)) -> StockSchema:
    """It returns the updated stock information for a given stock code

    Args:
        code (str): stock code
        db (AsyncSession): databse session

    Returns:
        StockSchema: stock schema
    """
    return await StockService.get_latest_stock_price(code, db)



