from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user as user_crud
from app.schemas.user import UserCreate


async def create_user_service(session: AsyncSession, data: UserCreate):
    return await user_crud.create_user(session, data)

async def get_user_service(session: AsyncSession, user_id: int):
    return await user_crud.get_user_by_id(session, user_id)