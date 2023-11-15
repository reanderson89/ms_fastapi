from typing import Optional
from pydantic import validator
from burp.utils.enums import AwardType, ChannelType
from burp.models.base_models import BasePydantic
from burp.models.award import AwardModel



class AwardResponse(AwardModel):
    pass


class AwardCreate(BasePydantic):
    name: str
    description: Optional[str]
    hero_image: Optional[str]
    channel: Optional[ChannelType]
    award_type: AwardType
    value: int

    @validator('award_type', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class AwardUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]
    channel: Optional[ChannelType]
    award_type: Optional[AwardType]
    value: Optional[int]

    @validator('award_type', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class AwardDelete(BasePydantic):
    ok: bool
    Deleted: AwardModel
