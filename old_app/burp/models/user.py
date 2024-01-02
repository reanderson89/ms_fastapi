from typing import Optional

from pydantic import validator
from sqlalchemy import String
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column

from burp.models.base_models import Base, BasePydantic
from burp.utils.enums import Admin

Integer = mysql.INTEGER


class UserModelDB(Base):
    __tablename__ = "user"

    uuid: Mapped[str] = mapped_column(String(56), default=None, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    latitude: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    longitude: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_ping: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_birthday: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    admin: Mapped[int] = mapped_column(Integer(11), default=0, nullable=True)
    auth_code: Mapped[int] = mapped_column(Integer(4), default=0, nullable=True)
    # TODO: Not part of v1.0, but may be added in future iteration.
    # Just a standin for now.
    # client_uuid_list: Mapped[str] = mapped_column(String(56), default=None)


class UserModel(BasePydantic):
    uuid: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    latitude: Optional[int]
    longitude: Optional[int]
    time_created: Optional[int]
    time_updated: Optional[int]
    time_ping: Optional[int]
    time_birthday: Optional[int]
    admin: Optional[Admin]
    auth_code: Optional[int]
    # client_uuid_list: Optional[list]

    @validator("admin", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value
