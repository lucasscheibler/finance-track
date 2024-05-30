from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.database.database import get_session
from app.services.wallet_service import WalletService

wallet_router = APIRouter()


@wallet_router.post('/', tags=["Wallet"])
async def refresh_wallet(db_session: AsyncSession = Depends(get_session)):
    return await WalletService.refresh_wallet(db_session)
    

    
