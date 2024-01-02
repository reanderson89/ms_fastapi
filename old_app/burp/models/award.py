from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from burp.utils.enums import AwardType, ChannelType
from burp.models.base_models import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class AwardModelDB(Base):
    __tablename__ = "award"

    uuid: Mapped[str] = mapped_column(String(56), default=None, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), default=None, index=True, nullable=True)
    description: Mapped[str] = mapped_column(Text, default=None, index=False, nullable=True)
    hero_image: Mapped[str] = mapped_column(String(4), default=None, index=True, nullable=True)
    channel: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    award_type: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    value: Mapped[int] = mapped_column(Integer(11), default=None, index=True, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class AwardModel(BasePydantic):
    uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]
    channel: Optional[ChannelType]
    award_type: Optional[AwardType]
    value: Optional[int]
    time_created: Optional[int]
    time_updated: Optional[int]