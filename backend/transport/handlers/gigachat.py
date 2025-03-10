from litestar import Request, get, post
from litestar.response import Response
from aiologger import Logger

from repositories.repositories import Repositories
from services.services import Services
from transport.schemas.response import NewResponseWithData, NewResponseWithMessageERROR


def get_model_list(route: str):
    @get(route, sync_to_thread=False)
    def handler(services: Services, logger: Logger, request: Request) -> Response:
        try:
            models = services.external_models_api.get_model_list()
            return NewResponseWithData(status_code=200, data=models)
            
        except Exception as e:
            logger.error(f"Ошибка получения моделей: {e}")
            return NewResponseWithMessageERROR(status_code=500, message="Ошибка сервера")
    
    return handler


def get_answer(route: str):
    @post(route, sync_to_thread=False)
    async def handler(repositories: Repositories,
                      services: Services, 
                      logger: Logger, 
                      request: Request) -> Response:
        try:
            body = await request.json()

            logger.info(body)

            agent_id = body.get("agent_id")
            query = body.get("query")

            if not agent_id or not query:
                return NewResponseWithMessageERROR(status_code=400, message="Отсутствует agent_id или query")

            weaviate_repository = repositories.document
            postgres_repository = repositories.agent

            agent_data = postgres_repository.get_by_id(agent_id)
            if agent_data is None:
                return NewResponseWithMessageERROR(status_code=404, message="Агент не найден")

            system_prompt = agent_data.system_prompt
            documents = weaviate_repository.search_similar(query, agent_id)

            if not documents:
                return NewResponseWithMessageERROR(status_code=500, message="Ошибка при поиске документов")

            result_document_query = [doc["content"] for doc in documents]

            models = services.external_models_api.get_answer(query, system_prompt, result_document_query, 1)
            return NewResponseWithData(status_code=200, data=models)
            
        except Exception as e:
            logger.error(f"Ошибка получения моделей: {e}")
            return NewResponseWithMessageERROR(status_code=500, message="Ошибка сервера")
    
    return handler
