# https://neon.tech/guides/drizzle-local-vercel
import typing as t
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session

from app.core.db import get_session
from app.services.pipeline import PipelineService
from app.validations.pipeline import PipelineCreate, PipelineDetails, PipelinePublic

router = APIRouter(prefix="/pipelines", tags=["Pipelines"])

ProjectId = t.Annotated[
    str, Path(description="The project Id", example=f"{str(uuid4())}")
]
PipelineId = t.Annotated[
    str, Path(description="The pipeline Id", example=f"{str(uuid4())}")
]


@router.post("", response_model=PipelinePublic)
async def create_pipeline(
    project_id: ProjectId,
    pipeline_data: PipelineCreate,
    session: Session = Depends(get_session),
):
    """Create a new pipeline"""
    try:
        service = PipelineService(session, project_id)
        return service.create(pipeline_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("", response_model=list[PipelinePublic])
async def list_pipelines(
    project_id: ProjectId,
    session: Session = Depends(get_session),
):
    """List all pipelines for a project"""
    service = PipelineService(session, project_id)
    return service.list()


@router.delete("/{pipeline_id}", status_code=204)
async def delete_pipeline(
    project_id: ProjectId,
    pipeline_id: PipelineId,
    session: Session = Depends(get_session),
):
    """Delete a pipeline by ID"""
    service = PipelineService(session, project_id)
    pipeline = service.get(pipeline_id)

    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    if pipeline.project_id != project_id:
        raise HTTPException(status_code=403, detail="Access forbidden to this pipeline")

    service.delete(pipeline)
    return None  # 204 No Content


@router.get(
    "/{pipeline_id}",
    response_model=PipelineDetails,
    response_model_exclude_unset=True,
)
async def get_pipeline(
    project_id: ProjectId,
    pipeline_id: PipelineId,
    session: Session = Depends(get_session),
):
    """Get a pipeline by ID"""
    service = PipelineService(session, project_id)
    pipeline = service.get(pipeline_id)

    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    if pipeline.project_id != project_id:
        raise HTTPException(status_code=403, detail="Access forbidden to this pipeline")

    return pipeline
