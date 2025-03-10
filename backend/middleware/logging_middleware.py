import time
from litestar import Request
from litestar.types import ASGIApp, Receive, Scope, Send
from litestar.middleware import MiddlewareProtocol

from utils.logger import get_logger


logger = get_logger()


class LoggingMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start_time = time.time()

        body = await request.body()
        logger.info(
            f"Incoming request: {request.method} {request.url}\n"
            f"Request body: {body.decode(errors='ignore')}"
        )

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                self.status_code = message["status"]
            elif message["type"] == "http.response.body":
                self.response_body = message.get("body", b"")
            await send(message)

        await self.app(scope, receive, send_wrapper)

        process_time = time.time() - start_time
        logger.info(
            f"Request completed: {request.method} {request.url}\n"
            f"Status: {self.status_code}\n"
            f"Response body: {self.response_body.decode(errors='ignore')}\n"
            f"Duration: {process_time:.3f}s"
        )
