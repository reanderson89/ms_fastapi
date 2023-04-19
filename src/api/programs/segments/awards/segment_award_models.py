from sqlmodel import SQLModel, Field
from typing import Optional

class Award(SQLModel, table=True):
	__tablename__ = "program_segment_award"

	uuid: str = Field(primary_key=True, index=True, max_length=77)
	program_uuid: str = Field(default=None, max_length=63, index=True, foreign_key="program.uuid")
	segment_9char: str = Field(default=None, max_length=9, index=True, foreign_key="program_segment.segment_9char")
	award_9char: str = Field(default=None, max_length=9, index=True, foreign_key="client_award.award_9char")
	time_created: int
	time_updated: int

class UpdateAward(SQLModel):
	program_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	award_9char: Optional[str] = None
	time_updated: Optional[int] = None
