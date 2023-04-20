from sqlmodel import Field, SQLModel
from typing import List, Optional

class UsersModel(SQLModel, table=False):
	__tablename__ = "user"

	uuid: str = Field(default=None, primary_key=True, index=True)
	first_name: str = None
	last_name: str = None
	latitude: int = None
	longitude: int = None
	time_created: int
	time_updated: int = None
	time_ping: int = None

class UsersUpdate(SQLModel, table=False):
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	latitude: Optional[int] = None
	longitude: Optional[int] = None
	time_updated: Optional[int] = None
	time_ping: Optional[str] = None
