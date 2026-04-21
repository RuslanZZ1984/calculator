from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User


async def create_user(session: AsyncSession, data):
    user = User(**data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()