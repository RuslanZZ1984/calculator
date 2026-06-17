from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Event

async def get_events(db: AsyncSession):
    result = await db.execute(select(Event))
    return result.scalars().all()

async def get_event_by_id(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalar_one_or_none()

async def get_events_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Event).where(Event.owner_id == user_id))
    return result.scalars().all()

async def delete_event(db: AsyncSession, event_id: int):
    await db.execute(delete(Event).where(Event.id == event_id))
    await db.commit()

async def create_event(db: AsyncSession, event_data):
    event = Event(
        title=event_data.title,
        owner_id=event_data.owner_id
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

async def update_event(db: AsyncSession, event_id: int, event_data):
    event = await get_event_by_id(db, event_id)
    if event:
        event.title = event_data.title
        await db.commit()
        await db.refresh(event)
    return event
