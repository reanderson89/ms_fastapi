from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic


class ProgramRuleModel(Base):
	__tablename__ = "program_rule"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	program_uuid: Mapped[str] = mapped_column(default=None, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None, index=True)
	rule_9char: Mapped[str] = mapped_column(default=None, index=True)
	rule_type: Mapped[int] = mapped_column(default=None, index=True)
	logic: Mapped[str] = mapped_column(default=None, index=True)
	status: Mapped[int] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)


class ProgramRuleUpdate(BasePydantic):
	rule_type: Optional[int] = None
	logic: Optional[str] = None
	status: Optional[int] = None


class ProgramRuleCreate(BasePydantic):
	rule_type: Optional[int] = None
	logic: Optional[str] = None
	status: Optional[int] = None