from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic

class SegmentDesignModel(Base):
	__tablename__ = "program_segment_design"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	program_uuid: Mapped[str] = mapped_column(default=None, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None, index=True)
	segment_9char: Mapped[str] = mapped_column(default=None, index=True)
	design_9char: Mapped[str] = mapped_column(default=None, index=True)
	template_uuid: Mapped[str] = mapped_column(default=None, index=True)
	channel: Mapped[int] = mapped_column(default=None, index=True)
	status: Mapped[int] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class SegmentDesignUpdate(BasePydantic):
	program_uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	design_9char: Optional[str] = None
	template_uuid: Optional[str] = None
	channel: Optional[int] = None
	status: Optional[int] = None
	time_updated: Optional[int] = None
