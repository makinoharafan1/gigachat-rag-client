from repositories.agent import AgentRepo


class Repositories:
    def __init__(self, agent: AgentRepo):
        self.agent = agent
