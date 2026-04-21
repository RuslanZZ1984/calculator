from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.database_url_async, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# get_session — это связка FastAPI ↔ база данных
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
