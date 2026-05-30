import asyncio
import random

from app.db.session import AsyncSessionLocal

from app.schemas.user import UserCreate
from app.schemas.event import EventCreate
from app.schemas.member import MemberCreate
from app.schemas.expense import ExpenseCreate
from app.schemas.split import SplitCreate

from app.services.settlement_service import calculate_settlements
from app.services.user import create_user_service
from app.services.event import create_event_service
from app.services.member import create_member_service
from app.services.expense import create_expense_service
from app.services.split import create_split_service
from app.services.balance import calculate_event_balances_service


names = [
    "Ruslan", "Svetlana", "Anton", "Maria",
    "Ivan", "Olga", "Pavel", "Elena",
    "Dmitry", "Nastya", "Kirill", "Oleg",
    "Anna", "Sergey", "Yulia", "Maxim",
    "Irina", "Viktor", "Airat", "Roman"
]


async def test():
    async with AsyncSessionLocal() as session:

        # 1. Users
        users = []

        for name in names:
            user = await create_user_service(
                session,
                UserCreate(
                    username=f"{name}_test_3_login",
                    password="123",
                    username=f"{name}_test_3"
                )
            )
            users.append(user)

        # 2. Event
        event = await create_event_service(
            session,
            EventCreate(
                title="Dinner_3",
                owner_id=users[0].id
            )
        )

        print("EVENT:", event.id, event.title)

        # 3. Members
        members = []

        for i, user in enumerate(users):
            p = await create_member_service(
                session,
                MemberCreate(
                    event_id=event.id,
                    user_id=user.id,
                    display_name=names[i]
                )
            )
            members.append(p)

        # 4. Expenses
        expenses = []

        for _ in range(10):
            payer = random.choice(members)
            amount = random.randint(100, 2000)

            expense = await create_expense_service(
                session,
                ExpenseCreate(
                    event_id=event.id,
                    payer_id=payer.id,
                    amount=amount,
                    description="Random expense"
                )
            )

            expenses.append(expense)

        # 5. Splits
        for expense in expenses:
            split_amount = round(expense.amount / len(members), 2)

            for m in members:
                await create_split_service(
                    session,
                    SplitCreate(
                        expense_id=expense.id,
                        member_id=m.id,
                        amount=split_amount
                    )
                )

        # 6. BALANCES
        balances = await calculate_event_balances_service(
            session,
            event.id
        )

        print("\nBALANCES:")
        for _, data in balances.items():
            print(
                data["name"],
                "paid =", data["paid"],
                "owed =", data["owed"],
                "balance =", data["balance"]
            )

        # 7. SETTLEMENTS
        settlements = calculate_settlements(balances)

        print("\nSETTLEMENTS:")
        for s in settlements:
            print(f'{s["from"]} -> {s["to"]} : {s["amount"]}')


if __name__ == "__main__":
    asyncio.run(test())