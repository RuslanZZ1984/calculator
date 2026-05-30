from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.member import MemberCreate, MemberRead
from app.services.member import create_member_service
from app.crud.member import get_event_members


router = APIRouter(prefix="/members", tags=["Members"])

@router.get("/")
async def get_members():
    return {"message": "Members endpoint"}


@router.post("/", response_model=MemberRead)
async def create_member(
    data: MemberCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_member_service(session, data)

@router.get("/event/{event_id}", response_model=list[MemberRead])
async def get_event_members(
    event_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await get_event_members(session, event_id)