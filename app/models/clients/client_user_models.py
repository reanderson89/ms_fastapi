from typing import Optional
from pydantic import validator
from burp.utils.enums import Admin
from burp.models.base_models import BasePydantic
from burp.models.user import UserModel
from burp.models.client_user import ClientUserModel



class ClientUserResponse(ClientUserModel):
    pass


class ClientUserCreate(BasePydantic):
    # user level fields
    first_name: Optional[str]
    last_name: Optional[str]
    location: Optional[str]
    time_birthday: Optional[int]
    # service level fields
    service_uuid: Optional[str] # "email" or "cell"
    service_user_id: Optional[str] # email address or cell phone number
    #include title, manager_uuid, department, active, admin
    admin: Optional[Admin]

    @validator('admin', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientUserUpdate(BasePydantic):
    uuid: Optional[str]
    manager_uuid: Optional[str]
    employee_id: Optional[str]
    title: Optional[str]
    department: Optional[str]
    active: Optional[bool]
    admin: Optional[Admin]

    @validator('admin', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientUserExpand(ClientUserModel):
    user: Optional[UserModel]
    # user_service: Optional[dict]


class ClientUserDelete(BasePydantic):
    ok: bool
    Deleted: ClientUserModel
