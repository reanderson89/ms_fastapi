from enum import IntEnum, Enum
from typing import Optional
from sqlmodel import Field, SQLModel

class AdminPermissions(IntEnum):
	none = 0
	supervisor = 1
	manager = 2

class AdminStatus(str, Enum):
	exists = "exists"
	created = "admin created"

class AdminExpand(str, Enum):
	client = "client"
	program = "program"
	user = "user"

class AdminBase(SQLModel):
	uuid: Optional[str] = Field(default=None, primary_key=True, index=True, max_length=56)
	program_uuid: Optional[str] = Field(default=None, index=True, max_length=65)
	client_uuid: Optional[str] = Field(default=None, index=True, max_length=56)
	program_9char: Optional[str] = Field(default=None, index=True, max_length=9)
	user_uuid: Optional[str] = Field(default=None, index=True, max_length=56)
	permissions: Optional[AdminPermissions] = Field(default=0, index=True)
	time_created: Optional[int] = None
	time_updated: Optional[int] = None

class AdminModel(AdminBase, table=True):
	__tablename__ = "program_admin"

class AdminCreate(SQLModel):
	program_uuid: Optional[str]
	user_uuid: str
	permissions: Optional[int]

class AdminStatus(AdminBase):
	status: AdminStatus = Field(description="This field can have the values 'exists' or 'admin created'.")

class AdminUpdate(SQLModel):
	permissions: Optional[int]
