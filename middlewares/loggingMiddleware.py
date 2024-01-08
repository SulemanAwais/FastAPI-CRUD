from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, ):
        super().__init__(
            app=app
        )

    async def dispatch(
            self, request: Request, call_next
    ) -> Response:
        try:
            json = await request.json()
            logger.info(f"A new {request.method} request has been made from {request.url.path}"
                        f" with the following data \n{json}")
        except Exception as e:
            logger.error(f"the following error was thrown by the request {request.url.path}: \n{e}")
        response = await call_next(request)
        try:
            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"{request.method} request from {request.url.path} succeeded with a status code of "
                            f" {response.status_code}")
        except Exception as e:
            logger.error(f"the following error was thrown as a response of {request.url.path} with status code "
                         f"{response.status_code}: \n{e}")
        return response
