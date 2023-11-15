from typing import Optional
from pydantic import validator
from burp.utils.enums import RuleType, Status
from burp.models.base_models import BasePydantic
from burp.models.program_rule import ProgramRuleModel


class ProgramRuleResponse(ProgramRuleModel):
    pass


class ProgramRuleUpdate(BasePydantic):
    rule_type: Optional[RuleType]
    status: Optional[Status]
    logic: Optional[dict]

    @validator("rule_type", "status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ProgramRuleCreate(BasePydantic):
    rule_type: Optional[RuleType]
    status: Optional[Status]
    logic: dict

    @validator("rule_type", "status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ProgramRuleDelete(BasePydantic):
    ok: bool
    Deleted: ProgramRuleModel
