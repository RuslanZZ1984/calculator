from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import ExpenseSplit
from app.schemas.split import SplitCreate


async def create_split(
    session: AsyncSession,
    data: SplitCreate
):
    split = ExpenseSplit(**data.model_dump())
    session.add(split)
    await session.commit()
    await session.refresh(split)
    return split

async def get_split(
    session: AsyncSession,
    split_id: int
):
    result = await session.execute(
        select(ExpenseSplit).where(
            ExpenseSplit.id == split_id
        )
    )
    return result.scalar_one_or_none()


async def get_splits_by_expense(
    session: AsyncSession,
    expense_id: int
):
    result = await session.execute(
        select(ExpenseSplit).where(
            ExpenseSplit.expense_id == expense_id
        )
    )
    return result.scalars().all()


async def delete_split(
    session: AsyncSession,
    split_id: int
):
    split = await get_split(session, split_id)

    if not split:
        return False
    
    await session.delete(split)
    await session.commit()
    return True