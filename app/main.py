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

@app.get("/health")
def read_root():
    return {"message": "milestones is up and making memories, let's GOOOO"}

app.include_router(routers, prefix="/v1")

if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		**run_config.__dict__
	)
