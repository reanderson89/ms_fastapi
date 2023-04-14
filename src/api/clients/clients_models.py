from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional

class ClientModel(SQLModel, table=True):
	__tablename__ = "client"

	uuid: str = Field(default=None, primary_key=True, index=True)
	name: str = Field(default=None, index=True)
	description: str = Field(default=None, index=True)
	time_created: int
	time_updated: int
	time_ping: int


class ClientUpdate(SQLModel):
	name: Optional[str] = None
	description: Optional[str] = None
	time_updated: Optional[int] = None
	time_ping: Optional[int] = None