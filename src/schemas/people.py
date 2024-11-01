from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PeopleBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True


class PeopleCreate(PeopleBase):
    password_hash: str  # Изменено на password_hash


class PeopleOut(PeopleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class PeopleUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
