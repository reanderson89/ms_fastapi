from typing import Optional
from pydantic import validator, root_validator
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import Admin
from app.models.base_class import Base, BasePydantic
from app.actions.utils import convert_int_to_date_string


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
    # client_uuid_list: Optional[list]


class UserResponse(UserModel):
    time_birthday: Optional[int|str]

    @validator('time_birthday', pre=False)
    def validate_bday(cls, v):
        if isinstance(v, str):
            return v
        return convert_int_to_date_string(v)


class UserServiceInput(BasePydantic):
    email: Optional[str]
    work_email: Optional[str]
    personal_email: Optional[str]
    cell: Optional[int|str]
    cell_phone: Optional[int|str]
    cell_number: Optional[int|str]


class UserCreate(UserServiceInput):
    first_name: Optional[str]
    last_name: Optional[str]
    latitude: Optional[int]
    longitude: Optional[int]
    time_birthday: Optional[int|str]
    admin: Optional[Admin]
    location: Optional[str]

    @validator('admin', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class UserUpdate(BasePydantic):
    first_name: Optional[str]
    last_name: Optional[str]
    latitude: Optional[int]
    longitude: Optional[int]
    time_birthday: Optional[int]
    admin: Optional[Admin]

    @validator('admin', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


# class UserAdminUpdate(BasePydantic):
#   client_uuid_list: Optional[list]


class UserExpanded(UserModel):
    time_birthday: Optional[int|str]
    services: Optional[dict]

    @root_validator(pre=False)
    def validate_bday(cls, v):
        v['time_birthday'] = convert_int_to_date_string(v["time_birthday"])
        return v


class UserDelete(BasePydantic):
    ok: bool
    Deleted: UserModel
