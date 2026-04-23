from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.participant import get_event_participants
from app.crud.expense import get_expenses_by_event
from app.crud.split import get_splits_by_expense


async def calculate_event_balances_service(
    session: AsyncSession,
    event_id: int
):
    participants = await get_event_participants(session, event_id)

    if not participants:
        raise ValueError("У события нет участников")
    
    balances = {
        p.id: {
            "name": p.display_name,
            "paid": 0.0,
            "owed": 0.0,
            "balance": 0.0
        }
        for p in participants
    }

    expenses = await get_expenses_by_event(session, event_id)

    # вначале считаем всех
    for expense in expenses:
        # кто заплатил
        balances[expense.payer_id]["paid"] += expense.amount

        # Кому распределили
        splits = await get_splits_by_expense(session, expense.id)

        for split in splits:
            balances[split.participant_id]["owed"] += split.amount
        
    # Итоговый баланс:
    for participant_id in balances:
        item = balances[participant_id]
        item["balance"] = round(item["paid"] - item["owed"], 2)
        
    return balances        
