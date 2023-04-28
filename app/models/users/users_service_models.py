from sqlmodel import Field, SQLModel
from typing import Optional

class UsersServiceModel(SQLModel, table=True):
	__tablename__ = "user_service"

	uuid: str = Field(primary_key=True, index=True)
	user_uuid: str = Field(default=None, description="UUID set from `users` table")
	service_uuid: str = Field(default=None)
	service_user_id: str = Field(default=None, index=True, max_length=255)
	service_user_screenname: str = Field(default=None, max_length=255)
	service_user_name: str = Field(default=None, max_length=255)
	service_access_token: str = Field(default=None, max_length=255)
	service_access_secret: str = Field(default=None, max_length=255)
	service_refresh_token: str = Field(default=None, max_length=255)
	time_created: int = None
	time_updated: int = None

class UsersServiceUpdate(SQLModel, table=False):
	service_user_screenname: Optional[str] = Field(default=None, max_length=255)
	service_user_name: Optional[str] = Field(default=None, max_length=255)
	service_access_token: Optional[str] = Field(default=None, max_length=255)
	service_access_secret: Optional[str] = Field(default=None, max_length=255)
	service_refresh_token: Optional[str] = Field(default=None, max_length=255)
	time_updated: Optional[int] = None
