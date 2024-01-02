from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from burp.models.base_models import Base, BasePydantic
from burp.utils.utils import new_9char
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class ProgramAwardModelDB(Base):
    __tablename__ = "program_award"

    uuid: Mapped[str] = mapped_column(String(74), default=None, primary_key=True, index=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    program_9char: Mapped[str] = mapped_column(String(9), default=None, index=None, nullable=True)
    program_award_9char: Mapped[str] = mapped_column(String(9), default=None, index=None, nullable=True)
    client_award_9char: Mapped[str] = mapped_column(String(9), default=None, index=None, nullable=True)
    name: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    description: Mapped[str] = mapped_column(Text, default=None, nullable=True)
    hero_image: Mapped[str] = mapped_column(String(4), default=None, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.program_award_9char:
            self.program_award_9char = new_9char()
        if not self.uuid:
            self.uuid = (self.client_uuid + self.program_9char + self.client_award_9char)


class ProgramAwardModel(BasePydantic):
    uuid: Optional[str]
    client_uuid: Optional[str]
    program_9char: Optional[str]
    program_award_9char: Optional[str]
    client_award_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]
    time_created: Optional[int]
    time_updated: Optional[int]