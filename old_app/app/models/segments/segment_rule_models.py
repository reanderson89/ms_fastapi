from typing import Optional
from pydantic import validator
from burp.utils.enums import RuleType, Status
from burp.models.base_models import BasePydantic
from burp.models.segment_rule import SegmentRuleModel


class SegmentRuleResponse(SegmentRuleModel):
    pass


class SegmentRuleUpdate(BasePydantic):
    status: Optional[Status]
    rule_type: Optional[RuleType]
    logic: dict

    @validator("rule_type", "status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentRuleCreate(BasePydantic):
    status: Optional[Status]
    rule_type: Optional[RuleType]
    logic: Optional[dict]

    @validator("rule_type", "status", pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class SegmentRuleDelete(BasePydantic):
    ok: bool
    Deleted: SegmentRuleModel
