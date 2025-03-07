from abc import ABC, abstractmethod

class MigrationService(ABC):
    @abstractmethod
    def Up(self):
        """Запускает все миграции"""
        pass

    @abstractmethod
    def DownToBase(self):
        """Откатывает все миграции"""
        pass