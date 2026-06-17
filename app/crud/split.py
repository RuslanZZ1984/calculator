from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ExpenseSplit

async def get_splits(db: AsyncSession):
    result = await db.execute(select(ExpenseSplit))
    return result.scalars().all()

async def get_splits_by_expense(db: AsyncSession, expense_id: int):
    result = await db.execute(select(ExpenseSplit).where(ExpenseSplit.expense_id == expense_id))
    return result.scalars().all()

async def get_splits_by_event(db: AsyncSession, event_id: int):
    result = await db.execute(
        select(ExpenseSplit).join(ExpenseSplit.expense).where(ExpenseSplit.expense.has(event_id=event_id))
    )
    return result.scalars().all()

async def delete_splits_by_expense(db: AsyncSession, expense_id: int):
    await db.execute(delete(ExpenseSplit).where(ExpenseSplit.expense_id == expense_id))
    await db.commit()

async def delete_splits_by_event(db: AsyncSession, event_id: int):
    splits = await get_splits_by_event(db, event_id)
    for split in splits:
        await db.delete(split)
    await db.commit()

async def create_split(db: AsyncSession, split_data):
    split = ExpenseSplit(**split_data.model_dump())
    db.add(split)
    await db.commit()
    await db.refresh(split)
    return split
