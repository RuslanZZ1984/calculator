from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.db.models import User

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    # Получаем токен из cookie
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise credentials_exception
    
    payload = decode_access_token(access_token)
    if payload is None:
        raise credentials_exception
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user

Authorization = get_current_user
AuthorizationRefresh = get_current_user  # Для refresh будет отдельная логика
