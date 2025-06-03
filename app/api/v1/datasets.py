from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_session
from app.services import DatasetService
from app.validations.datasets import DatasetDetailsPublic, DatasetPublic

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.get("", response_model=list[DatasetPublic])
async def list_datasets(
    project_id: str = Path(...),
    session: AsyncSession = Depends(get_session),
):
    """
    List all datasets for a project.
    """
    service = DatasetService(session, project_id)
    return service.list()


@router.get("/{dataset_id}", response_model=DatasetDetailsPublic)
async def get_dataset(
    project_id: str = Path(...),
    dataset_id: str = Path(...),
    session: AsyncSession = Depends(get_session),
):
    """
    Get a dataset by ID.
    """
    service = DatasetService(session, project_id)
    dataset = service.get(dataset_id)

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if dataset.project_id != project_id:
        raise HTTPException(status_code=403, detail="Access forbidden to this dataset")

    return dataset
