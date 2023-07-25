from typing import Optional
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic


class ProgramRuleModelDB(Base):
    __tablename__ = "program_rule"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    program_uuid: Mapped[str] = mapped_column(default=None, index=True)
    client_uuid: Mapped[str] = mapped_column(default=None, index=True)
    program_9char: Mapped[str] = mapped_column(default=None, index=True)
    rule_9char: Mapped[str] = mapped_column(default=None, index=True)
    rule_type: Mapped[int] = mapped_column(default=None, index=True)
    logic: Mapped[JSON] = mapped_column("logic", JSON, default=None, index=True)
    status: Mapped[int] = mapped_column(default=None, index=True)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)


class ProgramRuleResponse(BasePydantic):
    uuid: Optional[str] = None
    program_uuid: Optional[str] = None
    client_uuid: Optional[str] = None
    program_9char: Optional[str] = None
    rule_9char: Optional[str] = None
    rule_type: Optional[int] = None
    logic: Optional[dict] = None
    status: Optional[int] = None
    time_created: Optional[int] = None
    time_updated: Optional[int] = None


class ProgramRuleUpdate(BasePydantic):
    rule_type: Optional[int] = None
    logic: Optional[dict] = None
    status: Optional[int] = None


class ProgramRuleCreate(BasePydantic):
    rule_type: Optional[int] = None
    logic: dict
    status: Optional[int] = None
