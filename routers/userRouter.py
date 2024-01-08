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
    tags=["User"],

)


@user_router.post("/signup",
                  description="New here? SignUp to the app real quick and explore all the features.",
                  response_model=UserSchema)
def signup(
        user: UserRegisterSchema,
        request: Request,
        db: Session = Depends(get_db)
):
    try:
        user.password = request.state.hashed_password
        created_user = db_crud_user.create_user(db=db, user=user)
        if created_user is not None:
            return created_user
    except Exception as error:
        print(error)
        raise HTTPException(detail=error, status_code=400)


@user_router.post("/login",
                  description=" Already a user? login here",
                  response_model=UserSchema
                  )
def login(user: UserGetSchema,
          request: Request,
          db: Session = Depends(get_db)):
    try:
        if request.state.encoded_password:
            fetched_user = db_crud_user.get_user_with_email(db=db, email=user.email)
            if fetched_user is not None:
                import bcrypt
                encoded_password = request.state.encoded_password
                fetched_password = fetched_user.password.encode('utf-8')
                is_password_correct = bcrypt.checkpw(password=encoded_password, hashed_password=fetched_password)
                if is_password_correct:
                    return fetched_user
                else:
                    print("password not found")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=400, detail=error)
    print("request.state.encoded_password not found")
