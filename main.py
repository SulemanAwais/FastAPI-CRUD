from middlewares.loggingMiddleware import LoggingMiddleware
from middlewares.userAuthenticationMiddleware import UserAuth
from fastapi import FastAPI, Depends
from routers import userRouter
import models
from database import engine
from logger import logger
from routers.userRouter import get_db

models.user.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="TODO tasks manager.",
    description="This is a web application based on [FastAPI](https://fastapi.tiangolo.com/) which a python based web "
                "framework.",
    debug=True,
)
logger.info("STARING FASTAPI APP...")

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
app.add_middleware(UserAuth)
app.add_middleware(LoggingMiddleware)
app.include_router(userRouter.user_router, prefix="/user")


@app.get(
    "/",
    description=" FastAPI crud homepage"
)
def root():
    return {
        "message": "Welcome to fastAPI crud."
    }
