from sqlalchemy.orm import Session
from schemas.users import UserRegisterSchema
from models.user import User


def create_user(
        db: Session,
        user: UserRegisterSchema
):
    db_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
