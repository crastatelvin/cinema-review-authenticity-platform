from fastapi import Header, HTTPException


VALID_API_KEYS = {"dev-key"}


def require_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
