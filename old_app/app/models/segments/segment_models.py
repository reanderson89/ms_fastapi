from typing import Optional
from pydantic import validator
from burp.utils.enums import Status
from burp.models.base_models import BasePydantic
from burp.models.segment import SegmentModel


class SegmentResponse(SegmentModel):
    pass


class SegmentUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    budget_9char: Optional[str]
    status: Optional[Status]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentCreate(BasePydantic):
    budget_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    status: Optional[Status]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentDelete(BasePydantic):
    ok: bool
    Deleted: SegmentModel
