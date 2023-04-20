
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File

from app.database.database import get_session
from app.services.wallet_service import WalletService

wallet_router = APIRouter()



    
