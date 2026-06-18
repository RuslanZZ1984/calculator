from fastapi import APIRouter, Depends, Response, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.db.session import get_db
from app.db.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

class SignInRequest(BaseModel):
    email: str
    password: str

def set_token_cookies(response: Response, access_token: str, refresh_token: str = None):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 60
    )
    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )

@router.post("/sign-in")
async def sign_in(
    response: Response,
    login_data: SignInRequest,
    db: AsyncSession = Depends(get_db),
):
    # Ищем по email
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
        )
    
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    set_token_cookies(response, access_token, refresh_token)
    
    return {"ok": True, "result": True}

@router.post("/sign-in/refresh")
async def refresh_tokens(
    response: Response,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    
    from app.core.security import decode_access_token
    
    payload = decode_access_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    set_token_cookies(response, access_token, refresh_token)
    
    return {"ok": True, "result": True}

@router.post("/sign-in/googleAuth")
async def google_auth():
    return {"ok": True, "result": True}

@router.delete("/sign-out")
async def sign_out(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"ok": True, "result": True}
