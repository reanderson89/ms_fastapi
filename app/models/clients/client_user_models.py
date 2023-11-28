from typing import Optional
from pydantic import validator
from burp.utils.enums import Admin
from burp.models.base_models import BasePydantic
from burp.models.user import UserModel
# from burp.models.user_service import ServiceID
from burp.models.client_user import ClientUserModel
# from tests.conftest import service


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

    @validator("admin", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class CreateClientUser(BasePydantic):
    # Client User fields
    user_uuid: Optional[str]
    client_uuid: Optional[str]
    manager_uuid: Optional[str]
    employee_id: Optional[str]
    title: Optional[str]
    department: Optional[str]
    active: Optional[bool]
    time_created: Optional[str]
    time_updated: Optional[str]
    time_hire: Optional[str]
    time_start: Optional[str]
    admin: Optional[Admin]
    # User fields
    first_name: str
    last_name: str
    # latidude: Optional[int]
    # longitude: Optional[int]
    time_birthday: Optional[str]
    # Service fields
    email_address: Optional[str]
    work_email: Optional[str]
    cell: Optional[str]
    # service_uuid: Optional[ServiceID] # service type: "email" or "cell"
    # service_user_id: str # actual email or phone number value

    @validator("admin", pre=False)
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

    @validator("admin", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientUserExpand(ClientUserModel):
    user: Optional[UserModel]
    # user_service: Optional[dict]


class ClientUserDelete(BasePydantic):
    ok: bool
    Deleted: ClientUserModel
