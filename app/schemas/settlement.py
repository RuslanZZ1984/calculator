from pydantic import BaseModel


class SettlementItem(BaseModel):
    from_user: str
    to_user: str
    amount: float


class SettlementResponse(BaseModel):
    event_id: int
    settlements: list[SettlementItem]