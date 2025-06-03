# https://neon.tech/guides/drizzle-local-vercel
import typing as t
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path, status
from sqlmodel import Session

from app.core.db import get_session
from app.services import JobService
from app.tasks import train
from app.validations.job import JobCreate, JobCreated, JobStatus

router = APIRouter(prefix="/jobs", tags=["Jobs"])

ProjectId = t.Annotated[
    str, Path(description="The project Id", example=f"{str(uuid4())}")
]


@router.post("", response_model=JobCreated, status_code=status.HTTP_201_CREATED)
async def create_job(
    # background_tasks: BackgroundTasks,
    project_id: t.Annotated[
        str, Path(description="The project Id", example=f"{str(uuid4())}")
    ],
    job_data: JobCreate,
    background_tasks: BackgroundTasks,
    session: t.Annotated[Session, Depends(get_session)],
):
    service = JobService(session, project_id)
    job = service.create(job_data)

    # ✅ Launch background training
    background_tasks.add_task(train.task, job_id=job.id, session=session)
    # run_training_job(job_id=new_job.id, session=session)

    return job


@router.get(
    "/{job_id}",
    response_model=JobStatus,
    response_model_exclude_unset=True,
)
async def get_job(
    project_id: t.Annotated[
        str, Path(description="The project Id", example=f"{str(uuid4())}")
    ],
    job_id: str,
    session: t.Annotated[Session, Depends(get_session)],
):
    service = JobService(session, project_id)
    job = service.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
