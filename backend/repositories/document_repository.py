from abc import ABC, abstractmethod
from typing import List

from entities.agent_model import Agent


class DocumentRepository(ABC):
    @abstractmethod
    def create_collection(self):
        """Создает коллекцию документов"""
        pass

    @abstractmethod
    def insert_document(self):
        """Добавляет документ"""
        pass

    @abstractmethod
    def search_similar(self):
        """Ищет похожие документы"""
        pass

    @abstractmethod
    def delete_collection(self):
        """Удаляет коллекцию документов"""
        pass
    
    @abstractmethod
    def close(self):
        """Закрывает соединение"""
        pass
