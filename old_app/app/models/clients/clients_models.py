from typing import Optional
from pydantic import validator
from burp.utils.enums import ClientStatus
from burp.models.base_models import BasePydantic
from burp.models.client import ClientModel



class ClientResponse(ClientModel):
    pass


class ClientExpanded(ClientModel):
    budgets: dict


class ClientCreate(BasePydantic):
    name: str
    description: str
    status: Optional[ClientStatus]
    url: Optional[str]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    status: Optional[ClientStatus]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientDelete(BasePydantic):
    ok: bool
    Deleted: ClientModel
