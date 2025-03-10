from repositories.agent_repository import AgentRepository
from repositories.document_repository import DocumentRepository


class Repositories:
    def __init__(self, agent: AgentRepository, document: DocumentRepository):
        self.agent = agent
        self.document = document
