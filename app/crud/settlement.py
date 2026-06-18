from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Expense, ExpenseSplit, EventMember

async def get_settlements_by_event(db: AsyncSession, event_id: int):
    # Получаем балансы
    members_result = await db.execute(
        select(EventMember).where(EventMember.event_id == event_id)
    )
    members = members_result.scalars().all()
    
    balances = []
    for member in members:
        paid_result = await db.execute(
            select(func.sum(Expense.amount)).where(
                Expense.event_id == event_id,
                Expense.payer_id == member.id
            )
        )
        paid = paid_result.scalar() or 0.0
        
        owed_result = await db.execute(
            select(func.sum(ExpenseSplit.amount)).where(
                ExpenseSplit.member_id == member.id
            )
        )
        owed = owed_result.scalar() or 0.0
        
        balances.append({
            "member_id": member.id,
            "name": member.display_name,
            "balance": float(paid - owed)
        })
    
    # Простой алгоритм расчёта settlements
    debtors = [b for b in balances if b["balance"] < 0]
    creditors = [b for b in balances if b["balance"] > 0]
    settlements = []
    
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debt = -debtors[i]["balance"]
        credit = creditors[j]["balance"]
        amount = min(debt, credit)
        
        if amount > 0.01:
            settlements.append({
                "from_user": debtors[i]["name"],
                "to_user": creditors[j]["name"],
                "amount": round(amount, 2)
            })
        
        debtors[i]["balance"] += amount
        creditors[j]["balance"] -= amount
        
        if debtors[i]["balance"] >= -0.01:
            i += 1
        if creditors[j]["balance"] <= 0.01:
            j += 1
    
    return settlements
