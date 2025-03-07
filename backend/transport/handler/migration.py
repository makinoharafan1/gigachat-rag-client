from litestar import post
from aiologger import Logger
from litestar.exceptions import HTTPException

from repositories.repositories import Repositories
from services.services import Services
from transport.dto.response import Response

def upMigrations(route: str, l: Logger, r: Repositories, s: Services):
    
    @post(route, sync_to_thread=False)
    def handler() -> Response:

        try:
            s.migration.Up()
        except Exception as e:
            l.error(f"ошибка поднятия миграций {e}")
            raise HTTPException(status_code=500)

        return Response(status="OK")
    
    return handler

def downMigrations(route: str, l: Logger, r: Repositories, s: Services):
    
    @post(route, sync_to_thread=False)
    def handler() -> Response:

        try:
            s.migration.DownToBase()
        except Exception as e:
            l.error(f"ошибка сброса миграций {e}")
            raise HTTPException(status_code=500)

        return Response(status="OK")
    
    return handler