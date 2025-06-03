from app.schemas import Job
from app.services.base import BaseService
from app.validations.job import JobCreate, JobCreated


class JobService(BaseService, model_class=Job):
    """
    Service class for managing jobs.
    """

    def create(self, model: JobCreate) -> JobCreated:
        """Create a new job"""
        return super().create(model)
