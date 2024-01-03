from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserRegisterSchema(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
