from typing import Optional
from pydantic import validator
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import ClientStatus
from app.models.base_class import Base, BasePydantic


class ClientModelDB(Base):
    __tablename__ = "client"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(default=None, index=True)
    url: Mapped[str] = mapped_column(default=None, index=True)
    description: Mapped[str] = mapped_column(default=None, index=True)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)
    time_ping: Mapped[int] = mapped_column(default=None)
    status: Mapped[int] = mapped_column(default=1)


class ClientModel(BasePydantic):
    uuid: Optional[str]
    name: Optional[str]
    url: Optional[str]
    description: Optional[str]
    time_created: Optional[int]
    time_updated: Optional[int]
    time_ping: Optional[int]
    status: Optional[ClientStatus]


class ClientResponse(ClientModel):
    pass


class ClientExpanded(ClientModel):
    budgets: dict


class ClientCreate(BasePydantic):
    name: str
    description: str
    status: Optional[ClientStatus]
    url: Optional[str]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    status: Optional[ClientStatus]

    @validator('status', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientDelete(BasePydantic):
    ok: bool
    Deleted: ClientModel
