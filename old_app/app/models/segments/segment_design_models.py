from typing import Optional
from pydantic import validator
from burp.utils.enums import ChannelType, Status
from burp.models.base_models import BasePydantic
from burp.models.segment_design import SegmentDesignModel


class SegmentDesignResponse(SegmentDesignModel):
    pass


class SegmentDesignCreate(BasePydantic):
    message_uuid: Optional[str]
    channel: Optional[ChannelType]
    status: Optional[Status]

    @validator("status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentDesignUpdate(BasePydantic):
    channel: Optional[ChannelType]
    status: Optional[Status]

    @validator("status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentDesignDelete(BasePydantic):
    ok: bool
    Deleted: SegmentDesignModel
