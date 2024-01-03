from fastapi import FastAPI
from routers import userRouter
app = FastAPI(
    title="TODO tasks manager.",
    description="This is a web application based on [FastAPI](https://fastapi.tiangolo.com/) which a python based web "
                "framework.",

)
app.include_router(userRouter.user_router, prefix="/user")


@app.get(
    "/",
    description=" FastAPI crud homepage"
)
def root():
    return {
        "message": "Welcome to fastAPI crud."
    }

