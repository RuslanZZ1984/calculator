from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.balance import calculate_event_balances_service

router = APIRouter(prefix="balances", tags=["Balances"])


@router.get("/{event_id}")
async def get_balances(
    event_id: int,
    session: AsyncSession = Depends(get_session),
):
    balances = await calculate_event_balances_service(session, event_id)
    return balances