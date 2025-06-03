from fastapi import APIRouter

from . import health  # , run

router = APIRouter()

router.include_router(health.router)
# router.include_router(run.router)
