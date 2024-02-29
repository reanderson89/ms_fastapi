import json
from collections import defaultdict
import tests.testutil as utils


def run_asserts(response, util_obj):
    # assert "uuid" in response
    # assert response['company_id'] == util_obj['company_id']
    # assert response['client_admin_id'] == util_obj['client_admin_id']
    # assert isinstance(response['rule'], dict)
    # assert isinstance(response['users'], list) and all(isinstance(user, dict) for user in response['users'])
    assert isinstance(response, dict)


def test_create_program_rule(program_rule):
    run_asserts(program_rule, utils.new_program_rule)


def test_fail_create_program_rule_missing_fields(test_app):
    response = test_app.post("/v1/program_rule", json={"company_id": 5, "client_admin_id": 10})
    assert response.status_code == 422


def test_get_program_rules_by_company(test_app, program_rule):
    program_rules = test_app.get(f"/v1/program_rule/{program_rule['company_id']}")
    assert program_rules.status_code == 200
    program_rules = program_rules.json()
    for rule in program_rules:
        run_asserts(rule, utils.new_program_rule)


def test_get_program_rule(test_app, program_rule):
    rule_response = test_app.get(f"/v1/program_rule/{program_rule['company_id']}/{program_rule['uuid']}")
    rule_response.status_code == 200
    rule_response = rule_response.json()
    assert rule_response['uuid'] == program_rule['uuid']
    run_asserts(rule_response, utils.new_program_rule)


def test_update_program_rule(test_app, program_rule):
    rule_update = test_app.put(f"/v1/program_rule/{program_rule['company_id']}/{program_rule['uuid']}", json=utils.update_program_rule)
    rule_update.status_code == 200
    rule_update = rule_update.json()
    run_asserts(rule_update, utils.update_program_rule)


def test_fail_update_program_rule_missing_fields(test_app, program_rule):
    response = test_app.put(f"/v1/program_rule/{program_rule['company_id']}/{program_rule['uuid']}", json={"client_admin_id": 10})
    assert response.status_code == 422


def test_deactivate_program_rule(test_app, program_rule):
    rule_response = test_app.delete(f"/v1/program_rule/{program_rule['company_id']}/{program_rule['uuid']}")
    rule_response.status_code == 200
    rule_response = rule_response.json()
    assert rule_response["state"] == "INACTIVE"
    run_asserts(rule_response, utils.new_program_rule)


def test_get_staged_rewards_no_filters(test_app, staged_rewards):
    response = test_app.get(f"/v1/staged_rewards/{staged_rewards[0].company_id}")
    assert response.status_code == 200
    response = response.json()
    for reward in response['items']:
        assert staged_rewards[0].company_id == reward['company_id']


def test_get_staged_rewards_given_multiple_rule_uuids(test_app, staged_rewards):
    rule_uuids = json.dumps([reward.rule_uuid for reward in staged_rewards])
    response = test_app.get(f"/v1/staged_rewards/{staged_rewards[0].company_id}?rule_uuid={rule_uuids}")
    assert response.status_code == 200
    response = response.json()
    all_rewards_for_rules_found = False
    for reward in response['items']:
        if reward['rule_uuid'] in rule_uuids:
            all_rewards_for_rules_found = True
    assert all_rewards_for_rules_found


def test_get_staged_rewards_with_partial_name(test_app, staged_rewards):
    partial_name = staged_rewards[0].full_name[0:2]
    response = test_app.get(f"/v1/staged_rewards/{staged_rewards[0].company_id}?full_name={partial_name}")
    assert response.status_code == 200
    response = response.json()
    matching_name = False
    for reward in response['items']:
        if staged_rewards[0].full_name == reward['full_name']:
            matching_name = True
            break
    assert matching_name


def test_get_staged_rewards_by_date_range(test_app, staged_rewards):
    from_date = "2025-04-12"
    to_date = "2025-04-14"
    response = test_app.get(f"/v1/staged_rewards/{staged_rewards[0].company_id}?from_date={from_date}&to_date={to_date}")
    assert response.status_code == 200
    response = response.json()
    first_reward = False
    second_reward = False
    for searched_reward in response["items"]:
        if searched_reward["uuid"] == staged_rewards[0].uuid:
            first_reward = True
        if searched_reward["uuid"] == staged_rewards[1].uuid:
            second_reward = True
    assert first_reward
    assert second_reward


def test_get_reward_count_for_comapny_rules(test_app, program_rule, staged_rewards):
    test_rule_count = defaultdict(int)
    for reward in staged_rewards:
        if program_rule['uuid'] == reward.rule_uuid:
            test_rule_count[reward.rule_uuid] += 1
    response = test_app.get(f"/v1/staged_rewards/{staged_rewards[0].company_id}/count")
    assert response.status_code == 200
    response = response.json()
    rules = response['rules']
    assert rules[program_rule['uuid']] == test_rule_count[program_rule['uuid']]