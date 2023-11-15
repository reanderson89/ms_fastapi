from typing import Optional
from pydantic import validator
from burp.utils.enums import Cadence, CadenceValue, Status, ProgramType
from burp.models.base_models import BasePydantic
from burp.models.program import ProgramModel



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
