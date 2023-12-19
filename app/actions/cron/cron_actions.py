import os
import asyncio
# from burp.models import user
from fastapi import Request, HTTPException
from starlette import status
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.actions.rewards.reward_actions import RewardActions
from app.database.config import engine
from app.exceptions import ExceptionHandling
from burp.models.client_user import ClientUserModelDB
from burp.models.reward import RewardModelDB
from burp.models.user import UserModelDB


class CronActions:

    from collections import defaultdict
    from datetime import datetime, timedelta

    @classmethod
    async def send_rewards(cls):
        company_ids: list = await RewardActions.get_distinct_company_ids()

        for id in company_ids:
            rewards: list[RewardModelDB] = await RewardActions.get_rewards_by_company(id)

            # Determine the types of anniversaries present in the rewards
            anniversary_types = {reward.rule["anniversary_type"] for reward in rewards}

            # Create dict only for the present anniversary types
            birthdays = defaultdict(list) if "birthdate" in anniversary_types else None
            hire_dates = defaultdict(list) if "employment_date" in anniversary_types else None
            onboard_dates = defaultdict(list) if "onboarding_date" in anniversary_types else None

            user_accounts = await cls.get_user_accounts(id)

            for account in user_accounts:
                # Parse datetime strings and extract month and day
                birthday = datetime.fromisoformat(account["birthday"]).strftime("%m-%d")
                hired_on_date = datetime.fromisoformat(account["hired_on"])
                hired_on = hired_on_date.strftime("%m-%d")
                onboard_date = (hired_on_date + timedelta(days=90)).strftime("%m-%d")

                # Skip if hired_on date is today
                if hired_on_date.date() == datetime.now().date():
                    continue

                if birthdays is not None:
                    birthdays[birthday].append(account)
                if hire_dates is not None:
                    hire_dates[hired_on].append(account)
                if onboard_dates is not None:
                    onboard_dates[onboard_date].append(account)

            # Loop through rewards and determine which users match the rule
            for reward in rewards:
                today = datetime.now(timezone(timedelta(hours=-8))).strftime("%m-%d")
                match reward.rule["anniversary_type"]:
                    case "employment_date":
                        users = hire_dates.get(today, []) if hire_dates else []
                    case "onboarding_date":
                        users = onboard_dates.get(today, []) if onboard_dates else []
                    case "birthdate":
                        users = birthdays.get(today, []) if birthdays else []

                # Send rewards to users
                await asyncio.gather(*(cls.create_rewards(user, reward, id) for user in users))

        print("Done")

    @classmethod
    async def get_user_accounts(cls, company_id: str):
        # TODO: get user accounts from rails
        accounts = user_accounts["accounts"]
        return accounts

    @classmethod
    async def create_rewards(cls, user, reward, company_id):
        # TODO: logic to check if rules match users
        type = reward.rule["anniversary_type"]
        name = f"{user['first_name']} {user['last_name']}"
        print(f"Creating {type} reward for {name} from company {company_id}")

        # if it matches:
        # reward_create = {}

        # rails_api = os.environ["RAILS_API"]
        # url = f"{rails_api}/rewards/<name_pending>"
        # r = requests.post(url=url, json=reward_create)
        # return r.json()

    @classmethod
    async def kick_off(cls):
        users = await cls.get_all_cron(UserModelDB)
        client_users = await cls.get_all_cron(ClientUserModelDB)
        client_users_df = pd.DataFrame(client_users)
        users_df = pd.DataFrame(users)
        df = pd.merge(client_users_df, users_df, left_on="user_uuid", right_on="uuid")
        result = await cls.run_rule(df, rule)

        return result

    @classmethod
    async def get_all_cron(cls, model):
        with Session(engine) as session:
            query = select(model)
            db_query = session.scalars(query).all()
            await ExceptionHandling.check404(db_query)
            return db_query
        
    @staticmethod
    async def authenticate(request: Request):
        if request.headers.get("authorization"):
            token = request.headers.get("authorization").split(" ")[1]
        else:
            token = None
            
        user_agent = request.headers.get("user-agent")
        if token == os.environ.get("CRON_TOKEN") and user_agent == "milestones-cron-send-rewards":
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token and/or user-agent"
            )

    @classmethod
    async def run_rule(cls, df, rul):
        rule_list = rul["conditions"]

        today = datetime.now()
        today = datetime.fromtimestamp(int(today.timestamp()))

        df["check_day"] = df["time_start"].apply(
            lambda x: int(datetime.fromtimestamp(x).strftime("%d%m"))
        )
        df["check_year"] = df["time_start"].apply(
            lambda x: int(datetime.fromtimestamp(x).strftime("%Y"))
        )

        for rule in rule_list:
            match rule["var"]:
                case "hire_anniversary":
                    df = await cls.hire_anniversary(df, rule, today)
                case "anniversary_value":
                    df = await cls.anniversary_value(df, rule, today)
                case _:
                    print("not found")

        return df.to_dict("index")

    @classmethod
    async def hire_anniversary(cls, df, rule, today):
        today_string = today.strftime("%d%m")
        df = df[df["check_day"] == int(today_string)]
        return df

    @classmethod
    async def anniversary_value(cls, df, rule, today):
        year_string = today.strftime("%Y")
        df = df[df["check_year"] == int(year_string)]
        return df


