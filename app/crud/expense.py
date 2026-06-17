from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Expense

async def get_expenses(db: AsyncSession):
    result = await db.execute(select(Expense))
    return result.scalars().all()

async def get_expense_by_id(db: AsyncSession, expense_id: int):
    result = await db.execute(select(Expense).where(Expense.id == expense_id))
    return result.scalar_one_or_none()

async def get_expenses_by_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Expense).where(Expense.event_id == event_id))
    return result.scalars().all()

async def delete_expenses_by_event(db: AsyncSession, event_id: int):
    await db.execute(delete(Expense).where(Expense.event_id == event_id))
    await db.commit()

async def create_expense(db: AsyncSession, expense_data):
    expense = Expense(**expense_data.model_dump())
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense
