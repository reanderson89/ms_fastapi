from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import EventType
from app.models.base_class import Base, BasePydantic

event_types = {
    1: "award", #creating, updating, deleting custom awards
    2: "approval", #decision gate on whether an award can be sent
    3: "notification", #messages
    4: "budget"
}


class ProgramEventModelDB(Base):
    __tablename__ = "program_event"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    program_uuid: Mapped[str] = mapped_column(default=None, index=True)
    client_uuid: Mapped[str] = mapped_column(default=None, index=True)
    program_9char: Mapped[str] = mapped_column(default=None, index=True)
    event_9char: Mapped[str] = mapped_column(default=None, index=True)
    event_type: Mapped[int] = mapped_column(default=None, index=True)
    parent_9char: Mapped[str] = mapped_column(default=None, index=True)
    segment_9char: Mapped[str] = mapped_column(default=None, index=True)
    event_data: Mapped[str] = mapped_column(default=None)
    status: Mapped[int] = mapped_column(default=None, index=True)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)


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
