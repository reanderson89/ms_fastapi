from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic


class UserModelDB(Base):
    __tablename__ = "user"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(default=None)
    last_name: Mapped[str] = mapped_column(default=None)
    latitude: Mapped[int] = mapped_column(default=None)
    longitude: Mapped[int] = mapped_column(default=None)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)
    time_ping: Mapped[int] = mapped_column(default=None)
    time_birthday: Mapped[int] = mapped_column(default=None)
    admin: Mapped[int] = mapped_column(default=0)
    # TODO: Not part of v1.0, but may be added in future iteration.
    # Just a standin for now.
    # client_uuid_list: Mapped[str] = mapped_column(default=None)


class UserBase(BasePydantic):
    uuid: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    latitude: Optional[int]
    longitude: Optional[int]
    time_created: Optional[int]
    time_updated: Optional[int]
    time_ping: Optional[int]
    time_birthday: Optional[int]
    admin: Optional[int]
    # client_uuid_list: Optional[list]


class UserUpdate(BasePydantic):
    first_name: Optional[str]
    last_name: Optional[str]
    latitude: Optional[int]
    longitude: Optional[int]
    time_birthday: Optional[int]
    admin: Optional[int]


# class UserAdminUpdate(BasePydantic):
#   client_uuid_list: Optional[list]


class UserExpanded(UserBase):
    services: Optional[dict] = None
