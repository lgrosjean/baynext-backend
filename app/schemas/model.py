# app/models/model.py

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .job import Job  # Avoid circular import


class ModelBase(SQLModel):
    pass


class Model(SQLModel, table=True):
    __tablename__ = "models"

    # Attributes
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    job_id: str = Field(foreign_key="jobs.id")
    uri: str  # blob storage URI

    deployed: bool | None = Field(default=False)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)

    # Relationships
    job: Job = Relationship(
        back_populates="model",
        # sa_relationship_kwargs={
        #     "foreign_keys": "[Model.job_id]",
        # },
    )


class ModelCreate(ModelBase):
    pass


class ModelPublic(ModelBase):
    id: str
    created_at: datetime
    deployed: bool
