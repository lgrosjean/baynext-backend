import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import check_token
from app.core.settings import settings


@pytest.mark.asyncio
async def test_check_token_valid():
    # Mock the secret API key
    settings.ml_api_secret_api_key.get_secret_value = lambda: "valid_api_key"

    # Create a mock HTTPAuthorizationCredentials object with a valid token
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="valid_api_key"
    )

    # Call the function and ensure no exception is raised
    try:
        await check_token(credentials)
    except HTTPException:
        pytest.fail("check_token raised HTTPException unexpectedly!")


@pytest.mark.asyncio
async def test_check_token_invalid():
    # Mock the secret API key
    settings.ml_api_secret_api_key.get_secret_value = lambda: "valid_api_key"

    # Create a mock HTTPAuthorizationCredentials object with an invalid token
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="invalid_api_key"
    )

    # Call the function and ensure an HTTPException is raised
    with pytest.raises(HTTPException) as exc_info:
        await check_token(credentials)

    # Verify the exception details
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Invalid API key"
