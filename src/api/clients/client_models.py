from sqlmodel import Field, SQLModel
from typing import Optional

class ClientModel(SQLModel, table=True):
	__tablename__ = "client"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
	name: str = Field(default=None, index=True, max_length=255)
	description: str = Field(default=None, index=True, max_length=256)
	time_created: int
	time_updated: int
	time_ping: int

class ClientUpdate(SQLModel, table=False):
	name: Optional[str] = None
	description: Optional[str] = None
	time_updated: Optional[int] = None
	time_ping: Optional[int] = None
