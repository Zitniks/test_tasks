"""Unit tests for internal.crud.short_url."""

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use SQLite so connection.Base matches test engine
os.environ.setdefault('DATABASE_URL', 'sqlite:///./test_crud.db')

from internal.crud.short_url import create_short_url, get_short_url_by_code
from internal.db.connection import Base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test_crud.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='function')
def db():
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


def test_create_short_url(db):
    short_url = create_short_url(db, 'https://www.example.com')
    assert short_url.original_url == 'https://www.example.com'
    assert short_url.short_code is not None
    assert len(short_url.short_code) == 6


def test_create_short_url_with_custom_code(db):
    short_url = create_short_url(db, 'https://www.example.com', 'custom-code')
    assert short_url.short_code == 'custom-code'


def test_get_short_url_by_code(db):
    short_url = create_short_url(db, 'https://www.example.com', 'test-code')
    found = get_short_url_by_code(db, 'test-code')
    assert found is not None
    assert found.short_code == 'test-code'
    assert found.original_url == 'https://www.example.com'


def test_get_short_url_by_code_not_found(db):
    found = get_short_url_by_code(db, 'nonexistent')
    assert found is None
