from sqlmodel import SQLModel, Field
from typing import Optional

class SegmentAward(SQLModel, table=False):
	__tablename__ = "program_segment_award"

	uuid: str = Field(default=None, primary_key=True, max_length=81)
	program_uuid: str = Field(default=None, index=True, max_length=65, foreign_key="program.uuid")
	program_9char: str = Field(default=None, max_length=9, foreign_key="program.program_9char")
	segment_9char: str = Field(default=None, max_length=7, foreign_key="program_segment_rule.segment_9char")
	award_9char: str = Field(default=None, max_length=7)
	client_uuid: str = Field(default=None, max_length=56, foreign_key="client.uuid")
	time_created: int
	time_updated: int

class SegmentAwardUpdate(SQLModel):
	program_9char: str = Field(default=None, max_length=9)
	segment_9char: str = Field(default=None, max_length=9)
	award_9char: str = Field(default=None, max_length=9)
	time_updated: int = None
