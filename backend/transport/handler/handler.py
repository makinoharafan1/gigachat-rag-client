from litestar import Litestar
from aiologger import Logger

from services.services import Services
from repositories.repositories import Repositories

from transport.handler.ping import *
from transport.handler.migration import *

class Handler:
    def __init__(self, logger: Logger, repositories: Repositories, services: Services):
        self.logger = logger
        self.repositories = repositories
        self.services = services
    
    def CreateApp(self) -> Litestar:
        app = Litestar(
            route_handlers=[
                ping(route="ping", logger=self.logger),
                upMigrations(route="migrations/up", l=self.logger, s=self.services, r=self.repositories),
                downMigrations(route="migrations/down", l=self.logger, s=self.services, r=self.repositories),
            ]
        )

        return app

def NewHandler(logger: Logger, repositories: Repositories, services: Services) -> Handler:
    return Handler(logger, repositories, services)
