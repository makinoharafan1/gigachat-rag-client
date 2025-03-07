from litestar import get

from aiologger import Logger
from transport.dto.response import Response

def ping(route: str, logger: Logger):
    
    @get(route, sync_to_thread=False)
    def sync_hello_world() -> Response:
        return Response(status="OK")
    
    return sync_hello_world