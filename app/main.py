import asyncio
import os
from contextlib import asynccontextmanager
from threading import Thread

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi_pagination import add_pagination

from app.configs import run_config
from app.configs.queue_configs import QueueWorker
from app.middleware import LoggingMiddleware
from app.routers import admin_routers, auth_routers, cron_routers, routers
from app.seed_data import seed_database


async def run_worker():
    """ start the worker coroutine """
    queue_worker = QueueWorker()
    await queue_worker.worker()


def start_worker_thread():
    """ start the worker thread """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_worker())
    loop.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ start the worker thread when the app starts """
    worker_thread = Thread(target=start_worker_thread, daemon=True)
    worker_thread.start()

    bootstrap_envs = ["LOCAL", "DEV"]
    env = os.getenv("ENV", "LOCAL").upper()
    if env in bootstrap_envs:
        """
        try/except was added because when the container would reload when a change was made,
        it would error out on the fact that the users already existed.
        """
        try:
            await seed_database()
            yield
        except:
            yield
    else:
        yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(HTTPException, LoggingMiddleware.http_exception_handler)
app.add_exception_handler(RequestValidationError, LoggingMiddleware.validation_exception_handler)
app.include_router(routers, prefix="/v1")
app.include_router(auth_routers, prefix="/v1")
app.include_router(admin_routers, prefix="/v1")
app.include_router(cron_routers, prefix="/blue")

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        **run_config.__dict__
    )
