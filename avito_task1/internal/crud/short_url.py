"""CRUD operations for ShortUrl."""

from sqlalchemy.orm import Session

from configs.settings import settings
from internal.models.short_url import ShortUrl
from pkg.utils.url import generate_short_code

MAX_SHORT_CODE_ATTEMPTS = 100


def create_short_url(db: Session, original_url: str, custom_code: str | None = None) -> ShortUrl:
    """Create a ShortUrl; use custom_code if provided, else generate unique code."""
    if custom_code:
        short_code = custom_code
    else:
        length = settings.short_code_length
        for _ in range(MAX_SHORT_CODE_ATTEMPTS):
            short_code = generate_short_code(length=length)
            if not db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first():
                break
        else:
            raise RuntimeError('Could not generate unique short code')

    short_url = ShortUrl(original_url=original_url, short_code=short_code)
    db.add(short_url)
    db.commit()
    db.refresh(short_url)
    return short_url


def get_short_url_by_code(db: Session, short_code: str) -> ShortUrl | None:
    """Return ShortUrl by short_code or None if not found."""
    return db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
