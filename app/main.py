import asyncio
from contextlib import asynccontextmanager
from threading import Thread

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi_pagination import add_pagination

from app.configs import run_config
from app.worker.queue_worker import QueueWorker
from app.middleware import LoggingMiddleware
from app.api_routes import cron_routers, api_router


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
    
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
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
