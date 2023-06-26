from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic


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
	channel: Mapped[int] = mapped_column(default=None)
	status: Mapped[int] = mapped_column(default=1)
	body: Mapped[str] = mapped_column(default=None)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class MessageModel(BasePydantic):
	name: Optional[str] = None
	body: Optional[str] = None
	channel: Optional[int] = None
	message_uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	message_type: Optional[int] = None
	status: Optional[int] = None

class MessageCreate(BasePydantic):
	name: str
	body: str
	channel: int
	message_uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	message_type: Optional[int] = None
	status: Optional[int] = None

class MessageUpdate(BasePydantic):
	name: Optional[str] = None
	message_type: Optional[int] = None
	channel: Optional[int] = None
	status: Optional[int] = None
	body: Optional[str] = None
