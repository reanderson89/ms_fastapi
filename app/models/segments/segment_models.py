from typing import List, Optional
from sqlmodel import Field, SQLModel

class SegmentModel(SQLModel, table=False):
	__tablename__ = "program_segment"

	uuid: str = Field(default=None, primary_key=True, index=True)
	client_uuid: str = Field(default=None, index=True, foreign_key="client.uuid")
	program_9char: str = Field(default=None, index=True, foreign_key="program.program_9char")
	segment_9char: str = Field(default=None, index=True, foreign_key="segment.segment_9char")
	budget_9char: str = Field(default=None, index=True, foreign_key="client_budget.budget_9char")
	name: str = Field(default=None)
	description: str = Field(default=None)
	status: int = Field(default=None, index=True)
	time_created: int
	time_updated: int

class SegmentUpdate(SQLModel, table=False):
	name: Optional[str] = None
	description: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	budget_9char: Optional[str] = None
	status: Optional[int] = None
	time_updated: Optional[int] = None
