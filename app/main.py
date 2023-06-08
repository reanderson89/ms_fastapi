import uvicorn
from app.configs import run_config
from app.routers import routers, auth_routers
from app.middleware import ExceptionHandlingMiddleware
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException


app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     app.state.db = session()

# @app.on_event("shutdown")
# async def shutdown():
#     app.state.db.close()

app.add_middleware(ExceptionHandlingMiddleware)
app.add_exception_handler(HTTPException, ExceptionHandlingMiddleware.http_exception_handler)
app.add_exception_handler(RequestValidationError, ExceptionHandlingMiddleware.validation_exception_handler)
app.include_router(routers, prefix="/v1")
app.include_router(auth_routers, prefix="/v1")

if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		**run_config.__dict__
	)
