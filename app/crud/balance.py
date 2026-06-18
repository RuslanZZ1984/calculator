from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Expense, ExpenseSplit, EventMember

async def get_balances_by_event(db: AsyncSession, event_id: int):
    # Получаем всех участников события
    members_result = await db.execute(
        select(EventMember).where(EventMember.event_id == event_id)
    )
    members = members_result.scalars().all()
    
    balances = []
    for member in members:
        # Сумма расходов, которые заплатил участник
        paid_result = await db.execute(
            select(func.sum(Expense.amount)).where(
                Expense.event_id == event_id,
                Expense.payer_id == member.id
            )
        )
        paid = paid_result.scalar() or 0.0
        
        # Сумма расходов, которые должен участник (его доля)
        owed_result = await db.execute(
            select(func.sum(ExpenseSplit.amount)).where(
                ExpenseSplit.member_id == member.id
            )
        )
        owed = owed_result.scalar() or 0.0
        
        balances.append({
            "member_id": member.id,
            "name": member.display_name,
            "paid": float(paid),
            "owed": float(owed),
            "balance": float(paid - owed)
        })
    
    return balances
