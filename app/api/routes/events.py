from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_session
from app.schemas.event import EventCreate, EventRead
from app.services.event import create_event_service, get_events_service, get_event_service, get_user_events_service
from app.crud.event import get_event_by_id
from app.depends.auth import get_current_user
from app.db.models import User, Event

router = APIRouter(prefix="/events", tags=["Events"])

# Все эндпоинты событий требуют авторизацию
@router.get("/", response_model=List[EventRead])
async def get_events(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get all events (только для авторизованных)"""
    return await get_events_service(session)

@router.post("/", response_model=EventRead)
async def create_event(
    data: EventCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create new event (только для авторизованных)"""
    # Автоматически устанавливаем owner_id = текущий пользователь
    data.owner_id = current_user.id
    return await create_event_service(session, data)

@router.get("/{event_id}", response_model=EventRead)
async def get_event(
    event_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get event by ID (только для авторизованных)"""
    event = await get_event_service(session, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@router.get("/user/{user_id}", response_model=List[EventRead])
async def get_user_events(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get user's events (только для авторизованных)"""
    # Проверяем, что пользователь запрашивает свои события или он админ
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own events"
        )
    return await get_user_events_service(session, user_id)
