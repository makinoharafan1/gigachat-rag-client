from litestar import get
from aiologger import Logger

from transport.schemas.response import Response


def ping(route: str):
    @get(route, sync_to_thread=False)
    def handler(logger: Logger) -> Response:
        logger.info("Обработка запроса ping")
        return Response(status="OK")
    return handler
