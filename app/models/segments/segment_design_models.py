from typing import Optional
from pydantic import validator
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import ChannelType, Status
from app.models.base_class import Base, BasePydantic

class SegmentDesignModelDB(Base):
    __tablename__ = "program_segment_design"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    client_uuid: Mapped[str] = mapped_column(default=None, index=True)
    program_9char: Mapped[str] = mapped_column(default=None, index=True)
    segment_9char: Mapped[str] = mapped_column(default=None, index=True)
    design_9char: Mapped[str] = mapped_column(default=None, index=True)
    message_uuid: Mapped[str] = mapped_column(default=None, index=True)
    program_uuid: Mapped[str] = mapped_column(default=None, index=True)
    channel: Mapped[int] = mapped_column(default=None, index=True)
    status: Mapped[int] = mapped_column(default=None, index=True)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)


class SegmentDesignModel(BasePydantic):
    uuid: str
    client_uuid: str
    program_9char: str
    segment_9char: str
    design_9char: str
    program_uuid: Optional[str]
    message_uuid: Optional[str]
    channel: Optional[ChannelType]
    status: Optional[Status]
    time_created: Optional[int]
    time_updated: Optional[int]


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
