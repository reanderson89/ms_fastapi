import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

import tests.testutil as util

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
        response = client.delete("/v1/delete_all_message_events")
        is_deleted(response)


@pytest.fixture(scope="function")
def reward(test_app: TestClient):
    with patch("app.actions.rewards.reward_actions.requests.get", new_callable=MagicMock) as MockRequest:
        mock_rails_response = MagicMock()
        mock_rails_response.json.return_value = util.users_from_rails
        MockRequest.return_value = mock_rails_response
        try:
            reward = test_app.post("/v1/rewards", json=util.new_reward).json()
            yield reward
        except Exception as e:
            raise Exception(f"reward creation failed, Exception: {e}")
        finally:
            if reward is not None:
                test_app.delete(f"/v1/rewards/{reward['company_id']}/{reward['uuid']}")
