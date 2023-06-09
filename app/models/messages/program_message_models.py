from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from typing import Optional

class MessageModel(Base):
	__tablename__ = "program_message"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	program_uuid: Mapped[str] = mapped_column(default=None, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None, index=True)
	message_9char: Mapped[str] = mapped_column(default=None, index=True)
	template_uuid: Mapped[str] = mapped_column(default=None, index=True)
	channel: Mapped[int] = mapped_column(default=None, index=True)
	status: Mapped[int] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class MessageCreate(BasePydantic):
	template_uuid: Optional[str] = None
	channel: Optional[int] = None
	status: Optional[int] = None

class MessageUpdate(BasePydantic):
	template_uuid: Optional[str] = None
	channel: Optional[int] = None
	status: Optional[int] = None
