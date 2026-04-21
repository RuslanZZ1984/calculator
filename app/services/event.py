from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import event as event_crud
from app.schemas.event import EventCreate

async def create_event_service(session: AsyncSession, data: EventCreate):
    # Добавим потом логику, например, существует ли User
    return await event_crud.create_event(session, data)

async def get_user_events_service(session: AsyncSession, owner_id: int):
    return await event_crud.get_events_by_user(session, owner_id)
