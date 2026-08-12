from fastapi import Header, HTTPException

from app.config.settings import settings


def validate_api_key(x_api_key: str | None = Header(default=None)):
    if not settings.API_KEY:
        return True

    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return True
