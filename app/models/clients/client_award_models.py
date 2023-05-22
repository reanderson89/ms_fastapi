from sqlmodel import Field, SQLModel
from typing import List, Optional

class ClientAwardModel(SQLModel, table=True):
	__tablename__ = "client_award"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=65)
	client_uuid: str = Field(default=None, index=True, foreign_key="client.uuid", max_length=56)
	award_9char: str = Field(default=None, index=None, max_length=9)
	award_type: int = Field(default=0)
	name: str = Field(default=None, max_length=255)
	description: str = Field(default=None)
	hero_image: str = Field(default=None, max_length=255)
	channel: int = Field(default=0)
	time_created: int = None
	time_updated: int = None

class ClientAwardUpdate(SQLModel, table=False):
	award_type: Optional[int] = None
	name: Optional[str] = Field(default=None, max_length=255)
	description: Optional[str] = None
	hero_image: Optional[str] = Field(default=None, max_length=255)
	channel: Optional[int] = 0
	time_updated: Optional[int] = 0