rule = {
    "conditions": [
        {"var": "hire_anniversary", "operator": "=", "value": "today"},
        {"var": "anniversary_value", "operator": "=", "value": "0"},
    ],
    "details": {
        "award_type": "1",
        "client_award": "client_award_uuid",
        "program_award": "program_award_uuid",
        "message": "message_uuid",
    },
}

# import json
# path = os.path.dirname(os.path.abspath(__file__))
# with open(f"{path}/user_accounts.json") as f:
#     accounts = json.load(f)

now = datetime.now(timezone(timedelta(hours=-8)))

today = now.isoformat()
ninety_days_ago = (now - timedelta(days=90)).isoformat()
one_year_ago = (now - relativedelta(years=1)).isoformat()
three_years_ago = (now - relativedelta(years=3)).isoformat()
twenty_years_ago = (now - relativedelta(years=20)).isoformat()
thirty_five_years_ago = (now - relativedelta(years=35)).isoformat()
just_a_date = datetime(2000, 1, 1, 0, 0).isoformat()

user_accounts = {
    "accounts": [
        {
            "id": 447,
            "gid": "cc0f6d19-65f9-4d27-9341-790a0affe8a7",
            "first_name": "Ashish",
            "last_name": "Bhatnagar",
            "deactivated_at": None,
            "email": "ashish@eventbrite.com",
            "vip": True,
            "account_company_name": "Eventbrite",
            "account_company_id": 2,
            "employee_id": 4,
            "latest_login": "2014-07-14T18:06:06.399862Z",
            "active_role": "manager",
            "programs": [{"id": 29, "name": "Eventbrite Sales Rewards"}],
            "active_managers": [{"id": 6, "program_name": "Eventbrite Sales Rewards"}],
            "birthday": thirty_five_years_ago,
            "hired_on": just_a_date,
        },
        {
            "id": 500,
            "gid": "23a5054a-8e73-4d66-9d40-6b12ac1f317d",
            "first_name": "Tyler",
            "last_name": "Chandler",
            "deactivated_at": None,
            "email": "tchandler@eventbrite.com",
            "vip": False,
            "account_company_name": "Eventbrite",
            "account_company_id": 2,
            "employee_id": 39,
            "latest_login": "2014-10-13T23:33:50.143431Z",
            "active_role": "employee",
            "programs": [],
            "active_managers": [],
            "birthday": just_a_date,
            "hired_on": three_years_ago,
        },
        {
            "id": 501,
            "gid": "91022630-83b1-488a-9ada-4ea9c56f06c4",
            "first_name": "Ali",
            "last_name": "Dockery",
            "deactivated_at": None,
            "email": "adockery@eventbrite.com",
            "vip": False,
            "account_company_name": "Eventbrite",
            "account_company_id": 2,
            "employee_id": 40,
            "latest_login": "2014-10-13T23:51:36.976079Z",
            "active_role": "employee",
            "programs": [],
            "active_managers": [],
            "birthday": thirty_five_years_ago,
            "hired_on": three_years_ago,
        },
        {
            "id": 502,
            "gid": "72975ebf-7532-42f8-9042-f0d40c3e39a0",
            "first_name": "Livia",
            "last_name": "Marati",
            "deactivated_at": None,
            "email": "livia@eventbrite.com",
            "vip": False,
            "account_company_name": "Eventbrite",
            "account_company_id": 2,
            "employee_id": 38,
            "latest_login": "2014-10-13T23:48:20.907779Z",
            "active_role": "employee",
            "programs": [],
            "active_managers": [],
            "birthday": just_a_date,
            "hired_on": one_year_ago,
        },
        {
            "id": 503,
            "gid": "cb2e4a76-c875-4d20-97b1-369978e6f6ca",
            "first_name": "Vanessa",
            "last_name": "Vadas",
            "deactivated_at": None,
            "email": "vadas@eventbrite.com",
            "vip": False,
            "account_company_name": "Eventbrite",
            "account_company_id": 2,
            "employee_id": 41,
            "latest_login": "2014-10-14T00:06:10.436028Z",
            "active_role": "employee",
            "programs": [],
            "active_managers": [],
            "birthday": just_a_date,
            "hired_on": ninety_days_ago,
        },
        {
            "id": 646,
            "gid": "b72012fa-8d79-4ae6-a40a-096c73bb4102",
            "first_name": "Melissa",
            "last_name": "Dempsey",
            "deactivated_at": None,
            "email": "mdempsey@eventbrite.com",
            "vip": False,
            "account_company_name": "Eventbrite",
            "account_company_id": 2,
            "employee_id": 2,
            "latest_login": "2015-08-10T17:23:17.453403Z",
            "active_role": "employee",
            "programs": [],
            "active_managers": [],
            "birthday": just_a_date,
            "hired_on": today,
        },
        {
            "id": 1095,
            "gid": "bddb98d0-d2fa-4214-86fa-6cd61078e342",
            "first_name": "Thomas",
            "last_name": "St. Clair",
            "deactivated_at": None,
            "email": "tstclair@eventbrite.com",
            "vip": False,
            "account_company_name": "Eventbrite",
            "account_company_id": 2,
            "employee_id": 961,
            "latest_login": "2016-05-04T21:25:24.626696Z",
            "active_role": "employee",
            "programs": [],
            "active_managers": [],
            "birthday": twenty_years_ago,
            "hired_on": just_a_date,
        },
    ],
    "meta": {
        "total_entries": 7,
        "current_page": 1,
        "next_page": None,
        "previous_page": None,
        "total_count": 7,
    },
}
