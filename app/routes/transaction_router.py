
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File

from app.database.database import get_session
from app.services.transaction_service import TransactionService

transaction_router = APIRouter()


@transaction_router.post("/", tags=["Transaction"])
async def import_transactions(file: UploadFile = File(...), db_session: AsyncSession = Depends(get_session)):
    """It imports the transaction from excel file (B3) into database

    Args:
        file (UploadFile, optional): Excel file provided by B3. Defaults to File(...).
        db_session (AsyncSession, optional): database session. Defaults to Depends(get_session).

    Returns:
        _type_: _description_
    """    
    return await TransactionService.import_transactions(file, db_session)
    
