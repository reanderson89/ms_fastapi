from sqlmodel import Field, SQLModel
from typing import Optional

class SegmentRuleModel(SQLModel, table=False):
	__tablename__ = "program_segment_rule"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=81)
	program_uuid: str = Field(default=None, index=True, max_length=65, foreign_key="program.uuid")
	client_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="client.uuid")
	program_9char: str = Field(default=None, index=True, max_length=9, foreign_key="program.program_9char")
	segment_9char: str = Field(default=None, index=True, max_length=9, foreign_key="program_segment.segment_9char")
	rule_9char: str = Field(default=None, index=True, max_length=9, foreign_key="client_rule.rule_9char")
	status: int = Field(default=None, index=True)
	rule_type: int = Field(default=None, index=True)
	logic: str = Field(default=None)
	time_created: int
	time_updated: int

class SegmentRuleUpdate(SQLModel, table=False):
	program_uuid: Optional[str] = Field(default=None, max_length=65)
	client_uuid: Optional[str] = Field(default=None, max_length=56)
	program_9char: Optional[str] = Field(default=None, max_length=9)
	segment_9char: Optional[str] = Field(default=None, max_length=9)
	rule_9char: Optional[str] = Field(default=None, max_length=9)
	status: Optional[int] = None
	rule_type: Optional[int] = None
	logic: Optional[str] = None
	time_updated: Optional[int] = None
