from sqlmodel import Field, SQLModel
from typing import Optional

class ProgramEventModel(SQLModel, table=True):
	__tablename__ = "program_event"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=72)
	program_uuid: str = Field(default=None, index=True, max_length=65, foreign_key="program.uuid")
	client_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="client.uuid")
	program_9char: str = Field(default=None, index=True, max_length=9, foreign_key="program.program_9char")
	event_9char: str = Field(default=None, index=True, max_length=9)
	event_type: int = Field(default=None, index=True)
	parent_9char: str = Field(default=None, index=True, max_length=9)
	segment_9char: str = Field(default=None, index=True, max_length=9, foreign_key="program_segment.segment_9char")
	event_data: str = Field(default=None)
	status: int = Field(default=None, index=True)
	time_created: int
	time_updated: int

class ProgramEventUpdate(SQLModel, table=False):
	program_uuid: Optional[str] = Field(default=None, max_length=65)
	client_uuid: Optional[str] = Field(default=None, max_length=56)
	program_9char: Optional[str] = Field(default=None, max_length=9)
	event_9char: Optional[str] = Field(default=None, max_length=9)
	event_type: Optional[int] = None
	parent_9char: Optional[str] = Field(default=None, max_length=9)
	segment_9char: Optional[str] = Field(default=None, max_length=9)
	event_data: Optional[str] = None
	status: Optional[int] = None
	time_updated: Optional[int] = None
