from fastapi import APIRouter

from . import datasets, jobs, pipelines

router = APIRouter(prefix="/v1/projects/{project_id}")

router.include_router(pipelines.router)
router.include_router(datasets.router)
router.include_router(jobs.router)
