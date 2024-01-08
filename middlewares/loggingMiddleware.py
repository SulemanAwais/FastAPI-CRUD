from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from database import SessionLocal
from logger import logger
from models.Logs import Log


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app,):
        super().__init__(
            app=app
        )

    async def dispatch(
            self, request: Request, call_next
    ) -> Response:
        try:
            json = await request.json()
            message = f"A new {request.method} request has been made from {request.url.path} with the following data \n{json}"
            logger.info(message)
            log = Log(message=message)
            with SessionLocal() as session:
                session.add(log)
                session.commit()
                session.refresh(log)

        except Exception as e:
            message = f"the following error was thrown by the request {request.url.path}: \n{e}"
            logger.error(message)
            log = Log(message=message)
            with SessionLocal() as session:
                session.add(log)
                session.commit()
                session.refresh(log)
        response = await call_next(request)
        try:
            if response.status_code == 200 or response.status_code == 201:
                message = f"{request.method} request from {request.url.path} succeeded with a status code of {response.status_code}"
                logger.info(message)
                log = Log(message=message)
                with SessionLocal() as session:
                    session.add(log)
                    session.commit()
                    session.refresh(log)

        except Exception as e:
            message = f"the following error was thrown as a response of {request.url.path} with status code {response.status_code}: \n{e}"
            logger.error(message)
            log = Log(message=message)
            with SessionLocal() as session:
                session.add(log)
                session.commit()
                session.refresh(log)
        return response


