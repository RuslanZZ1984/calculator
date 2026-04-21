from pydantic import BaseModel


class ParticipantCreate(BaseModel):
    event_id: int
    user_id: int
    display_name: str


class ParticipanRead(BaseModel):
    id: int
    event_id: int
    user_id: int
    display_name: str

    class Config:
        from_attributes = True