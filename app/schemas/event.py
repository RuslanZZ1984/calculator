from pydantic import BaseModel
from typing import Optional

class EventCreate(BaseModel):
    title: str
    owner_id: Optional[int] = None  # Теперь необязательный, будет браться из текущего пользователя

class EventRead(BaseModel):
    id: int
    title: str
    owner_id: int
    
    class Config:
        from_attributes = True
