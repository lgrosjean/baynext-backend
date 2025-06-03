# app/schemas/pipeline_schemas.py
# Inspiration: https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.trainingPipelines

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from .model_spec import ModelSpec


class PipelineCreate(BaseModel):
    dataset_id: str = Field(examples=[str(uuid4())])
    model_spec: ModelSpec

    @field_validator("dataset_id")
    @classmethod
    def validate_dataset_id(cls, v):
        try:
            UUID(v)
        except ValueError as exc:
            raise ValueError("dataset_id must be a valid UUID") from exc
        return v


class PipelinePublic(BaseModel):
    id: UUID
    created_at: datetime


class PipelineDetails(PipelinePublic):
    dataset_id: str
    model_spec: ModelSpec
