from enum import IntEnum, Enum
from typing import Optional
from pydantic import Field
from burp.models.base_models import BasePydantic
from burp.models.program_admin import AdminModel


# TODO: finalize what permissions are needed/wanted
class AdminPermissions(IntEnum):
    none = 0
    supervisor = 1
    manager = 2

class ProgramAdminStatus(Enum):
    exists = "existing admin"
    created = "admin created"


class AdminCreate(BasePydantic):
    program_uuid: Optional[str]
    user_uuid: str
    permissions: Optional[int]

class AdminStatus(AdminModel):
    status: Optional[ProgramAdminStatus] = Field(description="This mapped_column can have the values 'exists' or 'admin created'.")

class AdminUpdate(BasePydantic):
    permissions: Optional[int]


class AdminDelete(BasePydantic):
    ok: bool
    Deleted: AdminModel
