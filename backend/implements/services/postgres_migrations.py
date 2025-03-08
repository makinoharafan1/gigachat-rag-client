from alembic.config import Config as AlembicConfig
from alembic import command

from utils.config import AppConfig
from services.migrations import MigrationService


class PostgresMigrationService(MigrationService):
    def __init__(self, config: AppConfig):
        connection_url = f"postgresql://{config.postgres_db_username}:{config.postgres_db_password}@db:{config.postgres_db_port}/{config.postgres_db_name}"
        self.alembic_cfg = AlembicConfig("alembic.ini")
        self.alembic_cfg.set_section_option('alembic', 'sqlalchemy.url', connection_url)
    
    def up(self):
        command.upgrade(self.alembic_cfg, "head")
    
    def down_to_base(self):
        command.downgrade(self.alembic_cfg, "base")
