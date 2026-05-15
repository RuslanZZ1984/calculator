"""
Пересчёт ExpenseSplit для события.

Логика:
- удаляем старые splits
- заново распределяем расходы между текущими участниками события
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.expense import get_expenses_by_event
from app.crud.participant import get_event_participants

from app.crud.split import delete_splits_by_event

from app.schemas.split import SplitCreate

from app.services.split import create_split_service


async def rebuild_event_splits_service(
    session: AsyncSession,
    event_id: int
):
    # 1. Получаем участников
    participants = await get_event_participants(
        session,
        event_id
    )

    if not participants:
        raise ValueError("У события нет участников")

    # 2. Получаем расходы
    expenses = await get_expenses_by_event(
        session,
        event_id
    )

    # 3. Удаляем старые splits
    await delete_splits_by_event(
        session,
        event_id
    )

    # 4. Пересоздаём splits
    for expense in expenses:

        split_amount = round(
            expense.amount / len(participants),
            2
        )

        for participant in participants:

            split_data = SplitCreate(
                expense_id=expense.id,
                participant_id=participant.id,
                amount=split_amount
            )

            await create_split_service(
                session,
                split_data
            )