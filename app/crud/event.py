from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.models import Event


async def create_event(session: AsyncSession, data):
    event = Event(**data.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def get_event(session: AsyncSession, event_id: int):
    result = await session.execute(
        select(Event).where(Event.id == event_id)
    )
    return result.scalar_one_or_none()


async def get_events_by_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Event).where(Event.owner_id == user_id)
    )
    return result.scalars().all()