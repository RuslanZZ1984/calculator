from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExpenseCreate(BaseModel):
    event_id: int
    payer_id: int
    amount: float
    description: str | None = None


class ExpenseRead(BaseModel):
    id: int
    event_id: int
    payer_id: int
    amount: float
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseUpdate(BaseModel):
    event_id: Optional[int] = None
    payer_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None
