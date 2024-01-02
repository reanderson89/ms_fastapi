from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from burp.models.base_models import Base
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


event_types = {
    1: "award", #creating, updating, deleting custom awards
    2: "approval", #decision gate on whether an award can be sent
    3: "notification", #messages
    4: "budget"
}


class ProgramEventModelDB(Base):
    __tablename__ = "program_event"

    uuid: Mapped[str] = mapped_column(String(72), default=None, primary_key=True, index=True)
    program_uuid: Mapped[str] = mapped_column(String(65), default=None, index=True, nullable=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    program_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    event_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    event_type: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    parent_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    segment_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    event_data: Mapped[str] = mapped_column(Text, default=None, nullable=True)
    status: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)