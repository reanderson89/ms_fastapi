from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
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

class ProgramBase(BasePydantic):
	uuid: Optional[str]
	user_uuid: Optional[str]
	program_9char: Optional[str]
	name: Optional[str]
	description: Optional[str]
	client_uuid: Optional[str]
	budget_9char: Optional[str]
	status: Optional[int]
	program_type: Optional[int]
	cadence: Optional[int]
	cadence_value: Optional[int]
	time_created: Optional[int]
	time_updated: Optional[int]

class ProgramCreate(BasePydantic):
	user_uuid: str
	name: str
	description: Optional[str]
	client_uuid: Optional[str]
	budget_9char: Optional[str]
	status: Optional[int]
	program_type: Optional[int]
	cadence: int
	cadence_value: Optional[int]

class ProgramUpdate(BasePydantic):
	name: Optional[str]
	description: Optional[str]
	client_uuid: Optional[str]
	budget_9char: Optional[str]
	status: Optional[int]
	program_type: Optional[int]
	cadence: Optional[int]
	cadence_value: Optional[int]
	time_updated: Optional[int]
