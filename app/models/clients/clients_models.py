from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic


class ClientModel(Base):
	__tablename__ = "client"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	name: Mapped[str] = mapped_column(default=None, index=True)
	description: Mapped[str] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)
	time_ping: Mapped[int] = mapped_column(default=None)

# class ClientBase(ClientTable):
# 	uuid: Mapped[str] = mapped_column(default=None, index=True)
# 	name: Mapped[str] = mapped_column(default=None, index=True)
# 	description: Mapped[str] = mapped_column(default=None, index=True)
# 	time_created: Mapped[int] = None
# 	time_updated: Mapped[int] = None
# 	time_ping: Mapped[int] = None

class ClientExpanded(BasePydantic):
	budgets: dict = None

class ClientUpdate(BasePydantic):
	name: Optional[str] = None
	description: Optional[str] = None
	time_updated: Optional[int] = None
	time_ping: Optional[int] = None
