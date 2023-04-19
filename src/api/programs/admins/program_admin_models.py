from sqlmodel import Field, SQLModel
from typing import Optional

class ProgramAdminModel(SQLModel, table=True):
	__tablename__ = "program_admin"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=63)
	program_uuid: str = Field(default=None, index=True, max_length=63, foreign_key="program.uuid")
	user_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="user.uuid")
	permissions: int = Field(default=None, index=True)
	time_created: int
	time_updated: int

class ProgramAdminUpdate(SQLModel, table=False):
	program_uuid: Optional[str] = None
	user_uuid: Optional[str] = None
	permissions: Optional[int] = None
	time_updated: Optional[int] = None
