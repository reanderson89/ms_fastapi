from sqlmodel import SQLModel, Field
from typing import Optional

class SegmentAward(SQLModel, table=False):
	__tablename__ = "program_segment_award"

	uuid: str = Field(primary_key=True, max_length=77)
	program_9char: str = Field(max_length=63)
	segment_9char: str = Field(max_length=7)
	award_9char: str = Field(max_length=7)
	time_created: int
	time_updated: int

class SegmentAwardUpdate(SQLModel):
	program_9char: str = None
	segment_9char: str = None
	award_9char: str = None
	time_updated: int = None
