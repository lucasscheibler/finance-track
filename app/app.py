from fastapi import FastAPI
from app.database.database import Database


def register_routes(app):
    from app.routes.home_router import home_router
    from app.routes.stock_router import stock_router

    app.include_router(home_router)
    app.include_router(stock_router, prefix="/api/stock")    
    

def create_app():
    application = FastAPI(title="Finance-Track", version="0.0.2")
    db = Database()
    db.upgrade_db()
    db.connect_async_database()
    register_routes(application)
    return application


    