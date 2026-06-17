from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import create_user, get_user_by_username
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from fastapi import HTTPException, status

async def create_user_service(db: AsyncSession, user_data: UserCreate):
    # Проверяем существование пользователя по email или username
    from sqlalchemy import select
    from app.db.models import User
    
    result = await db.execute(
        select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    return await create_user(db, user_data.email, user_data.username, hashed_password)
