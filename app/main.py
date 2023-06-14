import uvicorn

from app.actions.base_actions import BaseActions
from app.configs import run_config
from app.models.users import UserModel, UserServiceModel
from app.routers import routers
from app.middleware import LoggingMiddleware
from app.routers import routers, auth_routers
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
	user1 = UserModel(
		uuid="55063ccb52750171d9138f6293d93330e5be577fba84e92d72856426",
		first_name="TestUser",
		last_name="CellService",
		latitude=407127281,
		longitude=-740060152,
		time_created=1686591427,
		time_updated=1686591427,
		time_ping=1686591427
	)

	user2 = UserModel(
		uuid="0e58cd793a1d465c638276e450a92d82082f640b494fbc7735478aa9",
		first_name="TestUser",
		last_name="EmailService",
		latitude=407127281,
		longitude=-740060152,
		time_created=1686591427,
		time_updated=1686591427,
		time_ping=1686591427
	)

	user1_service = UserServiceModel(
		uuid= "a59a0209ab829e672d748026608bdcc19695d01b3e56ffc0d6adb29e",
		user_uuid= "55063ccb52750171d9138f6293d93330e5be577fba84e92d72856426",
		service_uuid= "cell",
		service_user_id= "15005550006",
		service_user_screenname= "TestUser CellService",
		service_user_name= "testusercellservice",
		service_access_token= "access token",
		service_access_secret= "secret token",
		service_refresh_token= "refresh token",
		time_created= 1686591427,
		time_updated= 1686591427,
		login_secret="place_holder",
		login_token="place_holder"
	)

	user2_service = UserServiceModel(
		uuid="774339d7415fe0f393cb401ed6efdb3537af7b0b9a1235bf542767b1",
		user_uuid="0e58cd793a1d465c638276e450a92d82082f640b494fbc7735478aa9",
		service_uuid="email",
		service_user_id="test.user@testclient.com",
		service_user_screenname="TestUser EmailService",
		service_user_name="testuseremailservice",
		service_access_token="access token",
		service_access_secret="secret token",
		service_refresh_token="refresh token",
		time_created=1686591427,
		time_updated=1686591427,
		login_secret="place_holder",
		login_token="place_holder"
	)
 
	'''
	try/except was added because when the container would reload when a change was made,
	it would error out on the fact that the users already existed.
	'''
	try:
		added_users = await BaseActions.create([user1, user2])
		added_services = await BaseActions.create([user1_service, user2_service])
		yield
	except:
		yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(HTTPException, LoggingMiddleware.http_exception_handler)
app.add_exception_handler(RequestValidationError, LoggingMiddleware.validation_exception_handler)
app.include_router(routers, prefix="/v1")
app.include_router(auth_routers, prefix="/v1")


if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		**run_config.__dict__
	)
