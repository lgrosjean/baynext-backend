# from typing import Annotated, Optional

# from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
# from pydantic import BaseModel
# from sqlalchemy.orm import Session

# from app.db import get_session
# from models.datasets import Dataset as DatasetDB
# from models.models import Model as ModelDB
# from validations.datasets import Dataset
# from validations.models import Model

# router = APIRouter(tags=["Run"])


# class ModelAndDatasetBody(BaseModel):
#     model: Model
#     dataset: Dataset


# @router.post(
#     "/{project_id}/runs",
#     status_code=status.HTTP_201_CREATED,
# )
# async def run_training_endpoint(
#     project_id: Annotated[str, Path(title="The ID of the project to get")],
#     # dataset_id: Optional[str] = Query(None, description="Existing dataset ID"),
#     # model_id: Optional[str] = Query(None, description="Existing model ID"),
#     data: Optional[ModelAndDatasetBody],
#     n_draws: Optional[int] = Query(
#         1000,
#         ge=1,
#         le=10000,
#         description="Number of draws to run",
#     ),
#     n_chains: int | None = Query(
#         4,
#         ge=1,
#         le=10,
#         description="Number of chains to run",
#     ),
#     n_burnin: Optional[int] = Query(
#         1000,
#         ge=0,
#         le=10000,
#         description="Number of burn-in iterations",
#     ),
#     n_adapt: Optional[int] = Query(
#         1000,
#         ge=0,
#         le=10000,
#         description="Number of adaptation iterations",
#     ),
#     n_keep: Optional[int] = Query(
#         1000,
#         ge=1,
#         le=10000,
#         description="Number of iterations to keep",
#     ),
#     session: Session = Depends(get_session),
# ):
#     """
#     Run the Meridian model with the given parameters.
#     """
#     print(project_id)

#     # --- Handle Model ---
#     # if model_id:
#     #     model = session.get(ModelDB, model_id)
#     #     if model is None:
#     #         raise HTTPException(status_code=404, detail="Model not found")
#     if data and data.model:
#         model = data.model
#     else:
#         raise HTTPException(status_code=400, detail="You must provide model body")

#     # # --- Handle Dataset ---
#     # if dataset_id:
#     #     dataset = session.get(DatasetDB, dataset_id)
#     #     if dataset is None:
#     #         raise HTTPException(status_code=404, detail="Dataset not found")
#     if data and data.dataset:
#         dataset = data.dataset
#     else:
#         raise HTTPException(status_code=400, detail="You must provide dataset body")

#     print(model)
#     print(dataset)
