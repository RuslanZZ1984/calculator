from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from app.core.security import get_password_hash
from app.db.session import get_db
from app.db.models import User
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["[auth] - sign-up (register)"])

class UserSignUp(BaseModel):
    email: EmailStr
    username: str
    password: str

@router.post("/sign-up", response_model=dict)
async def sign_up(
    user_data: UserSignUp,
    db: AsyncSession = Depends(get_db),
):
    """
    WORKS: User registration.
    """
    # Проверяем email
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Проверяем username
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Создаём пользователя
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        login=user_data.username,
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {
        "ok": True,
        "result": True,
        "message": "User registered successfully"
    }
