# app/models/dataset.py

from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, HttpUrl
from sqlmodel import ARRAY, JSON, AutoString, Field, SQLModel, String


class DatasetPublic(SQLModel):
    """
    Public dataset schema for API responses.
    """

    id: UUID4
    project_id: str
    name: str
    file_url: HttpUrl = Field(sa_type=AutoString)

    uploaded_at: datetime


class DatasetDetailsPublic(DatasetPublic):
    """
    Public dataset schema for detailed API responses.
    """

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
