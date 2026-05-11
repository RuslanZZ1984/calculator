from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.expense import ExpenseCreate, ExpenseRead
from app.services.expense import create_expense_service


router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/") # тестовый
async def get_expenses():
    return {"message": "Expenses endpoint"}


@router.post("/", response_model=ExpenseRead)
async def create_expense(
    data: ExpenseCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_expense_service(session, data)


@router.get("/event/{event_id}", response_model=list[ExpenseRead])
async def get_event_expenses(
    event_id: int,
    session: AsyncSession = Depends(get_session),
):
    from app.crud.expense import get_expenses_by_event
    return await get_expenses_by_event(session, event_id)