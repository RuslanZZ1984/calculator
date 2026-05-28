from pydantic import BaseModel


class MemberCreate(BaseModel):
    event_id: int
    user_id: int
    display_name: str


class MemberRead(BaseModel):
    id: int
    event_id: int
    user_id: int
    display_name: str

    class Config:
        from_attributes = True