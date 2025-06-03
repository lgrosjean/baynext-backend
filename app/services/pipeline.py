# app/services/pipeline_service.py

from ..schemas.pipeline import Pipeline
from ..validations.pipeline import PipelineCreate
from .base import BaseService


class PipelineService(BaseService, model_class=Pipeline):
    """
    Service class for managing pipelines.
    """

    def create(self, model: PipelineCreate) -> Pipeline:
        """Create a new pipeline"""

        return super().create(
            {
                "project_id": self.project_id,
                **model.model_dump(mode="json", exclude_none=True),
            }
        )
