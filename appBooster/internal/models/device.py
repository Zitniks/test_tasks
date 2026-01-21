import datetime

from sqlalchemy import Column, DateTime, Integer, String

from internal.db.connection import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, index=True)
    device_token = Column(String, unique=True, nullable=False, index=True)
    first_seen_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class DeviceExperiment(Base):
    __tablename__ = 'device_experiments'

    id = Column(Integer, primary_key=True, index=True)
    device_token = Column(String, nullable=False, index=True)
    experiment_key = Column(String, nullable=False, index=True)
    experiment_value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        {'sqlite_autoincrement': True},
    )
