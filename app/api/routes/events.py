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


@router.get("/{event_id}", response_model=EventRead)
async def get_event(
    event_id: int,
    session: AsyncSession = Depends(get_session),
):
    from app.crud.event import get_event_by_id
    return await get_event_by_id(session, event_id)


@router.get("/user/{user_id}", response_model=list[EventRead])
async def get_user_events(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    from app.crud.event import get_events_by_user
    return await get_events_by_user(session, user_id)