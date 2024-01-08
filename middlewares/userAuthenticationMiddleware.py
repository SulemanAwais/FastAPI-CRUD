from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class UserAuth(BaseHTTPMiddleware):
    def __init__(self, app, ):
        super().__init__(
            app=app
        )

    async def dispatch(
            self, request: Request, call_next
    ):
        if request.url.path == "/user/home/signup" and request.method == "POST":
            try:
                json_data = await request.json()
                password = json_data.get("password")
                if password:
                    import bcrypt
                    password_bytes = password.encode('utf-8')  # converting password into bytes
                    salt = bcrypt.gensalt()  # salt is used to add some extra text to the password
                    hashed_password = bcrypt.hashpw(password_bytes, salt)
                    hashed_password = hashed_password.decode('utf-8')
                    request.state.hashed_password = hashed_password
            except Exception as error:
                print(error, "\nError from middleware while login")
                raise HTTPException(status_code=400, detail=error)

        if request.url.path == "/user/home/login" and request.method == "POST":
            try:
                json_data = await request.json()
                password = json_data.get("password")
                if password:
                    import bcrypt
                    encoded_password = password.encode("utf-8")
                    request.state.encoded_password = encoded_password
            except Exception as error:
                print(error, "\nError from middleware while login")
                raise HTTPException(status_code=400, detail=error)
        return await call_next(request)

