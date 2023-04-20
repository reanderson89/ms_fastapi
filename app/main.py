import uvicorn

from app.configs import run_config
from fastapi import FastAPI
from app.routers import routers

app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     app.state.db = session()

# @app.on_event("shutdown")
# async def shutdown():
#     app.state.db.close()

app.include_router(routers, prefix="/v1")

if __name__ == "__main__":
	uvicorn.run(
		"app:app",
		**run_config.__dict__
	)
