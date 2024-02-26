import os
from time import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette import status
from datetime import datetime, timezone

from app.actions.rewards.rails_reward_actions import RailsRewardActions
from app.actions.rewards.staged_reward_actions import StagedRewardActions
from app.models.reward.reward_models import StagedRewardUpdate, RewardState, RailsCreateRewardResponse
from app.actions.rules.rule_actions import RuleActions
from burp.models.reward import ProgramRuleModelDB, StagedRewardModelDB
from app.actions.http.rails_api_requests import HttpRequests as RailsRequests
from app.worker.logging_format import init_logger
from app.worker.temp_worker import TempWorker

logger = init_logger()

# used for local development and testing
MOCK = os.environ.get("MOCK", "False").lower() == "true"
# if MOCK:
#     rewards_sent = None


class CronActions:

    @staticmethod
    async def handle_staged_reward_state_update(reward: StagedRewardModelDB, rails_response: RailsCreateRewardResponse):
        if rails_response.sent:
            update_model = StagedRewardUpdate(reward_id=rails_response.reward_id, approved_at=int(time()), state=RewardState.SENT.value)
        else:
            update_model = StagedRewardUpdate(reward_id=rails_response.reward_id, state=RewardState.FAILED_TO_SEND.value)
        return await StagedRewardActions.update_staged_reward(
            reward.uuid,
            reward.company_id,
            reward.rule_uuid,
            update_model
        )

    # @classmethod
    # async def handle_send_rails_reward_job(cls, reward: StagedRewardModelDB, rule: ProgramRuleModelDB):
    #     retry_attempts = 2
    #     for attempt in range(retry_attempts):
    #         try:
    #             response = await RailsRewardActions.rails_reward_request(reward, rule)
    #             if response.status_code == 200:
    #                 response = SendStagedRewardResponse(**response.json())
    #                 return await cls.handle_staged_reward_state_update(reward, response, True)
    #             else:
    #                 logger.milestone(f"Failed attempt {attempt+1} for reward {reward.uuid} with status {response.status_code}")
    #         except Exception as e:
    #             logger.milestone(f"Exception on attempt {attempt+1} for reward {reward.uuid}: {e}")
    #         if attempt < retry_attempts - 1:
    #             await asyncio.sleep(2 ** attempt)
    #     # Handle failure after all retries here
    #     response = SendStagedRewardResponse(**response.json())
    #     await cls.handle_staged_reward_state_update(reward, response, False)

    @classmethod
    async def send_staged_rewards(cls):
        now_utc = datetime.now(timezone.utc)
        today = now_utc.strftime("%Y-%m-%d")
        current_hour = now_utc.hour
        todays_staged_rewards = await StagedRewardActions.get_staged_rewards_by_date_and_time(today, current_hour)
        if not todays_staged_rewards:
            return

        temp_worker = TempWorker()
        staged_rewards_by_rule = defaultdict(list)
        for reward in todays_staged_rewards:
            staged_rewards_by_rule[reward.rule_uuid].append(reward)
        for rule_uuid, staged_rewards in staged_rewards_by_rule.items():
            company_id = staged_rewards[0].company_id
            rule = await RuleActions.get_program_rule(company_id, rule_uuid)
            for reward in staged_rewards:
                await StagedRewardActions.update_staged_reward(reward.uuid, company_id, rule.uuid, StagedRewardUpdate(state=RewardState.QUEUED.value))
                rails_reward_create_model = await RailsRewardActions.create_rails_reward_body(reward, rule)
                await temp_worker.send_rails_reward_job(rails_reward_create_model, MOCK)
                # await cls.handle_rails_reward_request(reward, rule)

    @classmethod
    async def rails_send_rewards(cls, staged_reward: StagedRewardModelDB, rule: ProgramRuleModelDB, company_id: int, sendable_id: int):
        type = rule.rule_type

        # Just for logging purposes
        user_uuid = staged_reward.user_account_uuid
        user_uuid_display = (str(user_uuid)[:6] + '...') if len(str(user_uuid)) > 6 else str(user_uuid)
        print(f"Sending {type} reward to account {user_uuid_display} from company {company_id}")

        # if MOCK:
        #     next(cls.rewards_sent)
        #     return
        return await RailsRequests.put(path=f"/api/v4/requests/{sendable_id}/send", headers=await RailsRewardActions.get_headers())

    @staticmethod
    async def authenticate(request: Request):
        if request.headers.get("authorization").split(" ")[1]:
            token = request.headers.get("authorization").split(" ")[1]
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token and/or user-agent"
            )

        user_agent = request.headers.get("user-agent")
        if token == os.environ.get("CRON_TOKEN") and user_agent == "milestones-cron-send-rewards":
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token and/or user-agent"
            )
