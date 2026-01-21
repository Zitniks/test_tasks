from pydantic import BaseModel, Field


class ShortUrlCreate(BaseModel):
    original_url: str = Field(..., description='Original URL to shorten')
    custom_code: str | None = Field(None, description='Custom short code (optional)', max_length=50, min_length=3)


class ShortUrlResponse(BaseModel):
    short_url: str
    original_url: str
    short_code: str

    class Config:
        from_attributes = True
