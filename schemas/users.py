from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserRegisterSchema(BaseModel):
    id: UUID
    username: str
    password: EmailStr
    email: str
