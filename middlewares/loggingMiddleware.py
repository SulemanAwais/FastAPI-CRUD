from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from database import SessionLocal
from logger import logger
from models.Logs import Log


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, request_message: str = "", response_message: str = ""):
        super().__init__(
            app=app
        )
        self.request_message = request_message
        self.response_message = response_message

    async def dispatch(
            self, request: Request, call_next
    ) -> Response:
        try:
            json = await request.json()
            self.request_message = f"A new {request.method} request has been made from {request.url.path} with the following data \n{json}"
        except Exception as e:
            self.request_message = f"the following error was thrown by the request {request.url.path}: \n{e}"
        logger.error(self.request_message)
        response = await call_next(request)
        try:
            if response.status_code == 200 or response.status_code == 201:
                self.response_message = f"{request.method} request from {request.url.path} succeeded with a status code of {response.status_code}"
            else:
                self.response_message = f"An error was thrown as a response of {request.url.path} with status code {response.status_code}"
        except Exception as e:
            self.response_message = f"the following error was thrown as a response of {request.url.path} with status code {response.status_code}: \n{e}"
            logger.error(self.response_message)

        self.save_log()
        return response

    def save_log(self):
        request_log = Log(message=self.request_message)
        response_log = Log(message=self.response_message)
        with SessionLocal() as session:
            session.add(request_log)
            session.add(response_log)
            session.commit()
            session.refresh(request_log)
            session.refresh(response_log)
