import os
import asyncio
from itertools import count
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette import status
from datetime import datetime, timedelta, timezone

from app.actions.rewards.rails_reward_actions import RailsRewardActions
from app.actions.rewards.staged_reward_actions import StagedRewardActions
from app.actions.rules.rule_actions import RuleActions
from burp.models.reward import ProgramRuleModelDB, StagedRewardModelDB
from app.actions.http.rails_api_requests import HttpRequests as RailsRequests


# used for local development and testing
MOCK = os.environ.get("MOCK", "False").lower() == "true"
if MOCK:
    rewards_sent = None


class CronActions:

    @classmethod
    async def send_rewards(cls):
        if MOCK:
            sendable_lookup = defaultdict(int)
            cls.rewards_sent = count()
        else:
            sendable_awards = (await RailsRequests.get("/api/v4/sendables/requested", await RailsRewardActions.get_headers())).json()['approved']
            sendable_lookup = {sendable['rewardable_id']: sendable['id'] for sendable in sendable_awards}

        company_ids: list = await RuleActions.get_distinct_company_ids()

        for company_id in company_ids:
            # get all companies reward rules
            program_rules: list[ProgramRuleModelDB] = await RuleActions.get_program_rules_by_company(company_id)

            # Loop through program_rules and determine which scheduled rewards match the rule
            for rule in program_rules:
                today = datetime.now(timezone(timedelta(hours=-8))).strftime("%m-%d-%y")
                staged_rewards = await StagedRewardActions.get_staged_rewards_by_date(rule.uuid, today)

                if staged_rewards:
                    sendable_rewards = []
                    # Loops through the rewards and checks their reward_id against the reward_id's from the sendable_awards.
                    for i, reward in enumerate(staged_rewards):
                        # Add every other reward_id to sendable_lookup
                        if MOCK and i % 2 == 0:
                            sendable_lookup[reward.reward_id] = reward.reward_id
                        if reward.reward_id in sendable_lookup:
                            reward.sendable_id = sendable_lookup[reward.reward_id]
                            sendable_rewards.append(reward)
                    # Send rewards to users
                    responses = await asyncio.gather(*(cls.rails_send_rewards(user_reward, rule, company_id) for user_reward in sendable_rewards))
                else:
                    print(f"No rewards scheduled for today for rule {rule.uuid}")
        if MOCK:
            return next(cls.rewards_sent)
        return True

    @classmethod
    async def rails_send_rewards(cls, staged_reward: StagedRewardModelDB, rule: ProgramRuleModelDB, company_id: int):
        type = rule.rule_type

        # Just for logging purposes
        user_uuid = staged_reward.user_account_uuid
        user_uuid_display = (str(user_uuid)[:6] + '...') if len(str(user_uuid)) > 6 else str(user_uuid)
        print(f"Sending {type} reward to account {user_uuid_display} from company {company_id}")

        if MOCK:
            next(cls.rewards_sent)
            return
        return await RailsRequests.put(path=f"/api/v4/requests/{staged_reward.sendable_id}/send", headers=await RailsRewardActions.get_headers())

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
