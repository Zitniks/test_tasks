import datetime

from sqlalchemy import Column, DateTime, Integer, String

from internal.db.connection import Base


class ShortUrl(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False, index=True)
    short_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
