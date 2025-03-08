from litestar import get
from litestar.response import Response
from aiologger import Logger

from transport.schemas.response import NewJSONResponseOK


def ping(route: str):
    @get(route, sync_to_thread=False)
    def handler(logger: Logger) -> Response:
        logger.info("Обработка запроса ping")
        return NewJSONResponseOK(status_code=200)
    return handler
