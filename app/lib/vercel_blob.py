import os
import tempfile
from contextlib import contextmanager
from typing import TypedDict

import httpx

from app.core.logging import logger
from app.core.settings import settings

logger = logger.getChild(__name__)

_VERCEL_BLOB_API_BASE_URL = "https://blob.vercel-storage.com"
_VERCEL_API_VERSION = "7"


class VercelBlobException(Exception):
    """
    Custom exception for Vercel blob storage errors.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class VercelBlobUploadException(VercelBlobException):
    """
    Custom exception for Vercel blob upload errors.
    """


is_not_local = not (os.getenv("RENDER") is None or os.getenv("VERCEL") is None)

Blob = TypedDict(
    "Blob",
    {
        "url": str,
        "pathname": str,
        "size": int,
        "uploadedAt": str,
    },
)


def list(limit: int = 1000) -> list:  # type: ignore
    """
    Lists all blobs in the Vercel blob storage.
    """
    headers = {
        "authorization": f"Bearer {settings.blob_read_write_token.get_secret_value()}",
    }

    params = {
        "limit": str(limit),
    }

    resp = httpx.get(
        _VERCEL_BLOB_API_BASE_URL,
        headers=headers,
        params=params,
        verify=is_not_local,
    )

    if resp.status_code != 200:
        logger.error(f"Failed to list blobs: {resp.text}")
        return []
    res = resp.json()
    blobs = [Blob(**blob) for blob in res.get("blobs", [])]
    return blobs


def head(url: str) -> dict:
    """
    Gets the metadata of the blob object at the specified URL.
    URL can also be the pathname of the blob.
    """
    headers = {
        "authorization": f"Bearer {settings.blob_read_write_token.get_secret_value()}",
        "x-api-version": _VERCEL_API_VERSION,
    }

    resp = httpx.get(
        f"{_VERCEL_BLOB_API_BASE_URL}/?url={url}",
        headers=headers,
        verify=is_not_local,
    )

    if resp.status_code != 200:
        logger.error(f"Failed to get blob metadata: {resp.text}")
        raise Exception(f"Failed to get blob metadata: {resp.text}")

    return resp.json()


@contextmanager
def get(url: str):
    """
    Downloads a file from Vercel blob storage.
    """

    headers = {
        "authorization": f"Bearer {settings.blob_read_write_token.get_secret_value()}",
        "x-api-version": _VERCEL_API_VERSION,
    }

    with tempfile.TemporaryDirectory(prefix="vercel_", dir=".") as tmp_dir:
        blob_head = head(url)

        resp = httpx.get(
            blob_head["downloadUrl"],
            headers=headers,
            verify=is_not_local,
        )

        if resp.status_code != 200:
            logger.error(f"Failed to download blob: {resp.text}")
            raise Exception(f"Failed to download blob: {resp.text}")

        # Save the file to a temporary location
        file_path = os.path.join(tmp_dir, blob_head["pathname"])

        if blob_head.get("contentType") == "text/csv" and not file_path.endswith(
            ".csv"
        ):
            file_path += ".csv"

        with open(file_path, "wb") as f:
            f.write(resp.content)

        yield file_path


def put(
    file,
    pathname: str,
    content_type: str = "application/octet-stream",
    random_suffix: bool = True,
):
    headers = {
        "authorization": f"Bearer {settings.blob_read_write_token.get_secret_value()}",
        "x-api-version": _VERCEL_API_VERSION,
        "x-vercel-blob-public": "true",
        "x-content-type": content_type,
    }

    if random_suffix:
        pathname += f"?{os.urandom(8).hex()}"

    with open(file, "rb") as f:
        resp = httpx.put(
            f"{_VERCEL_BLOB_API_BASE_URL}/{pathname}",
            headers=headers,
            data=f,
            verify=is_not_local,
        )

    if resp.status_code != 200:
        logger.error(f"Failed to upload blob: {resp.text}")
        raise VercelBlobUploadException(f"Failed to upload blob: {resp.text}")

    return resp.json()["url"]
