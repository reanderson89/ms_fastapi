from enum import Enum
from typing import Optional
from pydantic import Field
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic

class ServiceID(str, Enum):
	email = "email"
	cell = "cell"

class UserServiceStatus(str, Enum):
	exists = "exists"
	created = "service created"
	updated = "service updated"

class UserServiceModel(Base):
	__tablename__ = "user_service"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True)
	user_uuid: Mapped[Optional[str]] = mapped_column(default=None)
	service_uuid: Mapped[Optional[str]] = mapped_column(default=None)
	service_user_id: Mapped[Optional[str]] = mapped_column(default=None)
	service_user_screenname: Mapped[Optional[str]] = mapped_column(default=None)
	service_user_name: Mapped[Optional[str]] = mapped_column(default=None)
	service_access_token: Mapped[Optional[str]] = mapped_column(default=None)
	service_access_secret: Mapped[Optional[str]] = mapped_column(default=None)
	service_refresh_token: Mapped[Optional[str]] = mapped_column(default=None)
	time_created: Mapped[Optional[int]] = mapped_column(default=None)
	time_updated: Mapped[Optional[int]] = mapped_column(default=None)
	login_secret: Mapped[Optional[str]] = mapped_column(default=None)
	login_token: Mapped[Optional[str]] = mapped_column(default=None)

class ServiceBase(BasePydantic):
	uuid: Optional[str]
	user_uuid: Optional[str]
	service_uuid: Optional[str]
	service_user_id: Optional[str]
	service_user_screenname: Optional[str]
	service_user_name: Optional[str]
	service_access_token: Optional[str]
	service_access_secret: Optional[str]
	service_refresh_token: Optional[str]
	time_created: Optional[int]
	time_updated: Optional[int]
	login_secret: Optional[str]
	login_token: Optional[str]

class UserServiceCreate(BasePydantic):
	service_uuid: ServiceID
	service_user_id: str

class ServiceStatus(ServiceBase):
	status: Optional[UserServiceStatus] = Field(
		default=None,
		description="This mapped_column can have the values 'exists' or 'admin created'."
	)

class UserServiceUpdate(BasePydantic):
	service_user_screenname: Optional[str]
	service_user_name: Optional[str]
	service_access_token: Optional[str]
	service_access_secret: Optional[str]
	service_refresh_token: Optional[str]
	login_secret: Optional[str]
	login_token: Optional[str]

class ServiceBulk(UserServiceUpdate):
	uuid: str

class ServiceDelete(BasePydantic):
	service_uuid: str
