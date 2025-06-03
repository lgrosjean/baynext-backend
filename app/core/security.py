from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.settings import settings


async def check_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Security(
            HTTPBearer(
                description="Basic HTTP Bearer Authentication.",
            )
        ),
    ],
) -> None:
    # Simulate a database query to find a known token
    if credentials.credentials != settings.ml_api_secret_api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
