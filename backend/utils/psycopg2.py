import psycopg2
from psycopg2 import pool

from utils.config import Config

def NewPosgtresConnectionPool(config: Config):
    connectionPool = psycopg2.pool.SimpleConnectionPool(
        config.storage.minConnections,
        config.storage.maxConnections,
        dbname=config.storage.dbName,
        user=config.storage.dbUser,
        password=config.storage.dbPassword,
        host=config.storage.dbHost,
        port=config.storage.dbPort
    )

    return connectionPool
