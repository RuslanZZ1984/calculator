from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import member as member_crud
from app.crud.user import get_user_by_id
from app.crud.event import get_event

from app.schemas.member import MemberCreate


async def create_member_service(
        session: AsyncSession,
        data: MemberCreate
):
    # Проверяем пользователя
    user = await get_user_by_id(session, data.user_id)
    if not user:
        raise ValueError("Пользователь не найден")
    
    # Проверяем событие
    event = await get_event(session, data.event_id)
    if not event:
        raise ValueError("Событие не найдено")
    
    return await member_crud.create_member(session, data)


async def get_event_members_service(
        session: AsyncSession,
        event_id: int
):
    return await member_crud.get_event_members(
        session, event_id
    )


async def delete_member_service(
        session: AsyncSession,
        member_id: int
):
    return await member_crud.delete_member(
        session, member_id
    )