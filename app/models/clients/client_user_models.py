from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from typing import Optional


class ClientUserModelDB(Base):
	__tablename__ = 'client_user'

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	user_uuid: Mapped[str] = mapped_column(default=None, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	manager_uuid: Mapped[str] = mapped_column(default=None, index=True)
	employee_id: Mapped[str] = mapped_column(default=None, index=True)
	title: Mapped[str] = mapped_column(default=None)
	department: Mapped[str] = mapped_column(default=None)
	active: Mapped[bool] = mapped_column(default=None)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)
	time_hire: Mapped[int] = mapped_column(default=None)
	time_start: Mapped[int] = mapped_column(default=None)
	admin: Mapped[int] = mapped_column(default=None)

class ClientUserModel(BasePydantic):
	uuid: Optional[str]
	user_uuid: Optional[str]
	client_uuid: Optional[str]
	manager_uuid: Optional[str]
	employee_id: Optional[str]
	title: Optional[str]
	department: Optional[str]
	active: Optional[bool]
	time_created: Optional[int]
	time_updated: Optional[int]
	time_hire: Optional[int]
	time_start: Optional[int]
	admin: Optional[int]

class ClientUserCreate(ClientUserModel):
	# user level fields
	first_name: Optional[str]
	last_name: Optional[str]
	location: Optional[str]
	time_birthday: Optional[int]
	# service level fields
	service_uuid: Optional[str] # email or cell
	service_user_id: Optional[str] # email or cell


class ClientUserUpdate(BasePydantic):
	uuid: Optional[str] = None
	manager_uuid: Optional[str] = None
	employee_id: Optional[str] = None
	title: Optional[str] = None
	department: Optional[str] = None
	active: Optional[bool] = None
	time_updated: Optional[int] = None
	admin: Optional[int] = None
