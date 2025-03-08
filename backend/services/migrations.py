from abc import ABC, abstractmethod


class MigrationService(ABC):
    @abstractmethod
    def up(self):
        """Запускает все миграции"""
        pass

    @abstractmethod
    def down_to_base(self):
        """Откатывает все миграции"""
        pass
