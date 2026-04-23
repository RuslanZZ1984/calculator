# !!!! ЭТОТ лишний уже, не нужен

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.balance import calculate_event_balances_service


async def calculate_settlements_service(
    session: AsyncSession,
    event_id: int
):
    balances = await calculate_event_balances_service(session, event_id)

    creditors = []
    debtors = []

    # 1. разделяем ВСЕХ сразу
    for data in balances.values():
        balance = round(data["balance"], 2)

        if balance > 0:
            creditors.append({
                "name": data["name"],
                "amount": balance
            })
        elif balance < 0:
            debtors.append({
                "name": data["name"],
                "amount": -balance
            })

    # 2. сортировка (очень желательно)
    creditors.sort(key=lambda x: x["amount"], reverse=True)
    debtors.sort(key=lambda x: x["amount"], reverse=True)

    settlements = []

    i = 0
    j = 0

    # 3. только теперь расчёт
    while i < len(debtors) and j < len(creditors):

        debtor = debtors[i]
        creditor = creditors[j]

        pay = min(debtor["amount"], creditor["amount"])

        settlements.append({
            "from": debtor["name"],
            "to": creditor["name"],
            "amount": round(pay, 2)
        })

        debtor["amount"] -= pay
        creditor["amount"] -= pay

        if debtor["amount"] == 0:
            i += 1
        if creditor["amount"] == 0:
            j += 1

    return settlements