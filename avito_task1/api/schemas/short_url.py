"""Pydantic schemas for URL Shortener API."""

from pydantic import BaseModel, Field

MAX_ORIGINAL_URL_LENGTH = 4096


class ShortUrlCreate(BaseModel):
    original_url: str = Field(..., max_length=MAX_ORIGINAL_URL_LENGTH)
    custom_code: str | None = Field(None, min_length=3, max_length=50)


class ShortUrlResponse(BaseModel):
    short_url: str
    original_url: str
    short_code: str

    model_config = {'from_attributes': True}
