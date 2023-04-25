from typing import List, Optional
from sqlmodel import Field, SQLModel

class SegmentModel(SQLModel, table=True):
	__tablename__ = "program_segment"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=72)
	client_uuid: str = Field(default=None, index=True, max_length=65, foreign_key="client.uuid")
	program_9char: str = Field(default=None, index=True, max_length=65, foreign_key="program.program_9char")
	segment_9char: str = Field(default=None, index=True, max_length=65)
	budget_9char: str = Field(default=None, index=True, max_length=65, foreign_key="client_budget.budget_9char")
	name: str = Field(default=None, max_length=255)
	description: str = Field(default=None)
	status: int = Field(default=None, index=True)
	time_created: int = None
	time_updated: int = None

class SegmentUpdate(SQLModel, table=False):
	name: Optional[str] = Field(default=None, max_length=255)
	description: Optional[str] = None
	client_uuid: Optional[str] = Field(default=None, max_length=65)
	program_9char: Optional[str] = Field(default=None, max_length=9)
	budget_9char: Optional[str] = Field(default=None, max_length=9)
	status: Optional[int] = None
	time_updated: Optional[int] = None
