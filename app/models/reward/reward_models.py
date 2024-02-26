from enum import Enum
from typing import Optional
from burp.models.base_models import BasePydantic
from burp.models.reward import ProgramRuleModel
from pydantic import validator
from burp.models.reward import StagedRewardModel


class RuleType(Enum):
    ANNIVERSARY = "ANNIVERSARY"
    ONBOARDING = "ONBOARDING"
    BIRTHDAY = "BIRTHDAY"


class TimingType(Enum):
    DAY_OF = "DAY_OF"
    WEEKDAY_MONTH = "WEEKDAY_MONTH"  # first weekday of the month of the milestone
    WEEKDAY_WEEK = "WEEKDAY_WEEK"  # first weekday of the week of the milestone
    DAYS_PRIOR = "DAYS_PRIOR"  # x days prior to the milestone


class RuleState(Enum):
    ACTIVE = "ACTIVE"
    DRAFT = "DRAFT"
    INACTIVE = "INACTIVE"


class RewardState(Enum):
    APPROVING = "APPROVING"
    APPROVED = "APPROVED"
    HARD_DELETED = "HARD_DELETED"
    INACTIVE = "INACTIVE"
    REJECTED = "REJECTED"
    REMOVED = "REMOVED"
    SENT = "SENT"
    STAGED = "STAGED"
    FAILED_TO_SEND = "FAILED_TO_SEND"
    QUEUED = "QUEUED"
    # --Please Note--
    # The 'state' column in the Rails 'rewards' table includes the following
    # additional states not represented in this enum class: 'scheduling',
    # 'redeemed', 'rejected_notification', 'completed', and 'scheduled'.
    # Ensure synchronization if these states are utilized.


# TODO: Review optional fields. What are the minimum req fields to create a program rule?
class ProgramRuleCreate(BasePydantic):
    company_id: int
    rule_name: str
    rule_type: RuleType
    trigger_field: str
    timing_type: TimingType
    days_prior: Optional[int]
    sending_time: str
    timezone: str
    manager_id: int
    sending_managers_account_id: int
    sending_managers_program_id: int
    bucket_customization_id: int
    bucket_customization_price: int
    subject: str
    memo: str
    recipient_note: str
    company_values: Optional[list[str]]
    segmented_by: Optional[list[dict]]
    state: RuleState
    created_by: int
    updated_by: Optional[int]
    anniversary_years: Optional[list[int]] = None
    onboarding_period: Optional[int] = None

    # Validators to ensure `anniversary_years` and `onboarding_period` are provided when required
    @validator('anniversary_years', always=True)
    def check_anniversary_years(cls, v, values):  # pylint: disable=no-self-argument,no-self-use
        if values.get('rule_type') == RuleType.ANNIVERSARY.value and not v:
            raise ValueError('anniversary_years is required when rule_type is ANNIVERSARY')
        return v

    @validator('onboarding_period', always=True)
    def check_onboarding_period(cls, v, values):  # pylint: disable=no-self-argument,no-self-use
        if values.get('rule_type') == RuleType.ONBOARDING.value and not v:
            raise ValueError('onboarding_period is required when rule_type is ONBOARDING')
        return v

    @validator('days_prior', always=True)
    def check_days_prior(cls, v, values):  # pylint: disable=no-self-argument,no-self-use
        if values.get('timing_type') == TimingType.DAYS_PRIOR.value and not v:
            raise ValueError('days_prior is required when timing_type is DAYS_PRIOR')
        return v

    @validator("rule_type", "timing_type", pre=False)
    def validate_award_type(cls, v):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, Enum):
            return v.value

    @validator("state", pre=False)
    def validate_state(cls, v):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, Enum):
            if v.value == RuleState.INACTIVE.value:
                raise ValueError('INACTIVE state is not allowed on create')
            return v.value


class ProgramRuleResponse(ProgramRuleModel):
    pass


class ProgramRuleUpdate(BasePydantic):
    rule_name: Optional[str]
    rule_type: Optional[RuleType]
    trigger_field: Optional[str]
    timing_type: Optional[TimingType]
    days_prior: Optional[int]
    sending_time: str
    timezone: str
    manager_id: int
    sending_managers_account_id: int
    sending_managers_program_id: int
    bucket_customization_id: int
    bucket_customization_price: int
    subject: str
    memo: str
    recipient_note: str
    company_values: Optional[list[str]]
    segmented_by: Optional[list[dict]]
    state: Optional[RuleState]
    updated_by: Optional[int]
    anniversary_years: Optional[list[int]] = None
    onboarding_period: Optional[int] = None

    # Validators to ensure `anniversary_years` and `onboarding_period` are provided when required
    @validator('anniversary_years', always=True)
    def check_anniversary_years(cls, v, values):  # pylint: disable=no-self-argument,no-self-use
        if values.get('rule_type') == RuleType.ANNIVERSARY.value and not v:
            raise ValueError('anniversary_years is required when rule_type is ANNIVERSARY')
        return v

    @validator('onboarding_period', always=True)
    def check_onboarding_period(cls, v, values):  # pylint: disable=no-self-argument,no-self-use
        if values.get('rule_type') == RuleType.ONBOARDING.value and not v:
            raise ValueError('onboarding_period is required when rule_type is ONBOARDING')
        return v

    @validator('days_prior', always=True)
    def check_days_prior(cls, v, values):  # pylint: disable=no-self-argument,no-self-use
        if values.get('timing_type') == TimingType.DAYS_PRIOR.value and not v:
            raise ValueError('days_prior is required when timing_type is DAYS_PRIOR')
        return v

    @validator("rule_type", "timing_type", "state", pre=False)
    def validate_award_type(cls, v):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, Enum):
            return v.value

    @validator("state", pre=False)
    def validate_state(cls, v):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, Enum):
            if v.value == RuleState.INACTIVE.value:
                raise ValueError('INACTIVE state is not allowed on update')
            return v.value

class StagedRewardCountResponse(BasePydantic):
    rules: dict[str, int]

class StagedRewardResponse(StagedRewardModel):
    pass


class ProgramRuleDelete(BasePydantic):
    ok: bool
    Deleted: Optional[ProgramRuleModel]


class RailsRewardCreate:
    reward_id: int
    approved_at: str
    state: RewardState


class StagedRewardCreate(BasePydantic):
    user_account_uuid: str
    rule_uuid: str
    send_on: str
    send_at: int
    employee_id: int
    company_id: int
    program_id: int
    # using account_id from user_account
    employee_account_id: int
    # using account_gid from user_account
    gid: str
    bucket_customization_id: int
    bucket_customization_price: int


class StagedRewardUpdate(BasePydantic):
    program_id: Optional[int]
    bucket_customization_id: Optional[int]
    bucket_customization_price: Optional[int]
    state: Optional[RewardState]
    reward_id: Optional[int]
    approved_at: Optional[str]

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


class RailsCreateRewardResponse(BasePydantic):
    staged_reward_uuid: str
    reward_id: Optional[int]
    sent: bool
