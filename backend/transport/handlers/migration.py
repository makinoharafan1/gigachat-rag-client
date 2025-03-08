from litestar import post
from litestar.exceptions import HTTPException
from aiologger import Logger

from repositories.repositories import Repositories
from services.services import Services
from transport.schemas.response import Response


def up_migrations(route: str):
    @post(route, sync_to_thread=False)
    def handler(services: Services, logger: Logger) -> Response:
        try:
            services.migration.up()
        except Exception as e:
            logger.error(f"Ошибка поднятия миграций: {e}")
            raise HTTPException(status_code=500, detail="Ошибка поднятия миграций")
        return Response(status="OK")
    return handler


def down_migrations(route: str):
    @post(route, sync_to_thread=False)
    def handler(services: Services, logger: Logger) -> Response:
        try:
            services.migration.down_to_base()
        except Exception as e:
            logger.error(f"Ошибка сброса миграций: {e}")
            raise HTTPException(status_code=500, detail="Ошибка сброса миграций")
        return Response(status="OK")
    return handler
