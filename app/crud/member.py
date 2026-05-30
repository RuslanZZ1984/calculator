from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import EventMember
from app.schemas.member import MemberCreate

# create
async def create_member(
    session: AsyncSession,
    data: MemberCreate
) -> EventMember:
    member = EventMember(**data.model_dump())
    session.add(member)
    await session.commit()
    await session.refresh(member)
    return member

# read one
async def get_member(
    session: AsyncSession,
    member_id: int
):
    result = await session.execute(
        select(EventMember).where(
            EventMember.id == member_id
        )
    )
    return result.scalar_one_or_none()

# read many (by event)
async def get_event_members(
    session: AsyncSession,
    event_id: int
):
    result = await session.execute(
        select(EventMember).where(
            EventMember.event_id == event_id
        )
    )
    return result.scalars().all()

# delete
async def delete_member(
        session: AsyncSession,
        member_id: int
) -> bool:
    member = await get_member(session, member_id)

    if not member:
        return False
    
    await session.delete(member)
    await session.commit()
    return True