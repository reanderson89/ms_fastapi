from burp.models.base_models import BasePydantic


class RewardResponse(BasePydantic):
    message = 'Successfully created a Reward'


class RewardCreate(BasePydantic):
    account_id: int
    sender_id: int
    program_id: int
    bucket_customization_id: int
    subject: str
