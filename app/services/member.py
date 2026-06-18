from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import member as member_crud
from app.schemas.member import MemberCreate

async def create_member_service(db: AsyncSession, member_data: MemberCreate):
    return await member_crud.create_member(db, member_data)

async def get_members_service(db: AsyncSession):
    return await member_crud.get_members(db)

async def get_event_members_service(db: AsyncSession, event_id: int):
    return await member_crud.get_members_by_event(db, event_id)
