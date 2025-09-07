from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    date: datetime
    venue: Optional[str] = None
    description: Optional[str] = ""
    schedule: Optional[str] = ""
    rules: Optional[str] = ""
    contact: Optional[str] = ""

class EventOut(EventCreate):
    id: str
