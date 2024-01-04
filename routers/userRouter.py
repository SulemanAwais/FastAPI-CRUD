from middlewares.userAuthentication import UserAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db_crud import user as db_crud_user
from database import SessionLocal
from schemas.users import UserRegisterSchema, UserSchema, UserGetSchema


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(
    prefix="/home",
    tags=["User"]
)


@user_router.post("/signup",
                  description="New here? SignUp to the app real quick and explore all the features.",
                  response_model=UserSchema)
def signup(user: UserRegisterSchema, db: Session = Depends(get_db), hashed_password: str = Depends(UserAuth)):
    try:
        user.password = hashed_password
        created_user = db_crud_user.create_user(db=db, user=user)
        print("user->", user)
        if created_user is not None:
            return created_user
    except Exception as error:
        print(error)
        raise HTTPException(detail=error, status_code=400)


@user_router.post("/login",
                  description=" Already a user? login here",
                  response_model=UserSchema
                  )
def login(user: UserGetSchema, db: Session = Depends(get_db)):
    try:

        fetched_user = db_crud_user.get_user_with_email_and_password(db=db, user=user)
        if fetched_user is not None:
            return fetched_user
    except Exception as error:
        print(error)
