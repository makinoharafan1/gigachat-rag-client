from abc import ABC, abstractmethod
from typing import List

from entities.agent import Agent


class AgentRepo(ABC):

    @abstractmethod
    def get_base_info_by_filters(self, page: int, limit: int) -> List[Agent]:
        """Выдаёт список агентов удовлетворяющих фильтрам"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Agent:
        """Выдаёт агента по id"""
        pass

    @abstractmethod
    def create(self, agent: Agent) -> int:
        """Создаёт нового агента"""
        pass

    @abstractmethod
    def update(self, id: int, agent: Agent):
        """Обновляет данные агента по id"""
        pass

    @abstractmethod
    def delete(self, id: int):
        """Удаляет агента по id"""
        pass
