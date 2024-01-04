from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr


class UserGetSchema(BaseModel):
    email: EmailStr
    password: str
