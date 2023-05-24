from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from typing import Optional


class ClientBudgetBase():
	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	budget_9char: Mapped[str] = mapped_column(default=None, index=True)
	parent_9char: Mapped[str] = mapped_column(default=None, index=True)
	name: Mapped[str] = mapped_column(default=None)
	value: Mapped[int] = mapped_column(default=0)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)
	active: Mapped[bool] = mapped_column(default=True)
	budget_type: Mapped[int] = mapped_column(default=0)

class ClientBudgetModel(ClientBudgetBase, Base):
	__tablename__ = "client_budget"

class ClientBudgetCreate(BasePydantic):
	budget_9char: Optional[str] = None
	parent_9char: Optional[str] = None
	name: Optional[str] = None
	value: int = None
	active: Optional[bool] = True
	budget_type: Optional[int] = 0

class ClientBudgetUpdate(BasePydantic):
	name: Optional[str] = None
	value: Optional[int] = 0
	parent_9char: Optional[str] = None
	time_updated: Optional[int] = 0
	active: Optional[bool]
	budget_type: Optional[int]

class ClientBudgetExpanded(BasePydantic):
	client: Optional[dict]
	subbudgets_expanded: Optional[list[dict]]

class ClientBudgetShortExpand(BasePydantic):
	client: Optional[str]
	subbudgets: Optional[dict]