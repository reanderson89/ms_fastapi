from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic

class ProgramEventModel(Base):
	__tablename__ = "program_event"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	program_uuid: Mapped[str] = mapped_column(default=None, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None, index=True)
	event_9char: Mapped[str] = mapped_column(default=None, index=True)
	event_type: Mapped[int] = mapped_column(default=None, index=True)
	parent_9char: Mapped[str] = mapped_column(default=None, index=True)
	segment_9char: Mapped[str] = mapped_column(default=None, index=True)
	event_data: Mapped[str] = mapped_column(default=None)
	status: Mapped[int] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class ProgramEventUpdate(BasePydantic):
	program_uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	event_9char: Optional[str] = None
	event_type: Optional[int] = None
	parent_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	event_data: Optional[str] = None
	status: Optional[int] = None
	time_updated: Optional[int] = None
