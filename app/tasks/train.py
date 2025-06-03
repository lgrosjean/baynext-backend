# app/tasks/train_model.py

import tempfile
from datetime import datetime

from sqlmodel import Session

from app.core.logging import get_logger
from app.lib.meridian import load, prepare, save, train
from app.lib.vercel_blob import get, put
from app.schemas import Dataset, Job, Pipeline
from app.services import ModelService
from app.validations.enums import JobStatus
from app.validations.job_parameters import JobParams
from app.validations.model_spec import ModelSpec

logger = get_logger(__name__)


def task(job_id: str, session: Session):

    job: Job = session.get(Job, job_id)

    if job is None:
        raise ValueError(f"Job with ID {job_id} not found")

    logger.info("Training parameters: %s", job.params)
    job_params = JobParams(**job.params)

    pipeline: Pipeline = session.get(Pipeline, job.pipeline_id)

    if pipeline is None:
        raise ValueError(f"Pipeline with ID {job.pipeline_id} not found")

    logger.info("Model spec: %s", pipeline.model_spec)
    model_spec = ModelSpec(**pipeline.model_spec)

    dataset: Dataset = session.get(Dataset, pipeline.dataset_id)

    if dataset is None:
        raise ValueError(f"Dataset with ID {pipeline.dataset_id} not found")

    try:
        # Init: Start the job
        job.status = JobStatus.running
        session.add(job)
        session.commit()

        # Step 1: Load the dataset
        with get(dataset.file_url) as file_path:

            input_data = load(
                csv_path=file_path,
                kpi_type=dataset.kpi_type,
                time=dataset.time,
                kpi=dataset.kpi,
                controls=dataset.controls,
                geo=dataset.geo,
                population=dataset.population,
                revenue_per_kpi=dataset.revenue_per_kpi,
                media=dataset.medias,
                media_spend=dataset.media_spend,
                # organic_media=[],  # or from job.params if needed
                # non_media_treatments=[],
                media_to_channel=dataset.media_to_channel,
                media_spend_to_channel=dataset.media_spend_to_channel,
            )

        # Step 2: Prepare the model
        model = prepare(
            roi_mu=2,
            roi_sigma=0.5,
            max_lag=model_spec.max_lag,
        )

        # Step 3: Train model
        meridian_model = train(
            input_data=input_data,
            model_spec=model,
            n_draws=job_params.prior.n_draws,
            n_chains=job_params.posterior.n_chains,
            n_adapt=job_params.posterior.n_adapt,
            n_burnin=job_params.posterior.n_burnin,
            n_keep=job_params.posterior.n_keep,
        )

        # Step 4: Save the model
        with tempfile.NamedTemporaryFile(suffix=".pkl") as tmp_file:
            local_path = tmp_file.name
            save(meridian_model, local_path)

            model_uri = put(
                local_path,
                pathname=f"projects/{pipeline.id}/jobs/{job.id}/model.pkl",
                content_type="application/octet-stream",
            )

        job.status = JobStatus.completed

        model = ModelService(session, pipeline.project_id).create(
            {"job_id": job.id, "uri": model_uri}
        )

        session.add(model)

    except Exception as e:
        logger.error("Error during training job: %s: %s", job_id, str(e))
        job.status = JobStatus.failed
        job.error = str(e)

    finally:
        job.finished_at = datetime.utcnow()
        session.add(job)
        session.commit()
