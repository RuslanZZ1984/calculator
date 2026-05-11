from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.settlement_service import calculate_settlements
from app.schemas.settlement import SettlementResponse, SettlementItem

router = APIRouter(prefix="/settlements", tags=["Settlements"])

@router.get("/settlements/{event_id}", response_model=SettlementResponse)
async def get_settlements(
    event_id: int,
    session: AsyncSession = Depends(get_session),
):
    settlements = await calculate_settlements(session, event_id)

    result = [
        SettlementItem(
            from_user=s["from"],
            to_user=s["to"],
            amount=s["amount"],
        )
        for s in settlements
    ]

    return SettlementResponse(
        event_id=event_id,
        settlements=result
    )