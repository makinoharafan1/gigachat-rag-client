from litestar import Litestar
from litestar.di import Provide

from repositories.repositories import Repositories
from implements.repositories.postgres_repository import PostgresAgentRepository
from implements.repositories.weaviate_repository import WeaviateDocumentRepository

from services.services import Services
from implements.services.gigachat_api import GigaChatAPI
from implements.services.postgres_migrations import PostgresMigrationService

from middleware.logging_middleware import LoggingMiddleware

from transport.handlers.gigachat import get_model_list, get_answer
from transport.handlers.agent import (
    create_agent,
    get_agent_by_id,
    update_agent,
    delete_agent,
    get_agent_list_by_filters,
)
from transport.handlers.document import insert_document, search_similar_documents
from transport.handlers.ping import ping
from transport.handlers.migration import up_migrations, down_migrations

from utils.psycopg2 import posgtres_connection_pool
from utils.config import config
from utils.logger import get_logger
from utils.vectorizer import HFVectorizer


vectorizer = HFVectorizer(model_name="cointegrated/rubert-tiny2")


def get_repositories() -> Repositories:
    pool = posgtres_connection_pool(config)
    return Repositories(
        agent=PostgresAgentRepository(pool=pool),
        document=WeaviateDocumentRepository(vectorizer=vectorizer)
    )


def get_services() -> Services:
    return Services(
        migration=PostgresMigrationService(config),
        external_models_api=GigaChatAPI(
            authorization_key=config.gigachat_authorization_key,
            certificate_path="./data/certificates/russian_trusted_root_ca.cer",
        ),
    )


repositories = get_repositories()
services = get_services()


def provide_repositories() -> Repositories:
    return repositories


def provide_services() -> Services:
    return services


def provide_vectorizer() -> HFVectorizer:
    return vectorizer


def on_startup():
    repositories.document.create_collection()


def on_shutdown():
    repositories.document.delete_collection()


app = Litestar(
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    route_handlers=[
        ping(route="ping"),
        up_migrations(route="migrations/up"),
        down_migrations(route="migrations/down"),
        get_agent_by_id(route="agent/{id:int}"),
        get_agent_list_by_filters(route="agent"),
        create_agent(route="agent"),
        update_agent(route="agent/{id:int}"),
        delete_agent(route="agent/delete/{id:int}"),
        get_model_list(route="model"),
        get_answer(route="answer"),
        insert_document(route="insert"),
        search_similar_documents(route="similar")
    ],
    middleware=[LoggingMiddleware],
    dependencies={
        "repositories": Provide(provide_repositories, sync_to_thread=False),
        "services": Provide(provide_services, sync_to_thread=False),
        "vectorizer": Provide(provide_vectorizer, sync_to_thread=False),
        "logger": Provide(get_logger, sync_to_thread=False)
    },
    debug=True,
)
