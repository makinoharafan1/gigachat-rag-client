import os
from dotenv import load_dotenv

class Storage:
    def __init__(self):
        self.dbHost = os.getenv('DB_HOST')
        self.dbPort = os.getenv('DB_PORT')
        self.dbName = os.getenv('DB_NAME')
        self.dbUser = os.getenv('DB_USER')
        self.dbPassword = os.getenv('DB_PASSWORD')

        self.minConnections = os.getenv('DB_MIN_CON', 1)
        self.maxConnections = os.getenv('DB_MAX_CON', 10)

class Config:
    def __init__(self):
        load_dotenv()
        self.storage = Storage()

def NewConfig() -> Config:
    return Config()