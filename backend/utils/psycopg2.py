from psycopg2.pool import SimpleConnectionPool

from utils.config import AppConfig


def posgtres_connection_pool(config: AppConfig):
    connection_pool = SimpleConnectionPool(
        config.postgres_db_min_connections,
        config.postgres_db_max_connections,
        dbname=config.postgres_db_name,
        user=config.postgres_db_username,
        password=config.postgres_db_password,
        host=config.postgres_db_host,
        port=config.postgres_db_port
    )

    return connection_pool
