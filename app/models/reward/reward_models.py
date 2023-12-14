from typing import Optional
from burp.models.base_models import BasePydantic
from burp.models.reward import RewardModel


class Rule(BasePydantic):
    program_cadence: Optional[str]
    user_birthdate: Optional[int]
    anniversary: Optional[int]
    employment_date: Optional[int]
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


class RewardInfo(BasePydantic):
    award_type: Optional[str]
    sending_managers_account_id: Optional[int]
    sending_managers_program_id: Optional[int]
    bucket_customization: Optional[int]
    subject: Optional[str]


# ver. 1a reward create
class RewardCreate(BasePydantic):
    sending_managers_account_id: int
    sending_managers_program_id: int
    bucket_customization_id: int
    subject: str
    memo: str
    company_values: list[str]
    recipient_emails: list[str]
    recipient_note: str

# ver. 1b reward create
# class RewardCreate(BasePydantic):
#     company_id: int
#     client_admin_id: int
#     rule: Rule
#     users: list[User]
#     reward_info: RewardInfo


class BaseRewardModel(BasePydantic):
    uuid: str
    client_admin_id: int
    company_id: int
    rule: Rule
    reward_info: RewardInfo


class RewardResponse(BasePydantic):
    reward_info: dict


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
    Deleted: RewardModel
