from sqlmodel import Field, SQLModel
from typing import Optional

class SegmentDesignModel(SQLModel, table=False):
	__tablename__ = "program_segment_design"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=77)
	program_uuid: str = Field(default=None, index=True, max_length=63, foreign_key="program.uuid")
	client_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="client.uuid")
	program_9char: str = Field(default=None, index=True, max_length=7, foreign_key="program.program_9char")
	segment_9char: str = Field(default=None, index=True, max_length=7, foreign_key="program_segment.segment_9char")
	design_9char: str = Field(default=None, index=True, max_length=7, foreign_key="client_design.design_9char")
	template_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="client_template.uuid")
	channel: int = Field(default=None, index=True)
	status: int = Field(default=None, index=True)
	time_created: int
	time_updated: int

class SegmentDesignUpdate(SQLModel, table=False):
	program_uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	design_9char: Optional[str] = None
	template_uuid: Optional[str] = None
	channel: Optional[int] = None
	status: Optional[int] = None
	time_updated: Optional[int] = None
	