from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.balance import calculate_event_balances_service
from app.schemas.balance import BalanceResponse, BalanceItem

router = APIRouter(prefix="/finance", tags=["Finance"])


@router.get("/balances/{event_id}", response_model=BalanceResponse)
async def get_balances(
    event_id: int,
    session: AsyncSession = Depends(get_session),
):
    balances = await calculate_event_balances_service(session, event_id)

    result = [
        BalanceItem(
            participant_id=pid,
            name=data["name"],
            paid=data["paid"],
            owed=data["owed"],
            balance=data["balance"],
        )
        for pid, data in balances.items()
    ]

    return BalanceResponse(
        event_id=event_id,
        balances=result
    )