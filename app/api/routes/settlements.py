from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

from app.schemas.settlement import (
    SettlementResponse,
    SettlementItem
)

from app.services.balance import (
    calculate_event_balances_service
)

from app.services.settlement_service import (
    calculate_settlements
)

router = APIRouter(
    prefix="/settlements",
    tags=["Settlements"]
)


@router.get("/{event_id}", response_model=SettlementResponse)
async def get_settlements(
    event_id: int,
    session: AsyncSession = Depends(get_session),
):

    # 1. Получаем balances
    balances = await calculate_event_balances_service(
        session,
        event_id
    )

    # 2. Считаем settlements
    settlements = calculate_settlements(balances)

    # 3. Формируем response schema
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