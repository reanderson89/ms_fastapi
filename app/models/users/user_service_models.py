from enum import Enum
from sqlmodel import Field, SQLModel
from typing import Optional

class Service(str, Enum):
	email = "email"
	cell = "cell"

class UserServiceBase(SQLModel):
	user_uuid: Optional[str] = Field(default=None, description="UUID set from `users` table")
	service_uuid: Optional[str] = Field(default=None)
	service_user_id: Optional[str] = Field(default=None, max_length=255)
	service_user_screenname: Optional[str] = Field(default=None, max_length=255)
	service_user_name: Optional[str] = Field(default=None, max_length=255)
	service_access_token: Optional[str] = Field(default=None, max_length=255)
	service_access_secret: Optional[str] = Field(default=None, max_length=255)
	service_refresh_token: Optional[str] = Field(default=None, max_length=255)
	time_created: Optional[int] = None
	time_updated: Optional[int] = None

class UserService(UserServiceBase, table=True):
	__tablename__ = "user_service"

	uuid: str = Field(primary_key=True, default=None, max_length=56)

class UserServiceCreate(SQLModel):
	service_uuid: Service
	service_user_id: str

class Exists(UserServiceBase):
	status: str = "exists"

class UsersServiceUpdate(SQLModel):
	service_user_screenname: Optional[str]
	service_user_name: Optional[str]
	service_access_token: Optional[str]
	service_access_secret: Optional[str]
	service_refresh_token: Optional[str]

class ServiceBulk(UsersServiceUpdate):
	uuid: str


class ServiceDelete(SQLModel):
	service_uuid: str
