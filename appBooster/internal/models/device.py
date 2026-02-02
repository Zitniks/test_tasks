from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from internal.db.connection import Base


def _utc_now():
    return datetime.now(timezone.utc)


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, index=True)
    device_token = Column(String, unique=True, nullable=False, index=True)
    first_seen_at = Column(DateTime, default=_utc_now, nullable=False)


class DeviceExperiment(Base):
    __tablename__ = 'device_experiments'

    id = Column(Integer, primary_key=True, index=True)
    device_token = Column(String, nullable=False, index=True)
    experiment_key = Column(String, nullable=False, index=True)
    experiment_value = Column(String, nullable=False)
    created_at = Column(DateTime, default=_utc_now)

    __table_args__ = (
        {'sqlite_autoincrement': True},
    )
