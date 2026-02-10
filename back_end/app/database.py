 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.config import settings

# Synchronous engine for Alembic migrations
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30
)

# Asynchronous engine for FastAPI
async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=True if settings.APP_ENV == "development" else False,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

def get_db():
    """Dependency for synchronous database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """Dependency for asynchronous database sessions"""
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()