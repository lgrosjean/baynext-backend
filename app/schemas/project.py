# app/models/project.py

import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .dataset import Dataset
    from .pipeline import Pipeline


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    # user_id: str = Field(foreign_key="users.id")  # Assuming user model exists
    name: str
    description: Optional[str] = None

    # Relationships
    datasets: Optional[list["Dataset"]] = Relationship(back_populates="project")
    pipelines: Optional[list["Pipeline"]] = Relationship(back_populates="project")
