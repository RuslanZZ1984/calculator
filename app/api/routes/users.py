from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.user import UserCreate, UserResponse
from app.services.user import create_user_service
from app.crud.user import get_all_users
from app.depends.auth import get_current_user
from app.db.models import User

router = APIRouter(prefix="/users", tags=["Users"])

# Защищённые эндпоинты - требуют авторизацию
@router.post("/", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),  # Добавили защиту
):
    # Только авторизованные пользователи могут создавать новых пользователей
    return await create_user_service(session, data)

@router.get("/", response_model=list[UserResponse])
async def get_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),  # Добавили защиту
):
    # Только авторизованные пользователи могут видеть список пользователей
    return await get_all_users(session)
