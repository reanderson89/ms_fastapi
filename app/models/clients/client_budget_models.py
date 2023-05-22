from typing import Optional, List
from sqlmodel import Field, SQLModel


class ClientBudgetBase(SQLModel):
	uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
	client_uuid: str = Field(default=None, index=True, max_length=56)
	budget_9char: str = Field(default=None, index=True, max_length=9)
	parent_9char: str = Field(default=None, index=True, max_length=9)
	name: str = Field(default=None, max_length=255)
	value: int = Field(default=0)
	time_created: int = None
	time_updated: int = None
	active: bool = Field(default=True)
	budget_type: int = Field(default=0)

class ClientBudgetModel(ClientBudgetBase, table=True):
	__tablename__ = "client_budget"

class ClientBudgetCreate(SQLModel):
	budget_9char: Optional[str] = None
	parent_9char: Optional[str] = None
	name: Optional[str] = None
	value: int = None
	active: Optional[bool] = True
	budget_type: Optional[int] = 0

class ClientBudgetUpdate(SQLModel):
	name: Optional[str] = Field(default=None, max_length=255)
	value: Optional[int] = 0
	parent_9char: Optional[str] = None
	time_updated: Optional[int] = 0
	active: Optional[bool]
	budget_type: Optional[int]

class ClientBudgetExpanded(ClientBudgetBase):
	client: Optional[dict]
	subbudgets_expanded: Optional[List[dict]]

class ClientBudgetShortExpand(ClientBudgetBase):
	client: Optional[str]
	subbudgets: Optional[dict]
