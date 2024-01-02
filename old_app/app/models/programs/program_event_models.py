from typing import Optional
from burp.utils.enums import EventType
from burp.models.base_models import BasePydantic


class ProgramEventReturn(BasePydantic):
    uuid: str
    program_uuid: Optional[str]
    client_uuid: str
    program_9char: Optional[str]
    event_9char: str
    event_type: Optional[EventType]
    parent_9char: Optional[str]
    segment_9char: Optional[str]
    event_data: Optional[str]
    status: Optional[int] # status code value
    time_created: Optional[int]
    time_updated: Optional[int]


class ProgramEventUpdate(BasePydantic):
    event_type: Optional[int]
    event_data: Optional[str]
    status: Optional[int] # status code value


class ProgramEventCreate(BasePydantic):
    event_type: Optional[int]
    parent_9char: Optional[str]
    segment_9char: Optional[str]
    event_data: Optional[str]
    status: Optional[int] # status code value
