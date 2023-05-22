from typing import List, Optional
from sqlmodel import Field, SQLModel

class MessageTemplateModel(SQLModel, table=True):
	__tablename__ = "message_template"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
	channel: int = Field(default=None)
	body: str = Field(default=None)
	time_created: int = None
	time_updated: int = None

class MessageTemplateUpdateModel(SQLModel, table=False):
	channel: Optional[int]
	body: Optional[str]
	time_updated: Optional[int]
