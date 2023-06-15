import sys, traceback, logging
from datetime import datetime, timezone
from app.configs import run_config
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import (
	http_exception_handler as _http_exception_handler, 
    request_validation_exception_handler as _request_validation_exception_handler
)
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
	logger = logging.getLogger("uvicorn")
	logger.setLevel(run_config.log_level)
	logger.info(f"Current log level: {logger.level}.")

	@classmethod
	async def dispatch(cls, request:Request, call_next: RequestResponseEndpoint) -> Response:
		try:
			return await call_next(request)
		except Exception as ex:
			if ex is HTTPException:
				return await cls.http_exception_handler(request, ex) 
			elif ex is RequestValidationError:
				return await cls.validation_exception_handler(request, ex)
			return await cls.unhandled_exception_handler(request, ex)			

	@staticmethod
	async def logger_details(request, exc):
		headers = dict(request.headers)
		if 'authorization' in headers:
			del headers['authorization']
		if isinstance(exc,RequestValidationError):
			return {"errors": exc.errors(), "method": request.method, "port": request.url.port, "url": request.url.path, "headers":headers, "client": request.client, "query_params": request.query_params._dict, "cookies": request.cookies}
		return {"method": request.method, "port": request.url.port, "url": request.url.path, "headers":headers, "client": request.client, "query_params": request.query_params._dict, "cookies": request.cookies}

	@classmethod
	async def http_exception_handler(cls, request, exc):
		cls.logger.error(exc.__dict__)
		return await _http_exception_handler(request, exc)

	@classmethod
	async def validation_exception_handler(cls, request, exc):
		detail = await cls.logger_details(request, exc)
		detail['errors'][0]['ctx']['doc'] = exc.__dict__['body'].replace('\n', '').replace('\t','').replace("\"", "'")
		cls.logger.error(detail)
		return await _request_validation_exception_handler(request, exc)

	@classmethod
	async def unhandled_exception_handler(cls, request, exc) -> JSONResponse:
		exception_type, exception_value, _ = sys.exc_info()
		exception_name = getattr(exception_type, "__name__", None)
		detail = await cls.logger_details(request, exc)
		exception_vals = {}
		for k, v in exc.__dict__.items():
			if k != "orig":
				exception_vals[k] = v
			else:
				exception_vals['orig'] = {
					'OperationalError code': exc.orig.args[0],
					'OperationalError message': exc.orig.args[1]
				}
		detail['details'] = exception_vals
		tb = traceback.format_exception(exc)
		error_string = tb[-2].split(',')
		file_name = error_string[0].split('/app')[-1].replace("\"", "")
		line = error_string[1].split(" ")[-1]
		error = {
			'error_type': f"{exception_name}: {exception_value}",
			'file_and_line': f"{file_name}:{line}",
			'code_piece': str(error_string[2:]).split("    ")[1].replace("', '", ", ").replace("\\n", "")
		}
		detail["error"] = error
		i_time = datetime.now(timezone.utc).strftime("%m/%d/%Y %H:%M:%S")
		logger_error = {
			"time": f"{i_time} UTC",
			"method": detail['method'],
			"url": detail['url'],
			"query_params": detail['query_params'],
			"status_code": 500,
			"status_message": "Internal Server Error",
			"exception_name": exception_name,
			"exception_value": exception_value,
			"file": f"{file_name}:{line}"
		}
		cls.logger.error(logger_error)
		cls.logger.debug(detail)
		return JSONResponse(
			status_code=500,
			content = {"details": jsonable_encoder(detail)}
			)