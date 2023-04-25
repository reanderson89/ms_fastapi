from sqlmodel import Field, SQLModel
from typing import Optional

class ProgramAdminModel(SQLModel, table=True):
	__tablename__ = "program_admin"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
	program_uuid: str = Field(default=None, index=True, max_length=65, foreign_key="program.uuid")
	client_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="client.uuid")
	program_9char: str = Field(default=None, index=True, max_length=9)
	user_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="user.uuid")
	permissions: int = Field(default=None, index=True)
	time_created: int = None
	time_updated: int = None

class ProgramAdminUpdate(SQLModel, table=False):
	program_uuid: Optional[str] = Field(default=None, max_length=65)
	program_9char: Optional[str] = Field(default=None, max_length=9)
	client_uuid: Optional[str] = Field(default=None, max_length=56)
	user_uuid: Optional[str] = Field(default=None, max_length=56)
	permissions: Optional[int] = None
	time_updated: Optional[int] = None
