"""ShortUrl model for URL Shortener."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from internal.db.connection import Base


def _utc_now():
    return datetime.now(timezone.utc)


class ShortUrl(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False, index=True)
    short_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=_utc_now)
