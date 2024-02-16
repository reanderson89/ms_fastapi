from burp.models.base_models import BasePydantic


class RequestHeaders(BasePydantic):
    Cookie: str


class RailsBucketCustomization(BasePydantic):
    id: int


class RailsProgram(BasePydantic):
    id: int


class RailsEmployee(BasePydantic):
    email: str
    first_name: str
    last_name: str


class RailsAchievementData(BasePydantic):
    recipients_emails: list[str]
    note: str


class CreateRewardRequest(BasePydantic):
    employee: RailsEmployee
    bucket_customization: RailsBucketCustomization
    program: RailsProgram
    subject: str
    memo: str
    company_values: list[str]
    share_achievement_data: RailsAchievementData
    sending_managers_account_id: int
