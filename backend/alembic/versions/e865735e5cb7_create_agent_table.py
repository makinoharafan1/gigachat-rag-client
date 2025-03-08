"""create_agent_table

Revision ID: e865735e5cb7
Revises: d32468fbd56c
Create Date: 2025-03-08 13:02:34.884101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e865735e5cb7'
down_revision: Union[str, None] = 'd32468fbd56c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS users;

    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        title VARCHAR(64) NOT NULL UNIQUE,
        logo VARCHAR(255) NOT NULL,
        system_prompt VARCHAR(500) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS agents;")
