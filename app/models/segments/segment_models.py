from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic

class SegmentModel(Base):
	__tablename__ = "program_segment"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None, index=True)
	segment_9char: Mapped[str] = mapped_column(default=None, index=True)
	budget_9char: Mapped[str] = mapped_column(default=None, index=True)
	name: Mapped[str] = mapped_column(default=None)
	description: Mapped[str] = mapped_column(default=None)
	status: Mapped[int] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class SegmentReturn(BasePydantic):
	uuid: str 
	client_uuid: str 
	program_9char: str 
	segment_9char: str 
	budget_9char: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	status: Optional[int] = None
	time_created: Optional[int] = None
	time_updated: Optional[int] = None

class SegmentUpdate(BasePydantic):
	name: Optional[str] = None
	description: Optional[str] = None
	budget_9char: Optional[str] = None
	status: Optional[int] = None

class SegmentCreate(BasePydantic):
	budget_9char: Optional[str]
	name: Optional[str]
	description: Optional[str]
	status: Optional[int]
