import logging

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_URL
from .models import *


logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler = logging.FileHandler('logs/db_log.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session