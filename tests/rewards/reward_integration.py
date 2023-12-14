from typing import List
import tests.testutil as utils


def run_asserts(response, util_obj):
    # assert "uuid" in response
    # assert response['company_id'] == util_obj['company_id']
    # assert response['client_admin_id'] == util_obj['client_admin_id']
    # assert isinstance(response['rule'], dict)
    # assert isinstance(response['users'], list) and all(isinstance(user, dict) for user in response['users'])
    assert isinstance(response['reward_info'], dict)


def test_create_reward(reward):
    run_asserts(reward, utils.new_reward)


def test_fail_create_reward_missing_fields(test_app):
    response = test_app.post("/v1/rewards", json={"company_id":5, "client_admin_id": 10})
    assert response.status_code == 422


def test_get_rewards_by_company(test_app, reward):
    rewards = test_app.get(f"/v1/rewards/{reward['company_id']}")
    assert rewards.status_code == 200
    rewards = rewards.json()
    for reward in rewards['items']:
        run_asserts(reward, utils.new_reward)


def test_get_reward(test_app, reward):
    reward_response = test_app.get(f"/v1/rewards/{reward['company_id']}/{reward['uuid']}")
    reward_response.status_code == 200
    reward_response = reward_response.json()
    assert reward_response['uuid'] == reward['uuid']
    run_asserts(reward_response, utils.new_reward)


def test_update_reward(test_app, reward):
    reward_update = test_app.put(f"/v1/rewards/{reward['company_id']}/{reward['uuid']}", json=utils.update_reward)
    reward_update.status_code == 200
    reward_update = reward_update.json()
    run_asserts(reward_update, utils.update_reward)


def test_fail_update_reward_missing_fields(test_app, reward):
    response = test_app.put(f"/v1/rewards/{reward['company_id']}/{reward['uuid']}", json={"client_admin_id": 10})
    assert response.status_code == 422


def test_delete_reward(test_app, reward):
    reward_response = test_app.delete(f"/v1/rewards/{reward['company_id']}/{reward['uuid']}")
    reward_response.status_code == 200
    reward_response = reward_response.json()
    assert reward_response["ok"] == True
    run_asserts(reward_response["Deleted"], utils.new_reward)

