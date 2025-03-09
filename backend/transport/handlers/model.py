from litestar import Request, get, post
from litestar.response import Response
from aiologger import Logger

from repositories.repositories import Repositories
from services.services import Services
from transport.schemas.response import NewResponseWithData, NewResponseWithMessageERROR

def get_model_list(route: str):
    
    @get(route, sync_to_thread=False)
    def handler(repositories: Repositories, services: Services, logger: Logger, request: Request) -> Response:
        
        try:

            models = services.external_models_api.get_model_list()

            return NewResponseWithData(status_code=200, data=models)
            
        except Exception as e:

            logger.error(f"Ошибка получения моделей: {e}")
            return NewResponseWithMessageERROR(status_code=500, message="Ошибка сервера")
    
    
    return handler
