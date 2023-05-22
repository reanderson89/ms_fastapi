from typing import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
	uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
	first_name: str = Field(default=None, max_length=255)
	last_name: str = Field(default=None, max_length=255)
	latitude: int = None
	longitude: int = None
	time_created: int = None
	time_updated: int = None
	time_ping: int = None
	time_birthday: int = None

# Alternate implemetnation for SQMModel table using inheritance
class User(UserBase):
	__tablename__ = "user"

class UserExpanded(UserBase):
	services: dict = None

class UsersModel(SQLModel, table=True):
	__tablename__ = "user"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
	first_name: str = Field(default=None, max_length=255)
	last_name: str = Field(default=None, max_length=255)
	latitude: int = None
	longitude: int = None
	time_created: int = None
	time_updated: int = None
	time_ping: int = None
	time_birthday: int = None

class UsersUpdate(SQLModel, table=False):
	first_name: Optional[str] = Field(default=None, max_length=255)
	last_name: Optional[str] = Field(default=None, max_length=255)
	latitude: Optional[int] = None
	longitude: Optional[int] = None
	time_updated: Optional[int] = None
	time_ping: Optional[int] = None
