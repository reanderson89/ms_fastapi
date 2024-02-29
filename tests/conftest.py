import os
from collections import namedtuple
from datetime import datetime
from unittest.mock import patch

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

import tests.testutil as util
from burp.utils.base_crud import BaseCRUD
from app.actions.rewards.staged_reward_actions import StagedRewardActions
from burp.models.reward import ProgramRuleModelDB, StagedRewardModelDB


# from app.worker.temp_worker import TempWorker

# from dotenv import load_dotenv
# load_dotenv()

os.environ["TEST_MODE"] = "True"
# app needs to load after the environment variables
from app.main import app  # noqa


def err_msg(response):
    return f"Response[{response.status_code}]: {response.text} "


def is_deleted(response):
    assert response.status_code == 200


def delete_rule(rule_uuid):
    response = BaseCRUD.non_async_delete_one(
        ProgramRuleModelDB,
        [
            ProgramRuleModelDB.uuid == rule_uuid
        ]
    )
    print(response)


@pytest.fixture(scope="module")
def test_app():
    try:
        client = TestClient(app)
        yield client
    finally:
        pass


@pytest.fixture(scope="function")
def program_rule(test_app: TestClient, event_loop):
    with patch('app.actions.rules.rule_actions.RuleActions.trigger_worker_reward_creation') as mock_reward_creation:
        mock_reward_creation.return_value = None
        try:
            program_rule = test_app.post("/v1/program_rule", json=util.new_program_rule).json()
            yield program_rule
        except Exception as e:
            raise Exception(f"program_rule creation failed, Exception: {e}")
        finally:
            if program_rule is not None:
                # deactivate rule and delete related staged rewards
                test_app.delete(f"/v1/program_rule/{program_rule['company_id']}/{program_rule['uuid']}")
                # delete rule
                delete_rule(program_rule['uuid'])


@pytest.fixture(scope="module")
def test_dates():
    # Define the named tuple type
    TestData = namedtuple('TestData', ['birthate', 'hired_on', 'anniversary', 'today'])

    # Dec 22 1988 at 12:00:00 PM
    birthate = datetime.fromtimestamp(598801919)
    # Feb 13 2024 at 12:00:00 PM
    hired_on = datetime.fromtimestamp(1707825600)
    # Jan 13 2024 at 12:00:00 PM
    anniversary = datetime.fromtimestamp(1705147200)
    today = datetime(2024, 2, 15, 0, 0, 0, 0)

    # Return the named tuple
    return TestData(birthate, hired_on, anniversary, today)

@pytest_asyncio.fixture(scope="function")
async def staged_rewards(program_rule):
    util.staged_rewards[0]['rule_uuid'], util.staged_rewards[1]['rule_uuid'] = program_rule['uuid'], program_rule['uuid']
    try:
        staged_rewards = [StagedRewardModelDB(**reward) for reward in util.staged_rewards]
        staged_rewards = await BaseCRUD.create(staged_rewards)
        yield staged_rewards
    finally:
        for reward in staged_rewards:
            await StagedRewardActions.handle_delete_staged_rewards(reward.company_id, reward.rule_uuid)

