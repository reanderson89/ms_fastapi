from sqlmodel import Field, SQLModel
from typing import Optional


class ProgramEventModel(SQLModel, table=True):
	__tablename__ = "program_event"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=70)
	program_uuid: str = Field(default=None, index=True, max_length=63, foreign_key="program.uuid")
	client_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="client.uuid")
	program_9char: str = Field(default=None, index=True, max_length=7, foreign_key="program.program_9char")
	event_9char: str = Field(default=None, index=True, max_length=7, foreign_key="client_event.event_9char")
	event_type: int = Field(default=None, index=True)
	parent_9char: str = Field(default=None, index=True, max_length=7, foreign_key="client_event.event_9char")
	segment_9char: str = Field(default=None, index=True, max_length=7, foreign_key="program_segment.segment_9char")
	event_data: str = Field(default=None)
	status: int = Field(default=None, index=True)
	time_created: int
	time_updated: int

class ProgramEventUpdate(SQLModel, table=False):
	program_uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	event_9char: Optional[str] = None
	event_type: Optional[int] = None
	parent_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	event_data: Optional[str] = None
	status: Optional[int] = None
	time_updated: Optional[int] = None
