from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_session
from app.schemas.member import MemberCreate, MemberRead
from app.services.member import create_member_service, get_members_service, get_event_members_service
from app.depends.auth import get_current_user
from app.db.models import User

router = APIRouter(prefix="/members", tags=["Members"])

@router.get("/", response_model=List[MemberRead])
async def get_members(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_members_service(session)

@router.post("/", response_model=MemberRead)
async def create_member(
    data: MemberCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_member_service(session, data)

@router.get("/event/{event_id}", response_model=List[MemberRead])
async def get_event_members(
    event_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_event_members_service(session, event_id)
