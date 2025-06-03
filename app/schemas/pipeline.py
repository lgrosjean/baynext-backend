import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import field_validator
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel

from ..validations.model_spec import ModelSpec
from .dataset import Dataset
from .project import Project

if TYPE_CHECKING:
    from .job import Job  # Avoid circular import


class Pipeline(SQLModel, table=True):
    __tablename__ = "pipelines"

    id: str | None = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    project_id: str = Field(foreign_key="projects.id")
    dataset_id: str = Field(foreign_key="datasets.id")

    model_spec: ModelSpec = Field(sa_column=Column(JSONB))

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    project: Optional["Project"] = Relationship(back_populates="pipelines")
    dataset: Optional["Dataset"] = Relationship(back_populates="pipelines")
    jobs: Optional[list["Job"]] = Relationship(back_populates="pipeline")

    @field_validator("model_spec")
    def val_model_spec(
        cls, val
    ):  # pylint: disable=no-self-argument,missing-function-docstring
        return val.dict()
