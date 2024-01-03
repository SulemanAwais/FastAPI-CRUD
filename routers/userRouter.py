from fastapi import APIRouter

from schemas.users import UserRegisterSchema

user_router = APIRouter(
    prefix="/register",
)


@user_router.post(
    "/",
    description="New here? SignUp to the app real quick and explore all the features."
)
def user_register(
        credentials: UserRegisterSchema
):
    return {
        "message": "wait"
    }
