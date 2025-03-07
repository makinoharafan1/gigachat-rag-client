from implements.services.postgres_migrations import PostgresMigrationService

class Services:
    def __init__(self, migration: PostgresMigrationService):
        self.migration = migration