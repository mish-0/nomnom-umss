from pydantic import BaseModel, EmailStr, ConfigDict

from app.core.enums import UserRole


class UserCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    last_name: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)