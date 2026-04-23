from typing import Dict, List


def calculate_settlements(balances: Dict[int, dict]) -> List[dict]:
    """
    Превращает balances в список переводов:
    кто -> кому -> сколько
    """

    creditors = []
    debtors = []

    # 1. Разделяем
    for participant_id, data in balances.items():
        balance = round(data["balance"], 2)

        if balance > 0:
            creditors.append({
                "id": participant_id,
                "name": data["name"],
                "amount": balance
            })
        elif balance < 0:
            debtors.append({
                "id": participant_id,
                "name": data["name"],
                "amount": -balance  # делаем положительным долг
            })

    # 2. Сортируем (для стабильности и красоты)
    creditors.sort(key=lambda x: x["amount"], reverse=True)
    debtors.sort(key=lambda x: x["amount"], reverse=True)

    settlements = []

    i = 0  # debtor index
    j = 0  # creditor index

    # 3. Гасим долги
    while i < len(debtors) and j < len(creditors):

        debtor = debtors[i]
        creditor = creditors[j]

        pay_amount = min(debtor["amount"], creditor["amount"])

        settlements.append({
            "from": debtor["name"],
            "to": creditor["name"],
            "amount": round(pay_amount, 2)
        })

        debtor["amount"] -= pay_amount
        creditor["amount"] -= pay_amount

        # двигаем указатели
        if debtor["amount"] == 0:
            i += 1
        if creditor["amount"] == 0:
            j += 1

    return settlements