from sqlmodel import SQLModel, Field

class Award(SQLModel, table=True):
	__tablename__ = "program_segment_award"

	uuid: str = Field(primary_key=True, max_length=77)
	program_7char: str = Field(max_length=63)
	segment_7char: str = Field(max_length=7)
	award_7char: str = Field(max_length=7)
	time_created: int
	time_updated: int

class CreateAward(SQLModel):
	uuid: str
	award_7char: str
	time_created: int
	time_updated: int

class UpdateAward(SQLModel):
	program_7char: str = None
	segment_7char: str = None
	award_7char: str = None
	time_updated: int = None
