import os

from fastapi import FastAPI

from .api.v1 import router as v1_router
from .core.security import check_token
from .core.settings import settings
from .routes import router

app = FastAPI(
    title=settings.app_name,
    redoc_url=None,
    docs_url="/docs" if not os.getenv("RENDER") else None,
)

app.include_router(router)
app.include_router(v1_router)
