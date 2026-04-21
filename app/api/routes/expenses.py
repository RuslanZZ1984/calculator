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