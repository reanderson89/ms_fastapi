from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic


class ClientModel(Base):
	__tablename__ = "client"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	name: Mapped[str] = mapped_column(default=None, index=True)
	description: Mapped[str] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)
	time_ping: Mapped[int] = mapped_column(default=None)
	status: Mapped[int] = mapped_column(default=0)

class ClientBase(BasePydantic):
	uuid: Optional[str]
	name: Optional[str]
	description: Optional[str]
	time_created: Optional[int]
	time_updated: Optional[int]
	time_ping: Optional[int]
	status: Optional[int]

class ClientExpanded(ClientBase):
	budgets: dict = None

class ClientUpdate(BasePydantic):
	name: Optional[str] = None
	description: Optional[str] = None
	status: Optional[int] = None
