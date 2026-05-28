from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    login: str
    password: str
    username: str

class UserRead(BaseModel):
    id: int
    login: str
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True