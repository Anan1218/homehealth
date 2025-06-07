from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    created_at: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: int
    user: UserResponse 