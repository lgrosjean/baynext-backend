# app/models/job.py
# Inspiration: https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.pipelineJobs

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel

from app.validations.enums import JobStatus
from app.validations.job_parameters import JobParams

if TYPE_CHECKING:

    from .model import Model
    from .pipeline import Pipeline


class Job(SQLModel, table=True):

    __tablename__ = "jobs"

    # Attributes
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    pipeline_id: str = Field(foreign_key="pipelines.id")
    # model_id: str | None = Field(default=None, foreign_key="models.id")

    status: JobStatus = JobStatus.pending

    params: JobParams = Field(sa_column=Column(JSONB))
    # metrics: dict | None = Field(default=None, sa_column=Column(JSONB))

    started_at: datetime | None = Field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None

    # retries: int = 0
    error: str | None = None

    # Relationships
    pipeline: "Pipeline" = Relationship(back_populates="jobs")
    model: "Model" = Relationship(back_populates="job")

    @field_validator("params")
    def val_model_spec(
        cls, val
    ):  # pylint: disable=no-self-argument,missing-function-docstring
        return val.dict()
