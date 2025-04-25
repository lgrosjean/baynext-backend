import logging
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .logging import logger
from .models import RunFormData
from .tasks import load, prepare, save, train


class JobStatus(StrEnum):
    """
    Enum for job status.
    """

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class BaseJob(BaseModel):
    """
    Base job model for the `run_model` endpoint.
    """

    job_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)


class JobCreated(BaseJob):
    """
    JobCreated model for the `run_model` endpoint.
    """


class Job(BaseJob):
    """
    RunResponse model for the `run_model` endpoint.
    """

    started_at: datetime | None = None
    ended_at: datetime | None = None
    status: JobStatus = JobStatus.CREATED
    error_message: str | None = None

    @property
    def logger(self) -> logging.Logger:
        """
        Get the logger for the job.
        """
        return logger.getChild(f"job_{self.job_id}")

    def end(self) -> None:
        """
        Mark the job as ended.
        """
        self.ended_at = datetime.now()

    def running(self) -> None:
        """
        Mark the job as running.
        """
        self.started_at = datetime.now()
        self.status = JobStatus.RUNNING
        self.logger.info("Job %s started at %s", self.job_id, datetime.now())

    def completed(self) -> None:
        """
        Mark the job as completed.
        """
        self.end()
        self.status = JobStatus.COMPLETED
        self.logger.info(
            "Job %s completed at %s. Duration: %s",
            self.job_id,
            self.ended_at,
            (self.ended_at - self.started_at).total_seconds(),
        )

    def failed(self, error: Exception) -> None:
        """
        Mark the job as failed.
        """
        self.end()
        self.status = JobStatus.FAILED
        self.error_message = str(error)
        self.logger.error(
            "Job %s failed at %s with error: %s",
            self.job_id,
            self.ended_at,
            error,
        )
        raise error

    def run(self, data: RunFormData) -> None:
        """
        Run the model with the given data.
        """

        input_data = load(
            csv_path=data.csv_path,
            kpi_type=data.kpi_type,
            time=data.time,
            kpi=data.kpi,
            controls=data.controls,
            geo=data.geo,
            population=data.population,
            revenue_per_kpi=data.revenue_per_kpi,
            media=data.media,
            media_spend=data.media_spend,
            organic_media=data.organic_media,
            non_media_treatments=data.non_media_treatments,
            # media_to_channel=MEDIA_TO_CHANNEL,
            # media_spend_to_channel=MEDIA_SPEND_TO_CHANNEL,
        )

        model_spec = prepare(
            roi_mu=data.roi_mu,
            roi_sigma=data.roi_sigma,
            max_lag=data.max_lag,
        )

        try:
            self.running()

            meridian = train(
                input_data=input_data,
                model_spec=model_spec,
                n_draws=data.n_draws,
                n_chains=data.n_chains,
                n_adapt=data.n_adapt,
                n_burnin=data.n_burnin,
                n_keep=data.n_keep,
            )

            self.completed()

            file_path = (
                f"./meridian_model_{self.ended_at.strftime('%Y%m%d_%H%M%S')}.mmm"
            )

            save(meridian, file_path)

        except Exception as exc:
            self.failed(exc)
