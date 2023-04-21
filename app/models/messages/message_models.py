from sqlmodel import Field, SQLModel
from typing import Optional

class MessageModel(SQLModel, table=True):
	__tablename__ = "program_message"

	uuid: str = Field(default=None, primary_key=True, index=True, max_length=65)
	program_uuid: str = Field(default=None, index=True, max_length=65, foreign_key="program.uuid")
	client_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="client.uuid")
	program_9char: str = Field(default=None, index=True, max_length=9, foreign_key="program.program_9char")
	message_9char: str = Field(default=None, index=True, max_length=9)
	template_uuid: str = Field(default=None, index=True, max_length=56, foreign_key="message_template.uuid")
	channel: int = Field(default=None, index=True)
	status: int = Field(default=None, index=True)
	time_created: int
	time_updated: int

class MessageUpdate(SQLModel, table=False):
	program_uuid: Optional[str] = Field(default=None, max_length=65)
	client_uuid: Optional[str] = Field(default=None, max_length=56)
	program_9char: Optional[str] = Field(default=None, max_length=9)
	message_9char: Optional[str] = Field(default=None, max_length=9)
	template_uuid: Optional[str] = Field(default=None, max_length=56)
	channel: Optional[int] = None
	status: Optional[int] = None
	time_updated: Optional[int] = None
