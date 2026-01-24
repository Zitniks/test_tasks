from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from api.schemas.short_url import ShortUrlCreate, ShortUrlResponse
from configs.settings import settings
from internal.crud.short_url import create_short_url, get_short_url_by_code
from internal.db.connection import get_db
from internal.db.migrations import run_migrations
from pkg.utils.url import validate_short_code, validate_url

app = FastAPI(title='URL Shortener', version='1.0.0')


@app.on_event('startup')
def startup():
    run_migrations()


@app.post('/api/v1/shorten', response_model=ShortUrlResponse, status_code=status.HTTP_201_CREATED)
def create_short(url_data: ShortUrlCreate, db: Session = Depends(get_db)):
    if not validate_url(url_data.original_url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid or inaccessible URL')

    if url_data.custom_code:
        if not validate_short_code(url_data.custom_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid custom code format. Use 3-50 alphanumeric characters, hyphens, or underscores',
            )

        existing = get_short_url_by_code(db, url_data.custom_code)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Custom code already exists')

    short_url_obj = create_short_url(db, url_data.original_url, url_data.custom_code)

    return ShortUrlResponse(
        short_url=f'{settings.base_url}/{short_url_obj.short_code}',
        original_url=short_url_obj.original_url,
        short_code=short_url_obj.short_code,
    )


@app.get('/{short_code}')
def redirect(short_code: str, db: Session = Depends(get_db)):
    short_url = get_short_url_by_code(db, short_code)
    if not short_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Short URL not found')

    return RedirectResponse(url=short_url.original_url, status_code=status.HTTP_302_FOUND)


@app.get('/api/v1/health')
def health():
    return {'status': 'ok'}
