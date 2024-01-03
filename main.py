from fastapi import FastAPI

app = FastAPI(
    title="TODO tasks manager.",
    description="This is a web application based on [FastAPI](https://fastapi.tiangolo.com/) which a python based web "
                "framework.",

)


@app.get(
    "/",
    description=" FastAPI crud homepage"
)
def root():
    return {
        "message": "Welcome to fastAPI crud."
    }
