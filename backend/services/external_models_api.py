from abc import ABC, abstractmethod
from typing import List


class ExternalModelsAPIService(ABC):
    @abstractmethod
    def get_model_list(self) -> List[str]:
        """Получает список моделей"""
        pass
