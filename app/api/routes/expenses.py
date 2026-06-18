from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_session
from app.schemas.expense import ExpenseCreate, ExpenseRead
from app.services.expense import create_expense_service, get_expenses_service, get_event_expenses_service
from app.depends.auth import get_current_user
from app.db.models import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/", response_model=List[ExpenseRead])
async def get_expenses(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_expenses_service(session)

@router.post("/", response_model=ExpenseRead)
async def create_expense(
    data: ExpenseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_expense_service(session, data)

@router.get("/event/{event_id}", response_model=List[ExpenseRead])
async def get_event_expenses(
    event_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_event_expenses_service(session, event_id)
