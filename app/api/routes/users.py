from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.user import UserCreate, UserRead
from app.services.user import create_user_service
from app.crud.user import get_all_users

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")  # тестовый
async def get_users():
    return {"message": "Users endpoint"}


@router.post("/", response_model=UserRead)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_user_service(session, data)


@router.get("/", response_model=list[UserRead])
async def get_users(
    session: AsyncSession = Depends(get_session),
):
    return await get_all_users(session)
