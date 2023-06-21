from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from typing import Optional


class ClientUserModel(Base):
	__tablename__ = "client_user"

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

class ClientUserUpdate(BasePydantic):
	manager_uuid: Optional[str] = None
	employee_id: str = None
	title: str = None
	department: Optional[str] = None
	active: Optional[bool] = None
	time_updated: Optional[int] = None
	admin: Optional[int] = None
