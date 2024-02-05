from enum import Enum
from typing import Optional
from burp.models.base_models import BasePydantic
from burp.models.reward import ProgramRuleModel
from pydantic import validator


class RuleType(Enum):
    ANNIVERSARY = "ANNIVERSARY"
    ONBOARDING = "ONBOARDING"
    BIRTHDAY = "BIRTHDAY"


class Cadence(Enum):
    RECURRING = "RECURRING"
    NON_RECURRING = "NON_RECURRING"


class CadenceType(Enum):
    NA = "NA"
    YEAR = "YEAR"
    MONTH = "MONTH"
    WEEK = "WEEK"
    DAY = "DAY"


class TimingType(Enum):
    DAY_OF = "DAY_OF"
    WEEKDAY_MONTH = "WEEKDAY_MONTH"  # first weekday of the month of the milestone
    WEEKDAY_WEEK = "WEEKDAY_WEEK"  # first weekday of the week of the milestone
    DAYS_PRIOR = "DAYS_PRIOR"  # x days prior to the milestone TODO: requires an extra field to handle this


# TODO: Review optional fields. What are the minimum req fields to create a program rule?
class ProgramRuleCreate(BasePydantic):
    company_id: int
    rule_name: str
    rule_type: RuleType
    trigger_field: Optional[str]
    timing_type: Optional[TimingType]
    days_prior: Optional[int]
    sending_time: Optional[str]
    timezone: Optional[str]
    manager_id: Optional[int]
    sending_managers_account_id: Optional[int]
    sending_managers_program_id: Optional[int]
    bucket_customization_id: Optional[int]
    bucket_customization_price: Optional[int]
    subject: Optional[str]
    memo: Optional[str]
    recipient_note: Optional[str]
    company_values: Optional[list[str]]
    segmented_by: Optional[list[dict]]
    created_by: Optional[int]
    updated_by: Optional[int]
    anniversary_years: Optional[list[int]] = None
    onboarding_period: Optional[int] = None

      # Validators to ensure `anniversary_years` and `onboarding_period` are provided when required
    @validator('anniversary_years', always=True)
    def check_anniversary_years(cls, v, values):
        if values.get('rule_type') == RuleType.ANNIVERSARY.value and not v:
            raise ValueError('anniversary_years is required when rule_type is ANNIVERSARY')
        return v

    @validator('onboarding_period', always=True)
    def check_onboarding_period(cls, v, values):
        if values.get('rule_type') == RuleType.ONBOARDING.value and not v:
            raise ValueError('onboarding_period is required when rule_type is ONBOARDING')
        return v

    @validator('days_prior', always=True)
    def check_days_prior(cls, v, values):
        if values.get('timing_type') == TimingType.DAYS_PRIOR.value and not v:
            raise ValueError('days_prior is required when timing_type is DAYS_PRIOR')
        return v

    @validator("rule_type", "timing_type", pre=False)
    def validate_award_type(cls, v):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, Enum):
            return v.value


class ProgramRuleResponse(ProgramRuleModel):
    pass


class ProgramRuleUpdate(BasePydantic):
    company_id: Optional[int]
    rule_name: Optional[str]
    rule_type: Optional[RuleType]
    trigger_field: Optional[str]
    timing_type: Optional[TimingType]
    sending_time: Optional[str]
    timezone: Optional[str]
    manager_id: Optional[int]
    sending_managers_account_id: Optional[int]
    sending_managers_program_id: Optional[int]
    bucket_customization_id: Optional[int]
    subject: Optional[str]
    memo: Optional[str]
    recipient_note: Optional[str]
    company_values: Optional[list[str]]
    updated_by: Optional[int]

    @validator("rule_type", "timing_type", pre=False)
    def validate_award_type(cls, v):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, Enum):
            return v.value


class ProgramRuleRewardCountResponse(BasePydantic):
    staged_rewards: int
    company_id: int
    rule_uuid: str

class ProgramRuleDelete(BasePydantic):
    ok: bool
    Deleted: Optional[ProgramRuleModel]


class State(Enum):
    APPROVING = "APPROVING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SENT = "SENT"
    REMOVED = "REMOVED"
    HARD_DELETED = "HARD_DELETED"
    # --Please Note--
    # The 'state' column in the Rails 'rewards' table includes the following
    # additional states not represented in this enum class: 'scheduling',
    # 'redeemed', 'rejected_notification', 'completed', and 'scheduled'.
    # Ensure synchronization if these states are utilized.


class StagedRewardCreate(BasePydantic):
    reward_id: int
    user_account_uuid: str
    rule_uuid: str
    send_on: str
    employee_id: int
    company_values_showcased: list[str]
    company_id: int
    state: State
    approved_at: str
    program_id: int
    employee_account_id: int
    gid: str

    @validator("state", pre=True)
    def validate_case(cls, v):  # pylint: disable=no-self-argument,no-self-use
        return v.upper()

    @validator("state", pre=False)
    def validate_value(cls, v):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, Enum):
            return v.value


class SegmentRuleCreate(BasePydantic):
    parent_rule: str
    segmented_by: dict[str, str]
    bucket_customization_id: int
