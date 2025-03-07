from utils.config import Config
from services.migrations import MigrationService

from alembic.config import Config as alembicConfig
from alembic import command

class PostgresMigrationService(MigrationService):
    def __init__(self, config: Config):
        connection_url = f"postgresql://{config.storage.dbUser}:{config.storage.dbPassword}@{config.storage.dbHost}:{config.storage.dbPort}/{config.storage.dbName}"
        self.alembic_cfg = alembicConfig("alembic.ini")
        self.alembic_cfg.set_section_option('alembic', 'sqlalchemy.url', connection_url)
    
    def Up(self):
        command.upgrade(self.alembic_cfg, "head")
    
    def DownToBase(self):
        command.downgrade(self.alembic_cfg, "base")
