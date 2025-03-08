from litestar import post
from litestar.response import Response
from aiologger import Logger

from services.services import Services
from transport.schemas.response import NewJSONResponseOK, NewResponseWithMessageERROR


def up_migrations(route: str):
    @post(route, sync_to_thread=False)
    def handler(services: Services, logger: Logger) -> Response:
        
        try:
            services.migration.up()
            return NewJSONResponseOK(status_code=200)
        except Exception as e:
            logger.error(f"Ошибка поднятия миграций: {e}")
            return NewResponseWithMessageERROR(status_code=500, message="Ошибка поднятия миграций")
        
    return handler


def down_migrations(route: str):
    @post(route, sync_to_thread=False)
    def handler(services: Services, logger: Logger) -> Response:
        
        try:
            services.migration.down_to_base()
            return NewJSONResponseOK(status_code=200)
        except Exception as e:
            logger.error(f"Ошибка сброса миграций: {e}")
            return NewResponseWithMessageERROR(status_code=500, message="Ошибка сброса миграций")
    
    return handler
