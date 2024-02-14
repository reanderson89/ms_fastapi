import asyncio
from app.actions.rules.rule_actions import RuleActions
from app.actions.rewards.staged_reward_actions import StagedRewardActions
from app.models.reward.reward_models import ProgramRuleCreate

import pprint
from faker import Faker

fake = Faker()
company_id = fake.random_int(min=1, max=99)


def generate_user_account(birthday, hired_on):
    return {
        "id": fake.random_int(min=100, max=9999),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "deactivated_at": None,
        "email": fake.email(),
        "birthday": birthday,
        "hired_on": hired_on,
        "account_company_id": company_id,
    }


user_accounts = [
    generate_user_account("1980-02-29T00:00:00", "2020-01-01T00:00:00"),
    generate_user_account("1990-03-01T00:00:00", "2021-01-01T00:00:00"),
    generate_user_account("2000-02-29T00:00:00", "2022-02-28T00:00:00"),  # User has leap year birthday
    generate_user_account("2001-02-28T00:00:00", "2023-02-28T00:00:00"),
    generate_user_account("2002-03-01T00:00:00", "2024-02-29T00:00:00"),  # User hired on leap year
    generate_user_account("2003-01-01T00:00:00", "2025-12-31T00:00:00"),
]

program_rule = ProgramRuleCreate(
    company_id=1,
    rule_type="BIRTHDAY",
    sending_managers_account_id=1,
    sending_managers_program_id=1,
    bucket_customization_id=1,
    subject="Test Subject",
    rule_name= "Test rule"
    trigger_field= "birthday"
    timing_type= "DAY_OF"
    sending_time= "9:00 am"
    timezone= "Pacific Time"
    manager_id= 123
    bucket_customization_price= 500
    memo= "Test memo"
    recipient_note= "Test note"
    state= "ACTIVE"
    created_by= 1234
)



async def main():
    program_rule_db_model = await RuleActions.to_program_rule_db_model(program_rule)

    responses = await StagedRewardActions.create_staged_reward(user_accounts, program_rule_db_model)

    pprint.pprint(responses)
    # print(responses)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
