from pydantic import BaseModel


class SplitCreate(BaseModel):
    expense_id: int
    participant_id: int
    amount: float


class SplitRead(BaseModel):
    id: int
    expense_id: int
    participant_id: int
    amount: float

    class Config:
        from_attributes = True