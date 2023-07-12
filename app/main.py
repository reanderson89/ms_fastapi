import uvicorn
import os
from app.actions.base_actions import BaseActions
from app.configs import run_config
from app.models.users import UserModel, UserServiceModelDB
from app.routers import routers
from app.middleware import LoggingMiddleware
from app.routers import auth_routers
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from contextlib import asynccontextmanager
from fastapi_pagination import add_pagination
from app.seed_data.seed_data import generate_seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
	bootstrap_envs = ["LOCAL", "DEV"]
	env = os.getenv("ENV", "LOCAL").upper()
	if env in bootstrap_envs:
		"""
		try/except was added because when the container would reload when a change was made,
		it would error out on the fact that the users already existed.
		"""
		try:
			await BaseActions.seed_database(generate_seed_data())
			yield
		except:
			yield



app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(HTTPException, LoggingMiddleware.http_exception_handler)
app.add_exception_handler(RequestValidationError, LoggingMiddleware.validation_exception_handler)
app.include_router(routers, prefix="/v1")
app.include_router(auth_routers, prefix="/v1")

add_pagination(app)

if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		**run_config.__dict__
	)
