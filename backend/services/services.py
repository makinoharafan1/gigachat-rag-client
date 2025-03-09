from services.migrations import MigrationService
from services.external_models_api import ExternalModelsAPIService



class Services:
    def __init__(self, 
                 migration: MigrationService,
                 external_models_api: ExternalModelsAPIService
                 ):
        self.migration = migration
        self.external_models_api = external_models_api
