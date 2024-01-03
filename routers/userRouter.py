from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db_crud import user as db_crud_user
from database import SessionLocal
from schemas.users import UserRegisterSchema


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(
    prefix="/register",
)


@user_router.post(
    "/",
    description="New here? SignUp to the app real quick and explore all the features."
)
def user_register(
        user: UserRegisterSchema,
        db: Session = Depends(get_db)
):
    return {
        db_crud_user.create_user(
            db=db,
            user=user
        )
    }
