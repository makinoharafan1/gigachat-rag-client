from litestar import Litestar
from litestar.di import Provide

from implements.repositories.agent_repo import PostgresAgentRepo
from implements.services.postgres_migrations import PostgresMigrationService
from services.services import Services
from repositories.repositories import Repositories

from transport.handlers.agent import create_agent, get_agent_by_id, update_agent, delete_agent, get_agent_list_by_filters
from transport.handlers.ping import ping
from transport.handlers.migration import up_migrations, down_migrations

from utils.psycopg2 import posgtres_connection_pool
from utils.config import config
from utils.logger import get_logger


def get_repositories() -> Repositories:

    pool = posgtres_connection_pool(config)

    return Repositories(
        agent=PostgresAgentRepo(pool=pool)
    )


def get_services() -> Services:
    return Services(migration=PostgresMigrationService(config))


app = Litestar(
    route_handlers=[
        ping(route="ping"),
        up_migrations(route="migrations/up"),
        down_migrations(route="migrations/down"),
        get_agent_by_id(route="agent/{id:int}"),
        get_agent_list_by_filters(route="agent"),
        create_agent(route="agent"),
        update_agent(route="agent/{id:int}"),
        delete_agent(route="agent/delete/{id:int}"),
    ],
    dependencies={
        "repositories": Provide(get_repositories),
        "services": Provide(get_services),
        "logger": Provide(get_logger)
    },
    debug=True,
)
