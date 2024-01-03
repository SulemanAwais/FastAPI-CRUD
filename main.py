from fastapi import FastAPI
from routers import userRouter
import models
from database import engine, SessionLocal
models.user.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="TODO tasks manager.",
    description="This is a web application based on [FastAPI](https://fastapi.tiangolo.com/) which a python based web "
                "framework.",

)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
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

