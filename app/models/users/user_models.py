from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic

class UserBase():
	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	first_name: Mapped[str] = mapped_column(default=None)
	last_name: Mapped[str] = mapped_column(default=None)
	latitude: Mapped[int] = mapped_column(default=None)
	longitude: Mapped[int] = mapped_column(default=None)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)
	time_ping: Mapped[int] = mapped_column(default=None)
	time_birthday: Mapped[int] = mapped_column(default=None)

class UserModel(Base, UserBase):
	__tablename__ = "user"

class UserUpdate(BasePydantic):
	first_name: Optional[str] = mapped_column(default=None)
	last_name: Optional[str] = mapped_column(default=None)
	latitude: Optional[int] = None
	longitude: Optional[int] = None
	time_birthday: Optional[int] = None

class UserExpanded(BasePydantic):
	services: dict = None
