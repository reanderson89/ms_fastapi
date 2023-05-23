from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic

class ProgramModel(Base):
	__tablename__ = "program"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	user_uuid: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None, index=True)
	name: Mapped[str] = mapped_column(default=None, index=True)
	description: Mapped[str] = mapped_column(default=None, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	budget_9char: Mapped[str] = mapped_column(default=None, index=True)
	status: Mapped[int] = mapped_column(default=None, index=True)
	program_type: Mapped[int] = mapped_column(default=None, index=True)
	cadence: Mapped[int] = mapped_column(default=None, index=True)
	cadence_value: Mapped[int] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class ProgramUpdate(BasePydantic):
	name: Optional[str] = None
	description: Optional[str] = None
	client_uuid: Optional[str] = None
	budget_9char: Optional[str] = None
	status: Optional[int] = None
	program_type: Optional[int] = None
	cadence: Optional[int] = None
	cadence_value: Optional[int] = None
	time_updated: Optional[int] = None
