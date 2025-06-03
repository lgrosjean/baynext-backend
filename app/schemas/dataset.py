# app/models/dataset.py

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import HttpUrl
from sqlmodel import ARRAY, JSON, AutoString, Field, Relationship, SQLModel, String


class Dataset(SQLModel, table=True):
    __tablename__ = "datasets"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    project_id: str = Field(foreign_key="projects.id")  # FK to projects

    name: str
    file_url: HttpUrl = Field(sa_type=AutoString)

    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    geo: Optional[str] = None
    time: str
    kpi: str

    kpi_type: Optional[str] = None  # If you have enum later, can tighten

    population: Optional[str] = None
    revenue_per_kpi: Optional[str] = None

    # Array fields
    controls: Optional[List[str]] = Field(default=None, sa_type=ARRAY(String))
    medias: Optional[List[str]] = Field(default=None, sa_type=ARRAY(String))
    media_spend: Optional[List[str]] = Field(default=None, sa_type=ARRAY(String))

    # JSON fields
    media_to_channel: Optional[dict] = Field(default=None, sa_type=JSON)
    media_spend_to_channel: Optional[dict] = Field(default=None, sa_type=JSON)

    # Relationship back to Project
    project: Optional["Project"] = Relationship(back_populates="datasets")
    pipelines: Optional[list["Pipeline"]] = Relationship(back_populates="dataset")
