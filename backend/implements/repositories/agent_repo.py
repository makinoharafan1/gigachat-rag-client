import math
from typing import List

from psycopg2.pool import AbstractConnectionPool

from entities.agent import Agent
from repositories.agent import AgentRepo


class PostgresAgentRepo(AgentRepo):
    def __init__(self, pool: AbstractConnectionPool):
        self.pool = pool
    
    def get_by_id(self, id: int) -> Agent:
        
        connection = self.pool.getconn()
        cursor = connection.cursor()

        query = "select * from agents where id=%s;"
        cursor.execute(query, (id,))

        row = cursor.fetchone()
        if row:
            agent = Agent(
                    id=row[0], 
                    title=row[1], 
                    logo=row[2], 
                    system_prompt=row[3], 
                    created_at=row[4],
                    updated_at=row[5],
                )
            return agent

        cursor.close()
        self.pool.putconn(connection)
        
        return None

    def get_base_info_by_filters(self, page: int, limit: int) -> List[Agent]:
        
        connection = self.pool.getconn()
        cursor = connection.cursor()

        limit = max(limit, 1)
        page = max(page, 1)

        query = "select id, title, logo from agents order by created_at DESC LIMIT %s OFFSET %s;"
        cursor.execute(query, (limit, limit * (page - 1),))

        rows = cursor.fetchall()

        result = []
        for row in rows:
            agent = Agent(id=row[0], title=row[1], logo=row[2])
            result.append(agent)

        cursor.close()
        self.pool.putconn(connection)

        return result

    def create(self, agent: Agent) -> int:
        
        connection = self.pool.getconn()
        cursor = connection.cursor()

        query = """
            INSERT INTO agents (title, logo, system_prompt) 
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (agent.title, agent.logo, agent.system_prompt,))

        id = cursor.fetchone()[0]

        connection.commit()

        cursor.close()
        self.pool.putconn(connection)

        return id

    def update(self, id: int, agent: Agent):
        
        connection = self.pool.getconn()
        cursor = connection.cursor()

        query = """
            UPDATE agents
            SET title = %s, logo = %s, system_prompt = %s, updated_at = NOW()
            WHERE id = %s;
        """
        cursor.execute(query, (agent.title, agent.logo, agent.system_prompt, id))

        connection.commit()

        cursor.close()
        self.pool.putconn(connection)

    def delete(self, id: int):
        connection = self.pool.getconn()
        cursor = connection.cursor()

        query = """
            DELETE FROM agents
            WHERE id = %s;
        """
        cursor.execute(query, (id,))

        connection.commit()

        cursor.close()
        self.pool.putconn(connection)