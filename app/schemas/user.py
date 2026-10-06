from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    password: str
    language: str = "kn"


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    language: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }