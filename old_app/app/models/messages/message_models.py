from typing import Optional
from pydantic import validator
from burp.utils.enums import ChannelType, MessageType, Status
from burp.models.base_models import BasePydantic
from burp.models.message import MessageModel


class MessageResponse(MessageModel):
    pass


class MessageCreate(BasePydantic):
    name: str
    body: Optional[str]
    channel: ChannelType
    message_uuid: Optional[str]
    client_uuid: Optional[str]
    program_9char: Optional[str]
    segment_9char: Optional[str]
    message_type: MessageType
    status: Optional[Status]

    @validator("message_type", "status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class MessageUpdate(BasePydantic):
    name: Optional[str]
    message_type: Optional[MessageType]
    channel: Optional[ChannelType]
    status: Optional[Status]
    body: Optional[str]

    @validator("message_type", "status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class MessageRecipient(BasePydantic):
    client_user_uuid: str
    anniversary: Optional[int]
    award_uuid: str


class MessageSend(BasePydantic):
    client_uuid: str
    recipients: list[MessageRecipient]


class MessageDelete(BasePydantic):
    ok: bool
    Deleted: MessageModel
