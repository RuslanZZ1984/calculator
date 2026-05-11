from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.participant import ParticipantCreate, ParticipanRead
from app.services.participant import create_participant_service
from app.crud.participant import get_event_participants


router = APIRouter(prefix="/participants", tags=["Participants"])

@router.get("/")
async def get_participants():
    return {"message": "Participants endpoint"}


@router.post("/", response_model=ParticipanRead)
async def create_participant(
    data: ParticipantCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_participant_service(session, data)

@router.get("/event/{event_id}", response_model=list[ParticipanRead])
async def get_event_participants(
    event_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await get_event_participants(session, event_id)