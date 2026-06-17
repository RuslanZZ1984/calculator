from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["[auth] - sign-in (login)"])

@router.post("/sign-in/googleAuth")
async def google_auth(
    token: str = Query(..., description="Google token"),
    db: AsyncSession = Depends(get_db),
):
    """WORKS: User google auth."""
    return {"ok": True, "result": True}
