from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from internal.db.connection import Base


def _utc_now():
    return datetime.now(timezone.utc)


class Experiment(Base):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=_utc_now, nullable=False)


class ExperimentOption(Base):
    __tablename__ = 'experiment_options'

    id = Column(Integer, primary_key=True, index=True)
    experiment_key = Column(String, nullable=False, index=True)
    value = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
