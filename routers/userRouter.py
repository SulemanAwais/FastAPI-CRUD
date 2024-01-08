from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

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

templates = Jinja2Templates(
    directory="static"
)


@user_router.post("/signup-form")
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@user_router.post("/signup",
                  description="New here? SignUp to the app real quick and explore all the features.")
async def signup(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        user = UserRegisterSchema(username=username, password=password, email=email)
        # print(user)
        # user.password = await request.state.hashed_password
        created_user = db_crud_user.create_user(db=db, user=user)
        return templates.TemplateResponse("welcome.html", {"request": request, "user": created_user, "username": created_user.username})
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
