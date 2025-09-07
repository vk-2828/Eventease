from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    roles: Optional[List[str]] = ["participant"]

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    roles: List[str]
