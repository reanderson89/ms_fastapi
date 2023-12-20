from enum import Enum
from typing import Optional
from burp.models.base_models import BasePydantic
from burp.models.reward import RewardModel


class AnniversaryType(Enum):
    BIRTHDAY = 1
    HIRE_DATE = 2
    ONBOARDING_DATE = 3


class Rule(BasePydantic):
    anniversary_type: AnniversaryType
    program_cadence: Optional[str]
    anniversary: Optional[int]
    manager_ID: Optional[int]
    department: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    region: Optional[str]


class RewardUser(BasePydantic):
    user_birthdate :  Optional[int]
    employment_date : Optional[int]
    manager_ID : Optional[int]
    department : Optional[str]
    city : Optional[str]
    state : Optional[str]
    country : Optional[str]
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


class RewardInfo(BasePydantic):
    award_type: Optional[str]
    sending_managers_account_id: Optional[int]
    sending_managers_program_id: Optional[int]
    bucket_customization: Optional[int]
    subject: Optional[str]
    memo: Optional[str]
    recipient_note: Optional[str]


# ver. 1a reward create
# class RewardCreate(BasePydantic):
#     sending_managers_account_id: int
#     sending_managers_program_id: int
#     bucket_customization_id: int
#     subject: str
#     memo: str
#     company_values: list[str]
#     recipient_emails: list[str]
#     recipient_note: str

# ver. 1b reward create
class RewardCreate(BasePydantic):
    company_id: int
    client_admin_id: int
    rule: Rule
    reward_info: RewardInfo


class BaseRewardModel(BasePydantic):
    uuid: str
    client_admin_id: int
    company_id: int
    rule: Rule
    reward_info: RewardInfo


class RewardResponse(RewardModel):
    users: Optional[list[RewardUser]]


# class RewardResponse(BasePydantic):
#     reward_info: dict


class RewardUpdate(BasePydantic):
    company_id: int
    client_admin_id: Optional[int]
    rule: Optional[Rule]
    users: Optional[list[RewardUser]]
    reward_info: Optional[RewardInfo]


class RewardUsersUpdate(BasePydantic):
    company_id: int
    users: list[RewardUser]


class RewardDelete(BasePydantic):
    ok: bool
    Deleted: Optional[RewardModel]
