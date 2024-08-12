"""Add triger to updated_at table messages

Revision ID: 409671164c5d
Revises: b91216f49c9d
Create Date: 2024-08-12 10:53:59.239658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '409671164c5d'
down_revision: Union[str, None] = 'b91216f49c9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Список таблиц, в которых необходимо обновлять updated_at
tables_with_updated_at = [
    "messages",
]


def upgrade() -> None:
    # Создаем триггер для каждой таблицы из списка
    for table in tables_with_updated_at:
        op.execute(
            f"""
            CREATE TRIGGER IF NOT EXISTS update_{table}_updated_at
            AFTER UPDATE ON {table}
            FOR EACH ROW
            BEGIN
                UPDATE {table}
                SET updated_at = datetime('now')
                WHERE rowid = OLD.rowid;
            END;
            """
        )


def downgrade() -> None:
    # Удаляем триггеры для каждой таблицы из списка
    for table in tables_with_updated_at:
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_updated_at;")