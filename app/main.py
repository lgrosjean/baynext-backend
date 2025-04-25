# Sources:
# - https://github.com/astral-sh/uv-fastapi-example/blob/main/app/main.py
# - https://developers.google.com/meridian/notebook/meridian-getting-started
# - https://fastapi.tiangolo.com/tutorial/background-tasks/#using-backgroundtasks

import typing as t

from fastapi import Body, Depends, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from app import settings

from .job import Job, JobCreated
from .logging import logger
from .models import RunParams
from .security import check_token
from .settings import settings

app = FastAPI(
    title=settings.app_name,
    root_path=settings.root_path,
    redoc_url=None,
)


# https://fastapi.tiangolo.com/tutorial/handling-errors/?h=error#override-request-validation-exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.info(exc)
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}


# @app.get("/status/{job_id}", response_model=Job)
# def get_job_status(job_id: UUID) -> Job:
#     return Job(job_id=job_id, status=JobStatus.CREATED)


@app.post(
    "/run",
    status_code=status.HTTP_201_CREATED,
    # See: https://github.com/fastapi/fastapi/discussions/8741#discussioncomment-7209880
    # https://fastapi.tiangolo.com/tutorial/request-forms/#define-form-parameters
    # openapi_extra={
    #     "requestBody": {
    #         "content": {
    #             "multipart/form-data": {
    #                 "encoding": {
    #                     "controls": {
    #                         "style": "form",
    #                         "explode": True,
    #                     },
    #                     "media": {
    #                         "style": "form",
    #                         "explode": True,
    #                     },
    #                     "media_spend": {
    #                         "style": "form",
    #                         "explode": True,
    #                     },
    #                     "organic_media": {
    #                         "style": "form",
    #                         "explode": True,
    #                     },
    #                     "non_media_treatments": {
    #                         "style": "form",
    #                         "explode": True,
    #                     },
    #                 },
    #             },
    #         },
    #     },
    # },
)
async def run_model_endpoint(
    params: t.Annotated[RunParams, Body()],
    # background_tasks: BackgroundTasks,
    _: t.Annotated[None, Depends(check_token)],
) -> JobCreated:
    """
    Run the Meridian model with the given parameters.

    Source: [https://developers.google.com/meridian/docs/user-guide/run-model](https://developers.google.com/meridian/docs/user-guide/run-model)
    """
    job = Job()
    print(params)
    return job

    # try:
    #     job = Job()
    #     # background_tasks.add_task(job.run, data)
    #     return job
    # except Exception as exc:
    #     print(type(exc))
    #     print(exc)
    #     raise HTTPException(
    #         status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=jsonable_encoder(exc),
    #     ) from exc
