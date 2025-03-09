from litestar import Litestar
from litestar.di import Provide

from implements.services.sber_models_api import SberModelsAPI
from implements.repositories.agent_repo import PostgresAgentRepo
from implements.services.postgres_migrations import PostgresMigrationService
from services.services import Services
from repositories.repositories import Repositories

from transport.handlers.model import get_model_list
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
    return Services(
            migration=PostgresMigrationService(config),
            external_models_api=SberModelsAPI(authorization_key=config.sber_authorization_key, certificate_path="./data/certificates/russian_trusted_root_ca.cer"),
        )

repositories = get_repositories()
services = get_services()

def provide_repositories() -> Repositories:
    return repositories

def provide_services() -> Services:
    return services
 

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
        get_model_list(route="model")
    ],
    dependencies={
        "repositories": Provide(provide_repositories),
        "services": Provide(provide_services),
        "logger": Provide(get_logger)
    },
    debug=True,
)
