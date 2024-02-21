from typing import List
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
