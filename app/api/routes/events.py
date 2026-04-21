from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.event import EventCreate, EventRead
from app.services.event import create_event_service

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/") # Тестовый
async def get_events():
    return {"message": "Events endpoint"}


@router.post("/", response_model=EventRead)
async def create_event(
    data: EventCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_event_service(session, data)
