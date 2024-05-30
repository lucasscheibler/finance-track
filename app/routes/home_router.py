from fastapi import APIRouter

home_router = APIRouter()
 
    
@home_router.get("/")
async def root() -> dict:
    """Home route

    Returns:
        dict: A dictionary with Home message
    """
    return {"message": "Finance-Track home"}