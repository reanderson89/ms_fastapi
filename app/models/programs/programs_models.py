from sqlmodel import Field, SQLModel
from typing import Optional

class ProgramModel(SQLModel, table=True):
	__tablename__ = "program"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=65)
	user_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="user.uuid")
	program_9char: str = Field(default=None, index=True, max_length=9)
	name: str = Field(default=None, index=True, max_length=255)
	description: str = Field(default=None, index=True)
	client_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="client.uuid")
	budget_9char: str = Field(default=None, index=True, max_length=9, foreign_key="client_budget.budget_9char")
	status: int = Field(default=None, index=True)
	program_type: int = Field(default=None, index=True)
	cadence: int = Field(default=None, index=True)
	cadence_value: int = Field(default=None, index=True)
	time_created: int
	time_updated: int

class ProgramUpdate(SQLModel, table=False):
	name: Optional[str] = Field(default=None, max_length=255)
	description: Optional[str] = None
	client_uuid: Optional[str] = Field(default=None, max_length=56)
	budget_9char: Optional[str] = Field(default=None, max_length=9)
	status: Optional[int] = None
	program_type: Optional[int] = None
	cadence: Optional[int] = None
	cadence_value: Optional[int] = None
	time_updated: Optional[int] = None
