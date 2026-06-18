from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import expense as expense_crud
from app.schemas.expense import ExpenseCreate

async def create_expense_service(db: AsyncSession, expense_data: ExpenseCreate):
    return await expense_crud.create_expense(db, expense_data)

async def get_expenses_service(db: AsyncSession):
    return await expense_crud.get_expenses(db)

async def get_event_expenses_service(db: AsyncSession, event_id: int):
    return await expense_crud.get_expenses_by_event(db, event_id)
