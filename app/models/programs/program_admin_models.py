from enum import IntEnum, Enum
from typing import Optional
from pydantic import Field
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic

class AdminPermissions(IntEnum):
	none = 0
	supervisor = 1
	manager = 2

class ProgramAdminStatus(str, Enum):
	exists = "exists"
	created = "admin created"

class AdminExpand(str, Enum):
	client = "client"
	program = "program"
	user = "user"

class AdminModelDB(Base):
	__tablename__ = "program_admin"

	uuid: Mapped[Optional[str]] = mapped_column(default=None, primary_key=True, index=True)
	program_uuid: Mapped[Optional[str]] = mapped_column(default=None, index=True)
	client_uuid: Mapped[Optional[str]] = mapped_column(default=None, index=True)
	program_9char: Mapped[Optional[str]] = mapped_column(default=None, index=True)
	user_uuid: Mapped[Optional[str]] = mapped_column(default=None, index=True)
	permissions: Mapped[Optional[int]] = mapped_column(default=0, index=True)
	time_created: Mapped[Optional[int]] = mapped_column(default=None)
	time_updated: Mapped[Optional[int]] = mapped_column(default=None)

class AdminModel(BasePydantic):
	uuid: Optional[str]
	program_uuid: Optional[str]
	client_uuid: Optional[str]
	program_9char: Optional[str]
	user_uuid: Optional[str]
	permissions: Optional[int]
	time_created: Optional[int]
	time_updated: Optional[int]

class AdminCreate(BasePydantic):
	program_uuid: Optional[str]
	user_uuid: str
	permissions: Optional[int]

class AdminStatus(AdminModel):
	status: Optional[ProgramAdminStatus] = Field(description="This mapped_column can have the values 'exists' or 'admin created'.")

class AdminUpdate(BasePydantic):
	permissions: Optional[int]
