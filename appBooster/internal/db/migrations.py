import os
from alembic import command
from alembic.config import Config


def run_migrations():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_ini_path = os.path.join(base_dir, 'migrations', 'alembic.ini')
    alembic_cfg = Config(alembic_ini_path)
    
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./abtesting.db')
    if not database_url.startswith('sqlite'):
        database_url = 'sqlite:///./abtesting.db'
    
    alembic_cfg.set_main_option('sqlalchemy.url', database_url)
    
    try:
        command.upgrade(alembic_cfg, 'head')
    except Exception:
        from internal.db.connection import Base, engine
        Base.metadata.create_all(bind=engine)
