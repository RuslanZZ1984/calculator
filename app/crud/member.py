from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import EventMember

async def get_members(db: AsyncSession):
    result = await db.execute(select(EventMember))
    return result.scalars().all()

async def get_member_by_id(db: AsyncSession, member_id: int):
    result = await db.execute(select(EventMember).where(EventMember.id == member_id))
    return result.scalar_one_or_none()

async def get_members_by_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(EventMember).where(EventMember.event_id == event_id))
    return result.scalars().all()

async def get_event_members(db: AsyncSession, event_id: int):
    return await get_members_by_event(db, event_id)

async def delete_members_by_event(db: AsyncSession, event_id: int):
    await db.execute(delete(EventMember).where(EventMember.event_id == event_id))
    await db.commit()

async def create_member(db: AsyncSession, member_data):
    member = EventMember(**member_data.model_dump())
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member
