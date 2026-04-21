from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import EventParticipant
from app.schemas.participant import ParticipantCreate

# create
async def create_participant(
        session: AsyncSession,
        data: ParticipantCreate
) -> EventParticipant:
    participant = EventParticipant(**data.model_dump())
    session.add(participant)
    await session.commit()
    await session.refresh(participant)
    return participant

# read one
async def get_participant(
    session: AsyncSession,
    participant_id: int
):
    result = await session.execute(
        select(EventParticipant).where(
            EventParticipant.id == participant_id
        )
    )
    return result.scalar_one_or_none()

# read many (by event)
async def get_event_participants(
        session: AsyncSession,
        event_id: int
):
    result = await session.execute(
        select(EventParticipant).where(
            EventParticipant.event_id == event_id
        )
    )
    return result.scalars().all()

# delete
async def delete_participant(
        session: AsyncSession,
        participant_id: int
) -> bool:
    participant = await get_participant(session, participant_id)

    if not participant:
        return False
    
    await session.delete(participant)
    await session.commit()
    return True