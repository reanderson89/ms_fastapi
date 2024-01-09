from enum import Enum
from typing import Optional
from burp.models.base_models import BasePydantic
from burp.models.reward import RewardModel
from pydantic import validator


class RuleType(Enum):
    BIRTHDAY = 1
    HIRE_DATE = 2
    ONBOARDING_DATE = 3


class Cadence(Enum):
    RECURRING = 1
    NON_RECURRING = 2


class CadenceType(Enum):
    YEAR = 1
    MONTH = 2
    WEEK = 3
    DAY = 4


class TimingType(Enum):
    DAY_OF = 1
    DAY_BEFORE = 2
    DAY_AFTER = 3


class Rule(BasePydantic):
    rule_name: str
    rule_type: RuleType
    cadence: Optional[Cadence] # eventually needs to be required
    cadence_type: Optional[CadenceType] # eventually needs to be required
    cadence_value: Optional[list[int]] # eventually needs to be required
    trigger_field: Optional[str] # eventually needs to be required
    timing_type: Optional[TimingType] # eventually needs to be required
    sending_time: Optional[str] # eventually needs to be required

    @validator("rule_type", "cadence", "cadence_type", "timing_type", pre=False)
    def validate_award_type(cls, v):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(v, Enum):
            return v.value


class RewardInfo(BasePydantic):
    manager_ID: Optional[int]
    sending_managers_account_id: Optional[int]
    sending_managers_program_id: Optional[int]
    bucket_customization: Optional[int]
    subject: Optional[str]
    memo: Optional[str]
    recipient_note: Optional[str]
    company_values: Optional[list[str]]


class RewardUser(BasePydantic):
    user_birthdate: Optional[int]
    employment_date: Optional[int]
    manager_ID: Optional[int]
    department: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    region: Optional[str]
    account_ID: Optional[int]
    # These are all of the fields that come back for each account from the /api/v4/accounts?company=X endpoint
    id: Optional[int]
    gid: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    latest_login: Optional[str]
    deactivated_at: Optional[str]
    email: Optional[str]
    vip: Optional[bool]
    active_role: Optional[str]
    account_company_id: Optional[int]
    account_company_name: Optional[str]
    employee_id: Optional[int]
    programs: Optional[list[dict]]
    active_managers: Optional[list[dict]]


class RewardCreate(BasePydantic):
    company_id: int
    rule: Rule
    reward_info: RewardInfo


class BaseRewardModel(BasePydantic):
    uuid: str
    company_id: int
    rule: Rule
    reward_info: RewardInfo


class RewardResponse(RewardModel):
    users: Optional[dict]


class RuleUpdate(BasePydantic):
    rule_name: str


class RewardInfoUpdate(BasePydantic):
    subject: Optional[str]
    memo: Optional[str]
    recipient_note: Optional[str]
    company_values: Optional[list[str]]


class RewardUpdate(BasePydantic):
    rule: Optional[RuleUpdate]
    reward_info: Optional[RewardInfoUpdate]


class RewardUsersUpdate(BasePydantic):
    company_id: int
    users: dict


class RewardDelete(BasePydantic):
    ok: bool
    Deleted: Optional[RewardModel]
