from alembic import command
from alembic.config import Config

from internal.db.connection import engine


def run_migrations():
    alembic_cfg = Config('migrations/alembic.ini')
    command.upgrade(alembic_cfg, 'head')


def create_initial_migration():
    alembic_cfg = Config('migrations/alembic.ini')
    try:
        command.revision(alembic_cfg, autogenerate=True, message='Initial migration')
    except Exception:
        pass
