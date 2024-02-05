import os
from unittest.mock import MagicMock, patch, AsyncMock

import pytest
from fastapi.testclient import TestClient

import tests.testutil as util

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


@pytest.fixture(scope="module")
def test_app():
    try:
        client = TestClient(app)
        yield client
    finally:
        pass
        # response = client.delete("/v1/delete_all_message_events")
        # is_deleted(response)


@pytest.fixture
def mock_worker():
    worker = TempWorker()
    worker.get_users_for_reward_creation = AsyncMock()


@pytest.fixture(scope="function")
def program_rule(test_app: TestClient):



    with patch("app.actions.rewards.reward_actions.requests.get", new_callable=MagicMock) as MockRequest:
        mock_rails_response = MagicMock()
        mock_rails_response.json.return_value = util.users_from_rails  # TODO: still needs to be fixed
        MockRequest.return_value = mock_rails_response
        try:
            program_rule = test_app.post("/v1/program_rule", json=util.new_program_rule).json()
            yield program_rule
        except Exception as e:
            raise Exception(f"program_rule creation failed, Exception: {e}")
        finally:
            if program_rule is not None:
                test_app.delete(f"/v1/program_rule/{program_rule['company_id']}/{program_rule['uuid']}")
