from sqlalchemy.orm import Session

from internal.models.short_url import ShortUrl
from pkg.utils.url import generate_short_code


def create_short_url(db: Session, original_url: str, custom_code: str | None = None) -> ShortUrl:
    if custom_code:
        short_code = custom_code
    else:
        short_code = generate_short_code()
        while db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first():
            short_code = generate_short_code()

    short_url = ShortUrl(original_url=original_url, short_code=short_code)
    db.add(short_url)
    db.commit()
    db.refresh(short_url)
    return short_url


def get_short_url_by_code(db: Session, short_code: str) -> ShortUrl | None:
    return db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
