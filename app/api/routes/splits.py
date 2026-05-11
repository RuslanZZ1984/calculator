from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.split import SplitCreate, SplitRead
from app.services.split import create_split_service

router = APIRouter(prefix="/splits", tags=["Splits"])


@router.get("/")
async def get_splits():
    return {"message": "Splits endpoint"}


@router.post
async def create_split(
    data: SplitCreate,
    session: AsyncSession = Depends(get_session)
):
    return await create_split_service(session, data)