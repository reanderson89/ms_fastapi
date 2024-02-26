import asyncio
import os
from contextlib import asynccontextmanager
from enum import Enum

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi_pagination import add_pagination

from app.api_routes import api_router, cron_routers
from app.configs import run_config
from app.middleware import LoggingMiddleware
from app.worker.queue_worker import QueueWorker
from app.worker.cron_worker import CronWorker


class WorkerType(str, Enum):
    QUEUE_WORKER = "queue_worker"
    CRON_WORKER = "cron_worker"


async def run_worker(worker_type: WorkerType):
    """ start the worker coroutine """
    if worker_type == WorkerType.QUEUE_WORKER:
        queue_worker = QueueWorker()
        await queue_worker.worker()
    elif worker_type == WorkerType.CRON_WORKER:
        cron_worker = CronWorker()
        await cron_worker.worker()
    else:
        raise ValueError(f"Unknown worker type: {worker_type}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ start the worker tasks when the app starts """
    worker_task = asyncio.create_task(run_worker(WorkerType.QUEUE_WORKER))
    cron_task = asyncio.create_task(run_worker(WorkerType.CRON_WORKER))

    try:
        yield
    finally:
        worker_task.cancel()
        cron_task.cancel()
        try:
            await worker_task
            await cron_task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
# added for local devlopment for mario
if os.environ.get("ENV") == "local":
    from fastapi.middleware.cors import CORSMiddleware

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
app.add_exception_handler(HTTPException, LoggingMiddleware.http_exception_handler)
app.add_exception_handler(RequestValidationError, LoggingMiddleware.validation_exception_handler)
app.include_router(api_router, prefix="/v1")
app.include_router(cron_routers, prefix="/blue")

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        **run_config.__dict__
    )
