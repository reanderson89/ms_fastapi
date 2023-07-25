from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic


message_types = {
	1: "welcome",
	2: "auth",
	3: "award",
	4: "anniversary",
	5: "birthday",
	6: "redeem",
	7: "message",
	8: "reminder",
	9: "survey"
}

class MessageModelDB(Base):
	__tablename__ = "message"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	name: Mapped[str] = mapped_column(default=None)
	message_uuid: Mapped[str] = mapped_column(default=None, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	message_9char: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None, index=True)
	segment_9char: Mapped[str] = mapped_column(default=None, index=True)
	message_type: Mapped[int] = mapped_column(default=1)
	channel: Mapped[int] = mapped_column(default=None) #1 = email, 2 = text, 4 = slack, 8 = ms teams, 16 = web
	status: Mapped[int] = mapped_column(default=1)
	body: Mapped[str] = mapped_column(default=None)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class MessageModel(BasePydantic):
	uuid: Optional[str] = None
	name: Optional[str] = None
	message_9char: Optional[str]
	body: Optional[str] = None
	channel: Optional[int] = None #1 = email, 2 = text, 4 = slack, 8 = ms teams, 16 = web
	message_uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	message_type: Optional[int] = None
	status: Optional[int] = None
	time_created: Optional[int]
	time_updated: Optional[int]

class MessageCreate(BasePydantic):
	name: str
	body: Optional[str]
	channel: int
	message_uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	message_type: int
	status: Optional[int] = None

class MessageUpdate(BasePydantic):
	name: Optional[str] = None
	message_type: Optional[int] = None
	channel: Optional[int] = None
	status: Optional[int] = None
	body: Optional[str] = None

class MessageRecipient(BasePydantic):
	client_user_uuid: str
	anniversary: Optional[int] = None
	award_uuid: str

class MessageSend(BasePydantic):
	client_uuid: str
	recipients: list[MessageRecipient] 
