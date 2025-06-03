from datetime import datetime

from pydantic import BaseModel

from .enums import JobStatus as JobStatusAttr
from .job_parameters import JobParams
from .model import ModelPublic


class JobBase(BaseModel):
    pass
    # id: str | None


class JobCreate(JobBase):
    pipeline_id: str
    params: JobParams


class JobCreated(JobBase):
    id: str
    started_at: datetime


class JobStatus(JobBase):
    id: str
    started_at: datetime
    status: JobStatusAttr

    model: ModelPublic | None = None
