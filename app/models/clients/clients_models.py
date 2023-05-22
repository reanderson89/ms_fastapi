from sqlmodel import Field, SQLModel
from typing import Optional
from uuid import uuid4

class ClientModel(SQLModel, table=True):
	__tablename__ = "client"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
	name: str = Field(default=None, index=True, max_length=255)
	description: str = Field(default=None, index=True)
	time_created: int = None
	time_updated: int = None
	time_ping: int = None

class ClientBase(SQLModel):
	uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
	name: str = Field(default=None, index=True, max_length=255)
	description: str = Field(default=None, index=True)
	time_created: int = None
	time_updated: int = None
	time_ping: int = None


class Client(ClientBase):
	__tablename__ = "user"


class ClientExpanded(ClientBase):
	budgets: dict = None


class ClientUpdate(SQLModel, table=False):
	name: Optional[str] = Field(default=None, max_length=255)
	description: Optional[str] = None
	time_updated: Optional[int] = None
	time_ping: Optional[int] = None
