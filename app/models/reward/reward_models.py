from typing import Optional, List
from burp.models.base_models import BasePydantic
from burp.models.reward import RewardModel

class Rule(BasePydantic):
    program_cadence: Optional[str]
    user_birthdate : Optional[int]
    anniversary: Optional[int] 
    employment_date : Optional[int]
    manager_ID : Optional[int]
    department : Optional[str]
    city : Optional[str]
    state : Optional[str]
    country : Optional[str]
    region: Optional[str]

class User(BasePydantic):
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
    award_type : Optional[str]
    sending_managers_account_id: Optional[int]
    sending_managers_program_id: Optional[int]
    bucket_customization: Optional[int]
    subject: Optional[str]

# ver. 1a reward create
class RewardCreate(BasePydantic):
    sending_managers_account_id: int
    sending_managers_program_id: int
    bucket_customization: int
    subject: str

# ver. 1b reward create
# class RewardCreate(BasePydantic):
#     company_id: int
#     client_admin_id: int
#     rule: Rule
#     users: List[User]
#     reward_info: RewardInfo 


class RewardResponse(RewardModel):
    pass

class RewardUpdate(BasePydantic):
    company_id: int
    client_admin_id: int
    rule: Rule
    users: List[User]
    reward_info: RewardInfo

class RewardDelete(BasePydantic):
    ok: bool
    Deleted: RewardModel
