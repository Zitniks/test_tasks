"""Run Alembic migrations on startup."""

import logging
import os

from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError

from configs.settings import settings

logger = logging.getLogger(__name__)


def run_migrations():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_ini_path = os.path.join(base_dir, 'migrations', 'alembic.ini')
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option('sqlalchemy.url', settings.database_url)
    try:
        command.upgrade(alembic_cfg, 'head')
    except (CommandError, FileNotFoundError) as e:
        logger.warning('Alembic migration failed (%s), falling back to create_all', e)
        from internal.db.connection import Base, engine
        Base.metadata.create_all(bind=engine)


def create_initial_migration():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_ini_path = os.path.join(base_dir, 'migrations', 'alembic.ini')
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option('sqlalchemy.url', settings.database_url)
    try:
        command.revision(alembic_cfg, autogenerate=True, message='Initial migration')
    except (CommandError, FileNotFoundError):
        pass
