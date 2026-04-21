from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.db.models import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


# Create
async def create_expense(session: AsyncSession, data: ExpenseCreate) -> Expense:
    expense = Expense(**data.model_dump())
    session.add(expense)
    await session.commit()
    await session.refresh(expense)
    return expense

# Read one
async def get_expense(session: AsyncSession, expense_id: int) -> Expense | None:
    result = await session.execute(
        select(Expense).where(Expense.id == expense_id)
    )
    return result.scalar_one_or_none()

# read many
async def get_expenses_by_user(session: AsyncSession, payer_id: int):
    result = await session.execute(
        select(Expense).where(Expense.payer_id == payer_id)
    )
    return result.scalars().all()

# Update
async def update_expense(
    session: AsyncSession,
    expense_id: int,
    data: ExpenseUpdate
) -> Expense | None:
    result = await session.execute(
        select(Expense).where(Expense.id == expense_id)
    )
    expense = result.scalar_one_or_none()

    if not expense:
        return None
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)
    
    await session.commit()
    await session.refresh(expense)
    return expense

# Delete
async def delete_expense(session: AsyncSession, expense_id: int) -> bool:
    result = await session.execute(
        select(Expense).where(Expense.id == expense_id)
    )
    expense = result.scalar_one_or_none()

    if not expense:
        return False
    
    await session.delete(expense)
    await session.commit()
    return True
