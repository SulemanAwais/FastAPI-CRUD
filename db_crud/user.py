from sqlalchemy.orm import Session
from schemas.users import UserRegisterSchema, UserGetSchema
from models.user import User


def create_user(db: Session, user: UserRegisterSchema):
    db_user = User(username=user.username, email=user.email, password=user.password,)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as error:
        print(error)


def get_user_with_email_and_password(db: Session, user: UserGetSchema):
    try:
        return db.query(User).filter(User.email == user.email and user.password == user.password).first()
    except Exception as error:
        print(error)
