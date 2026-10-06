from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    phone: str | None = None
    password: str = Field(min_length=8)
    language: str = "kn"


class LoginRequest(BaseModel):
    identifier: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int


class UserMeResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    language: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }