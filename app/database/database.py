from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncIterator


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):

    def __init__(self):
        self.engine = None
        self.session_local = None
        self.base = declarative_base()

    def connect_async_database(self):
        if self.engine is not None:
            self.engine.dispose()
        
        self.engine = create_async_engine(
            'sqlite+aiosqlite:///fintrack_localdb.db', echo=False, poolclass = StaticPool
        )
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)

    def connect_database(self):
        if self.engine is not None:
            self.engine.dispose()
        
        self.engine = create_engine(
            'sqlite:///fintrack_localdb.db', echo=False, poolclass = StaticPool
        )
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_metadata(self):
        '''
            Add model's MetaData object here to be detected by alembic
        '''
        from app.database.model.stock import StockModel
        from app.database.model.wallet import WalletModel
        from app.database.model.transaction import TransactionModel

        return self.base.metadata

    def upgrade_db(self):        
        from alembic.config import Config
        from alembic import command

        self.connect_database()
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.attributes['configure_logger'] = False
        alembic_cfg.attributes['connection'] = self.engine
        command.upgrade(alembic_cfg, "head")

    async def run_async_upgrade(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.upgrade_db)


db = Database()
db.base = declarative_base()
db.get_metadata()


async def get_database_session():
    try:
        yield db.session_local
    finally:
        db.session_local.close()


async def get_session() -> AsyncIterator[AsyncSession]:
    async_session = sessionmaker(
                                db.engine, 
                                expire_on_commit=False, 
                                class_=AsyncSession
                    )
    async with async_session() as session:
        yield session