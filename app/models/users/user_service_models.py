from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic

class Service(str, Enum):
	email = "email"
	cell = "cell"

class UserServiceStatus(str, Enum):
	exists = "exists"
	created = "service created"

class UserService(Base):
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
	

class UserServiceCreate(BasePydantic):
	service_uuid: Service
	service_user_id: str

class ServiceStatus(BasePydantic):
	status: UserServiceStatus = None#(description="This mapped_column can have the values 'exists' or 'admin created'.")

class UsersServiceUpdate(BasePydantic):
	service_user_screenname: Optional[str]
	service_user_name: Optional[str]
	service_access_token: Optional[str]
	service_access_secret: Optional[str]
	service_refresh_token: Optional[str]
	login_secret: Optional[str]
	login_token: Optional[str]
class ServiceBulk(UsersServiceUpdate):
	uuid: str

class ServiceDelete(BasePydantic):
	service_uuid: str
