import config
from fastapi import FastAPI
from database.config import SessionLocal
from src.app_routers import router as app_routers

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = SessionLocal()

@app.on_event("shutdown")
async def shutdown():
    app.state.db.close()

app.include_router(app_routers, prefix="/v1")

if __name__ == "__main__":
	import uvicorn
	port = config.PORT
	# Note: workers are not set when reload is enabled
	uvicorn.run(
		"app:app",
		host="127.0.0.1", # i.e. localhost
		port=port,
		reload=True
		# workers=4,
	)
