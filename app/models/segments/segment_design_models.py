from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic

class SegmentDesignModel(Base):
    __tablename__ = "program_segment_design"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    client_uuid: Mapped[str] = mapped_column(default=None, index=True)
    program_9char: Mapped[str] = mapped_column(default=None, index=True)
    segment_9char: Mapped[str] = mapped_column(default=None, index=True)
    design_9char: Mapped[str] = mapped_column(default=None, index=True)
    message_uuid: Mapped[str] = mapped_column(default=None, index=True)
    program_uuid: Mapped[str] = mapped_column(default=None, index=True)
    channel: Mapped[int] = mapped_column(default=None, index=True)
    status: Mapped[int] = mapped_column(default=None, index=True)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)

class SegmentDesignUpdate(BasePydantic):
    channel: Optional[int] = None
    status: Optional[int] = None

class SegmentDesignReturn(BasePydantic):
    uuid: str
    client_uuid: str
    program_9char: str
    segment_9char: str
    design_9char: str
    program_uuid: Optional[str] = None
    message_uuid: Optional[str] = None
    channel: Optional[int] = None
    status: Optional[int] = None
    time_created: Optional[int] = None
    time_updated: Optional[int] = None

class SegmentDesignCreate(BasePydantic):
    program_uuid: Optional[str] = None
    message_uuid: Optional[str] = None
    channel: Optional[int] = None
    status: Optional[int] = None