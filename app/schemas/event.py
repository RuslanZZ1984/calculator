from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    owner_id: int

class EventRead(BaseModel):
    id: int
    title: str
    owner_id: int

    class Config:
        from_attributes = True