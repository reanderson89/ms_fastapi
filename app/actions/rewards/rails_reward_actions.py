import os
from fastapi.exceptions import HTTPException
from datetime import datetime, timezone
from app.actions.http.rails_api_requests import HttpRequests as RailsRequests
from burp.models.reward import ProgramRuleModelDB
from app.models.rails.requests_models import (
    RailsEmployee,
    RailsProgram,
    RailsBucketCustomization,
    RailsAchievementData,
    CreateRewardRequest
)
from burp.models.reward import StagedRewardModelDB
from burp.utils.auth_utils import access_token_creation
from requests.models import Response
from app.worker.logging_format import init_logger

logger = init_logger()

# used for local development and testing
MOCK = os.environ.get("MOCK", "False").lower() == "true"


TOKEN_DATA = {
    "exp": 1707430772,
    "company_gid": "6cdcf917-a0da-4445-93ec-d51d662c60c6",
    "sub": "dd3085e2-a6bd-4339-a7bb-9d06c0132c34",
    "scp": "account",
    "aud": None,
    "iat": 1707171572,
    "jti": "de9829d5-cf97-4ad0-aa46-278bcc3fd27c"
}

class RailsRewardActions:

    @classmethod
    async def handle_delete_rails_rewards(cls, staged_rewards: list, current_managers_account_id: int, updated_rule: ProgramRuleModelDB):
        reward_ids = [reward.reward_id for reward in staged_rewards]
        current_time_utc = datetime.now(timezone.utc)
        formatted_time = current_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        body = {
            "reward":{
                "deletion_reason": "Milestones rule has been updated",
                "deletion_requested_at": formatted_time,
                "deletion_approver_id": current_managers_account_id,
                "reward_ids": reward_ids,
                "milestones": True
            }
        }
        if MOCK:
            delete_response = Response()
            delete_response.status_code = 200
        else:
            delete_response = await RailsRequests.patch(f"/api/v4/rewards/bulk_delete", await cls.get_headers(), body)

        if delete_response.status_code != 207:
            raise HTTPException(status_code=delete_response.status_code, detail="The staged rewards and rails rewards for the updated rule were not deleted")
        delete_response = delete_response.json()
        # rails_reward_ids = [response['reward'] for response in delete_response]
        # # Create a set for faster membership testing
        # rails_reward_ids_set = set(rails_reward_ids)
        # # Collect ids with status != "ok" from delete_response
        # failed_deletion_ids = {response['reward'] for response in delete_response if response["status"] != "ok"}
        # for reward_id in reward_ids:
        #     # Check if the reward_id is not in rails_reward_ids or deletion failed
        #     if reward_id not in rails_reward_ids_set or reward_id in failed_deletion_ids:
        #         await cls.update_staged_reward(reward_id, updated_rule.company_id, updated_rule.rule_uuid, StagedRewardUpdate(state=RewardState.INACTIVE))


    @staticmethod
    async def get_headers():
        jwt = await access_token_creation(TOKEN_DATA, True)
        headers = {
            "Cookie": f"stagingJwtToken={jwt['access_token']}"
        }
        return headers
    
    @classmethod
    async def create_rails_reward_body(cls, staged_reward: StagedRewardModelDB, program_rule: ProgramRuleModelDB):
            employee = RailsEmployee(
                email=staged_reward.email,
                first_name=staged_reward.first_name,
                last_name=staged_reward.last_name
            )
            bucket_customization = RailsBucketCustomization(
                id=program_rule.bucket_customization_id
            )
            program = RailsProgram(
                id=program_rule.sending_managers_program_id
            )
            share_achievement_data = RailsAchievementData(
                recipients_emails=[staged_reward.email],
                note=program_rule.recipient_note
            )
            create_reward = CreateRewardRequest(
                employee=employee,
                bucket_customization=bucket_customization,
                program=program,
                subject=program_rule.subject,
                memo=program_rule.memo,
                share_achievement_data=share_achievement_data,
                company_values=program_rule.company_values,
                sending_managers_account_id=program_rule.sending_managers_account_id,
                staged_reward_uuid=staged_reward.uuid
            )

            return create_reward
            # return await RailsRequests.post(
            #     path="/api/v4/new/endpoint",
            #     headers=await cls.get_headers(),
            #     body=create_reward.dict()
            # )