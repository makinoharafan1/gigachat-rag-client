from litestar import Request, get, post, put
from litestar.response import Response
from aiologger import Logger

from entities.agent_model import Agent, AgentShortSchema
from repositories.repositories import Repositories
from services.services import Services
from transport.schemas.response import (
    NewResponseWithData,
    NewResponseWithMessageERROR,
    NewJSONResponseOK,
)


def get_agent_list_by_filters(route: str):
    @get(route, sync_to_thread=False)
    def handler(
        repositories: Repositories, services: Services, logger: Logger, request: Request
    ) -> Response:
        try:
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 50))

            limit = max(min(limit, 50), 1)
            page = max(page, 1)

            agents = repositories.agent.get_base_info_by_filters(page=page, limit=limit)

            agents = [
                AgentShortSchema(
                    id=agent.id,
                    title=agent.title,
                    logo=agent.logo,
                )
                for agent in agents
            ]

            return NewResponseWithData(
                status_code=200, data=[agent.model_dump() for agent in agents]
            )

        except Exception as e:
            logger.error(f"Ошибка получения агента по id: {e}")
            return NewResponseWithMessageERROR(
                status_code=500, message="Ошибка сервера"
            )

    return handler


def get_agent_by_id(route: str):
    @get(route, sync_to_thread=False)
    def handler(
        repositories: Repositories, services: Services, logger: Logger, request: Request
    ) -> Response:
        try:
            id = int(request.path_params["id"])
            agent = repositories.agent.get_by_id(id=id)

            if agent == None:
                return NewResponseWithMessageERROR(
                    status_code=400, message="Агент с таким id не найден"
                )

            return NewResponseWithData(status_code=200, data=agent.model_dump())

        except Exception as e:
            logger.error(f"Ошибка получения агента по id: {e}")
            return NewResponseWithMessageERROR(
                status_code=500, message="Ошибка сервера"
            )

    return handler


def create_agent(route: str):
    @post(route)
    async def handler(
        repositories: Repositories, services: Services, logger: Logger, request: Request
    ) -> Response:
        try:
            body = await request.json()
            try:
                agent = Agent(**body)
            except:
                return NewResponseWithMessageERROR(
                    status_code=400, message="Неверный набор данных"
                )
            id = repositories.agent.create(agent=agent)

            return NewResponseWithData(status_code=200, data={"id": id})

        except Exception as e:
            logger.error(f"Ошибка создания агента: {e}")
            return NewResponseWithMessageERROR(
                status_code=500, message="Ошибка сервера"
            )

    return handler


def update_agent(route: str):
    @put(route)
    async def handler(
        repositories: Repositories, services: Services, logger: Logger, request: Request
    ) -> Response:
        try:
            body = await request.json()
            id = int(request.path_params["id"])

            try:
                agent = Agent(**body)
            except:
                return NewResponseWithMessageERROR(
                    status_code=400, message="Неверный набор данных"
                )

            repositories.agent.update(id=id, agent=agent)

            return NewJSONResponseOK(status_code=201)

        except Exception as e:

            logger.error(f"Ошибка обновления агента: {e}")
            return NewResponseWithMessageERROR(
                status_code=500, message="Ошибка сервера"
            )

    return handler


def delete_agent(route: str):
    @post(route, sync_to_thread=False)
    def handler(
        repositories: Repositories, services: Services, logger: Logger, request: Request
    ) -> Response:
        try:
            id = int(request.path_params["id"])
            repositories.agent.delete(id=id)
            return NewJSONResponseOK(status_code=200)

        except Exception as e:
            logger.error(f"Ошибка удаления агента: {e}")
            return NewResponseWithMessageERROR(
                status_code=500, message="Ошибка сервера"
            )

    return handler
