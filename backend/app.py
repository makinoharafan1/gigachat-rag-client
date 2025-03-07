from __future__ import annotations

from implements.services.postgres_migrations import PostgresMigrationService


from utils.psycopg2 import NewPosgtresConnectionPool
from utils.config import Config, NewConfig
from utils.logger import setup_logger
from services.services import Services
from repositories.repositories import Repositories
from transport.handler.handler import NewHandler

def getRepositories(storage) -> Repositories:

    return Repositories()

def getServices(config: Config) -> Services:

    return Services(migration=PostgresMigrationService(config))

config = NewConfig()
logger = setup_logger()
storage = NewPosgtresConnectionPool(config)

repositories = getRepositories(storage=storage)
services = getServices(config=config)

handler = NewHandler(logger, repositories, services)
app = handler.CreateApp()
