from starlette.middleware.base import BaseHTTPMiddleware

from middlewares.userAuthentication import UserAuth
from fastapi import FastAPI, Depends
from routers import userRouter
import models
from database import engine, SessionLocal
from fastapi.staticfiles import StaticFiles
from typing import Annotated

models.user.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="TODO tasks manager.",
    description="This is a web application based on [FastAPI](https://fastapi.tiangolo.com/) which a python based web "
                "framework.",

)
# app.mount(
#     "/static",
#     StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
# user_auth_middleware = UserAuth(my_str="my auth middleware")
app.add_middleware(UserAuth)
app.include_router(userRouter.user_router, prefix="/user")


@app.get(
    "/",
    description=" FastAPI crud homepage"
)
def root():
    return {
        "message": "Welcome to fastAPI crud."
    }
