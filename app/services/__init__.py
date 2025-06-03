from ..schemas import Dataset, Model
from .base import BaseService, make_service
from .job import JobService
from .pipeline import PipelineService

DatasetService = make_service(Dataset)
ModelService = make_service(Model)
