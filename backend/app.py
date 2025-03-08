from litestar import Litestar
from litestar.di import Provide

from implements.services.postgres_migrations import PostgresMigrationService
from services.services import Services
from repositories.repositories import Repositories
from transport.handlers.ping import ping
from transport.handlers.migration import up_migrations, down_migrations
from utils.config import config
from utils.logger import get_logger


def get_repositories() -> Repositories:
    return Repositories()


def get_services() -> Services:
    return Services(migration=PostgresMigrationService(config))


app = Litestar(
    route_handlers=[
        ping(route="ping"),
        up_migrations(route="migrations/up"),
        down_migrations(route="migrations/down"),
    ],
    dependencies={
        "repositories": Provide(get_repositories),
        "services": Provide(get_services),
        "logger": Provide(get_logger)
    },
    debug=True,
)
