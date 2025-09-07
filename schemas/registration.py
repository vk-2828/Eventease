from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RegistrationCreate(BaseModel):
    event_id: str
    name: str
    email: EmailStr
    college: Optional[str] = ""
    phone: Optional[str] = ""

class RegistrationOut(RegistrationCreate):
    id: str
    created_at: datetime
