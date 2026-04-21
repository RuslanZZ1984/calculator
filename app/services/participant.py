from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import participant as participant_crud
from app.crud.user import get_user_by_id
from app.crud.event import get_event

from app.schemas.participant import ParticipantCreate


async def create_participant_service(
        session: AsyncSession,
        data: ParticipantCreate
):
    # Проверяем пользователя
    user = await get_user_by_id(session, data.user_id)
    if not user:
        raise ValueError("Пользователь не найден")
    
    # Проверяем событие
    event = await get_event(session, data.event_id)
    if not event:
        raise ValueError("Событие не найдено")
    
    return await participant_crud.create_participant(session, data)


async def get_event_participants_service(
        session: AsyncSession,
        event_id: int
):
    return await participant_crud.get_event_participants(
        session, event_id
    )


async def delete_participant_service(
        session: AsyncSession,
        participant_id: int
):
    return await participant_crud.delete_participant(
        session, participant_id
    )