from typing import Optional
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from burp.utils.enums import RuleType, Status
from burp.models.base_models import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class ProgramRuleModelDB(Base):
    __tablename__ = "program_rule"

    uuid: Mapped[str] = mapped_column(String(81), default=None, primary_key=True, index=True)
    program_uuid: Mapped[str] = mapped_column(String(65), default=None, index=True, nullable=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    program_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    rule_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    rule_type: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    status: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    logic: Mapped[JSON] = mapped_column("logic", JSON, default=None, index=True, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class ProgramRuleModel(BasePydantic):
    uuid: Optional[str]
    program_uuid: Optional[str]
    client_uuid: Optional[str]
    program_9char: Optional[str]
    rule_9char: Optional[str]
    rule_type: Optional[RuleType]
    status: Optional[Status]
    logic: Optional[dict]
    time_created: Optional[int]
    time_updated: Optional[int]