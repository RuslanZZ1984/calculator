from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.balance import calculate_event_balances_service
from app.services.settlement_service import calculate_settlements

router = APIRouter(prefix="/settlements", tags=["Settlements"])


router.get("/{event_id}")
async def get_settlements(
    event_id: int,
    session: AsyncSession = Depends(get_session),
):
    balances = await calculate_event_balances_service(session, event_id)
    settlements = calculate_settlements(balances)
    return settlements