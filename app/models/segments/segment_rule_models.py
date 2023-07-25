from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic

class SegmentRuleModel(Base):
    __tablename__ = "program_segment_rule"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    program_uuid: Mapped[str] = mapped_column(default=None, index=True)
    client_uuid: Mapped[str] = mapped_column(default=None, index=True)
    program_9char: Mapped[str] = mapped_column(default=None, index=True)
    segment_9char: Mapped[str] = mapped_column(default=None, index=True)
    rule_9char: Mapped[str] = mapped_column(default=None, index=True)
    status: Mapped[int] = mapped_column(default=None, index=True)
    rule_type: Mapped[int] = mapped_column(default=None, index=True)
    logic: Mapped[str] = mapped_column(default=None)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)

class SegmentRuleUpdate(BasePydantic):
    program_uuid: Optional[str] = None
    client_uuid: Optional[str] = None
    program_9char: Optional[str] = None
    segment_9char: Optional[str] = None
    rule_9char: Optional[str] = None
    status: Optional[int] = None
    rule_type: Optional[int] = None
    logic: Optional[str] = None
    time_updated: Optional[int] = None
