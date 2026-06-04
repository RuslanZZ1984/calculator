from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import split as split_crud
from app.crud import expense as expense_crud
from app.crud import member as member_crud

from app.schemas.split import SplitCreate


async def create_split_service(
    session: AsyncSession,
    data: SplitCreate
):
    expense = await expense_crud.get_expense(
        session,
        data.expense_id
    )
    if not expense:
        raise ValueError("Расход не найден")
    
    member = await member_crud.get_member(
        session,
        data.member_id
    )
    if not member:
        raise ValueError("Участник не найден")
    
    if member.event_id != expense.event_id:
        raise ValueError("Участник не из этого события")
    
    return await split_crud.create_split(session, data)


async def get_expense_splits_service(
    session: AsyncSession,
    expence_id: int
):
    return await split_crud.get_splits_by_expense(
        session,
        expence_id
    )


async def delete_split_service(
    session: AsyncSession,
    split_id: int
):
    return await split_crud.delete_split(
        session,
        split_id
    )