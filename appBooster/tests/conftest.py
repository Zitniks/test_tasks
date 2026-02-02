"""Pytest fixtures for API tests."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cmd.server.main import app
from internal.db.connection import Base, get_db
from internal.models.experiment import Experiment, ExperimentOption

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _seed_test_experiments(session):
    """Insert initial experiments and options for tests."""
    for key, options in [
        ("button_color", [("#FF0000", 33), ("#00FF00", 33), ("#0000FF", 34)]),
        ("price", [("10", 75), ("20", 10), ("50", 5), ("5", 10)]),
    ]:
        if session.query(Experiment).filter(Experiment.key == key).first():
            continue
        exp = Experiment(key=key)
        session.add(exp)
        session.commit()
        session.refresh(exp)
        for value, weight in options:
            session.add(ExperimentOption(experiment_key=key, value=value, weight=weight))
        session.commit()


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    _seed_test_experiments(db_session)
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
