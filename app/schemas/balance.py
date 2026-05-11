from pydantic import BaseModel


class BalanceItem(BaseModel):
    participant_id: int
    name: str
    paid: float
    owed: float
    balance: float


class BalanceResponse(BaseModel):
    event_id: int
    balances: list[BalanceItem]