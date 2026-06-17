from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import event as event_crud
from app.schemas.event import EventCreate

async def create_event_service(db: AsyncSession, event_data: EventCreate):
    return await event_crud.create_event(db, event_data)

async def get_events_service(db: AsyncSession):
    return await event_crud.get_events(db)

async def get_event_service(db: AsyncSession, event_id: int):
    return await event_crud.get_event_by_id(db, event_id)

async def get_user_events_service(db: AsyncSession, user_id: int):
    return await event_crud.get_events_by_user(db, user_id)

async def update_event_service(db: AsyncSession, event_id: int, event_data: EventCreate):
    return await event_crud.update_event(db, event_id, event_data)

async def delete_event_service(db: AsyncSession, event_id: int):
    return await event_crud.delete_event(db, event_id)
