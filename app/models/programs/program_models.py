from typing import Optional
from pydantic import validator
from sqlalchemy.orm import Mapped, mapped_column
from app.enums import Cadence, CadenceValue, Status, ProgramType
from app.models.base_class import Base, BasePydantic


class ProgramModelDB(Base):
    __tablename__ = "program"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    user_uuid: Mapped[str] = mapped_column(default=None, index=True)
    program_9char: Mapped[str] = mapped_column(default=None, index=True)
    name: Mapped[str] = mapped_column(default=None, index=True)
    description: Mapped[str] = mapped_column(default=None, index=True)
    client_uuid: Mapped[str] = mapped_column(default=None, index=True)
    budget_9char: Mapped[str] = mapped_column(default=None, index=True)
    status: Mapped[int] = mapped_column(default=None, index=True)
    program_type: Mapped[int] = mapped_column(default=None, index=True)
    cadence: Mapped[int] = mapped_column(default=None, index=True)
    cadence_value: Mapped[int] = mapped_column(default=None, index=True)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)


class ProgramModel(BasePydantic):
    uuid: Optional[str]
    user_uuid: Optional[str]
    program_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    client_uuid: Optional[str]
    budget_9char: Optional[str]
    status: Optional[Status]
    program_type: Optional[ProgramType]
    cadence: Optional[Cadence]
    cadence_value: Optional[CadenceValue]
    time_created: Optional[int]
    time_updated: Optional[int]


class ProgramResponse(ProgramModel):
    pass


class ProgramCreate(BasePydantic):
    user_uuid: str
    name: str
    description: Optional[str]
    budget_9char: Optional[str]
    status: Optional[Status]
    program_type: Optional[ProgramType]
    cadence: Cadence
    cadence_value: Optional[CadenceValue]

    @validator(
            "status",
            "program_type",
            "cadence",
            "cadence_value",
            pre=False
        )
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ProgramUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    budget_9char: Optional[str]
    status: Optional[Status]
    program_type: Optional[ProgramType]
    cadence: Optional[Cadence]
    cadence_value: Optional[CadenceValue]

    @validator(
            "status",
            "program_type",
            "cadence",
            "cadence_value",
            pre=False
        )
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ProgramDelete(BasePydantic):
    ok: bool
    Deleted: ProgramModel
