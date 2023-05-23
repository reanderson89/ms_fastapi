from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic

class SegmentAward(Base):
	__tablename__ = "program_segment_award"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True)
	program_uuid: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None)
	segment_9char: Mapped[str] = mapped_column(default=None)
	award_9char: Mapped[str] = mapped_column(default=None)
	client_uuid: Mapped[str] = mapped_column(default=None)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class SegmentAwardUpdate(BasePydantic):
	program_9char: Optional[str] = None
	segment_9char: Optional[str] = None
	award_9char: Optional[str] = None
	time_updated: Optional[int] = None
