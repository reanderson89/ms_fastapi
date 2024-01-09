import os
import asyncio
from fastapi import Request, HTTPException
from starlette import status
from datetime import datetime, timedelta, timezone

from app.actions.rewards.reward_actions import RewardActions
from burp.models.reward import RewardModelDB
from app.actions.http.rails_api_requests import HttpRequests as RailsRequests

# Imports from commented out methods
# import pandas as pd
# from sqlalchemy import select
# from sqlalchemy.orm import Session
# from app.database.config import engine
# from app.exceptions import ExceptionHandling
# from burp.models.client_user import ClientUserModelDB
# from burp.models.user import UserModelDB


class CronActions:

    @classmethod
    async def send_rewards(cls):
        sendable_awards = (await RailsRequests.get("/api/v4/sendables/requested", await RewardActions.get_headers())).json()['approved']
        # reward["id"] in this loop is actually the sendable_id
        sendable_lookup = {sendable['rewardable_id']: sendable['id'] for sendable in sendable_awards}
        company_ids: list = await RewardActions.get_distinct_company_ids()

        for company_id in company_ids:
            # get all companies reward rules
            rewards: list[RewardModelDB] = await RewardActions.get_rewards_by_company(company_id)

            # Loop through rewards and determine which users match the rule
            for reward in rewards:
                today = datetime.now(timezone(timedelta(hours=-8))).strftime("%m-%d-%y")
                rewards_by_date = reward.users

                # Check if there are any users with a reward for today
                if rewards_by_date and today in rewards_by_date:
                    users = rewards_by_date[today]

                    # Loops through the users and checks their reward_id against the reward_id's from the sendable_awards.
                    sendable_users = []
                    # Iterate through users to update 'sendable_id'
                    for user in users:
                        reward_id = user['reward']['id']
                        if reward_id in sendable_lookup:
                            user['reward']['sendable_id'] = sendable_lookup[reward_id]
                            sendable_users.append(user)
                    # Send rewards to users
                    responses = await asyncio.gather(*(cls.rails_send_rewards(user, reward, company_id) for user in sendable_users))
                    # return responses

    @classmethod
    async def rails_send_rewards(cls, user: dict, reward: RewardModelDB, company_id: int):
        type = reward.rule["rule_type"]
        name = f"{user['first_name']} {user['last_name']}"

        print(f"Sending {type} reward to {name} from company {company_id}")

        # return await RailsRequests.put(path=f"/api/v4/requests/22436/send", headers=await RewardActions.get_headers())
        return await RailsRequests.put(path=f"/api/v4/requests/{user['reward']['sendable_id']}/send", headers=await RewardActions.get_headers())

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

    # @classmethod
    # async def kick_off(cls):
    #     users = await cls.get_all_cron(UserModelDB)
    #     client_users = await cls.get_all_cron(ClientUserModelDB)
    #     client_users_df = pd.DataFrame(client_users)
    #     users_df = pd.DataFrame(users)
    #     df = pd.merge(client_users_df, users_df, left_on="user_uuid", right_on="uuid")
    #     result = await cls.run_rule(df, rule)

    #     return result

    # @classmethod
    # async def get_all_cron(cls, model):
    #     with Session(engine) as session:
    #         query = select(model)
    #         db_query = session.scalars(query).all()
    #         await ExceptionHandling.check404(db_query)
    #         return db_query

    # @classmethod
    # async def run_rule(cls, df, rul):
    #     rule_list = rul["conditions"]

    #     today = datetime.now()
    #     today = datetime.fromtimestamp(int(today.timestamp()))

    #     df["check_day"] = df["time_start"].apply(
    #         lambda x: int(datetime.fromtimestamp(x).strftime("%d%m"))
    #     )
    #     df["check_year"] = df["time_start"].apply(
    #         lambda x: int(datetime.fromtimestamp(x).strftime("%Y"))
    #     )

    #     for rule in rule_list:
    #         match rule["var"]:
    #             case "hire_anniversary":
    #                 df = await cls.hire_anniversary(df, rule, today)
    #             case "anniversary_value":
    #                 df = await cls.anniversary_value(df, rule, today)
    #             case _:
    #                 print("not found")

    #     return df.to_dict("index")

    # @classmethod
    # async def hire_anniversary(cls, df, rule, today):
    #     today_string = today.strftime("%d%m")
    #     df = df[df["check_day"] == int(today_string)]
    #     return df

    # @classmethod
    # async def anniversary_value(cls, df, rule, today):
    #     year_string = today.strftime("%Y")
    #     df = df[df["check_year"] == int(year_string)]
    #     return df


# rule = {
#     "conditions": [
#         {"var": "hire_anniversary", "operator": "=", "value": "today"},
#         {"var": "anniversary_value", "operator": "=", "value": "0"},
#     ],
#     "details": {
#         "award_type": "1",
#         "client_award": "client_award_uuid",
#         "program_award": "program_award_uuid",
#         "message": "message_uuid",
#     },
# }
