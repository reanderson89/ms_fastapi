from re import M
# from unittest import mock
import pytest
import tests.testutil as utils
from burp.utils.helper_actions import SHA224Hash
from burp.models.reward import ProgramRuleModelDB
from unittest.mock import patch, MagicMock, AsyncMock
from app.actions.rules.rule_actions import RuleActions
from app.actions.rewards.staged_reward_actions import StagedRewardActions
from app.models.reward.reward_models import ProgramRuleCreate, RuleState
from app.worker.temp_worker import TempWorker


@pytest.fixture
def mock_trigger():
    with patch.object(RuleActions, "trigger_worker_reward_creation", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_delete():
    with patch.object(StagedRewardActions, "handle_delete_staged_rewards", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_check():
    with patch.object(RuleActions, "handle_check_keys", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_setup():
    with patch.object(RuleActions, "setup_staged_rewards_for_update", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_crud():
    with patch("app.actions.rules.rule_actions.BaseCRUD", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_get_staged_reward():
    with patch.object(StagedRewardActions, "get_staged_rewards_by_rule", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_update_staged_reward():
    with patch.object(StagedRewardActions, "update_staged_reward", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_worker():
    with patch("app.actions.rules.rule_actions.TempWorker", new_callable=MagicMock) as mock_class:
        mock_instance = mock_class.return_value
        mock_instance.get_users_for_reward_creation = MagicMock()
        yield mock_instance


@pytest.fixture
def mock_get_program_rule_by_uuid():
    with patch.object(RuleActions, "get_program_rule", new_callable=AsyncMock) as mock:
        yield mock


@pytest.mark.asyncio
async def test_create_program_rule_mock_users(mock_trigger, mock_crud):
    mock_trigger.return_value = True

    rule_uuid = SHA224Hash()
    mock_create_response = ProgramRuleModelDB(uuid=rule_uuid, **utils.new_program_rule)
    mock_crud.create.return_value = mock_create_response
    mock_update_response = ProgramRuleModelDB(uuid=rule_uuid, **utils.new_program_rule)
    mock_crud.update.return_value = mock_update_response

    program_rule = ProgramRuleCreate(**utils.new_program_rule)

    response = await RuleActions.create_rule(program_rule)
    mock_trigger.assert_called_once_with(mock_create_response)
    assert response == mock_create_response
    assert mock_crud.create.called


@pytest.mark.asyncio
async def test_handle_rule_state_change_to_active(mock_trigger, mock_delete, mock_check, mock_setup):
    current_rule = ProgramRuleModelDB(state=RuleState.DRAFT.value)
    updated_rule = ProgramRuleModelDB(state=RuleState.ACTIVE.value)

    await RuleActions.handle_rule_state_change(current_rule, updated_rule)

    mock_trigger.assert_called_once_with(updated_rule)
    mock_delete.assert_not_called()
    mock_check.assert_not_called()
    mock_setup.assert_not_called()


@pytest.mark.asyncio
async def test_handle_rule_state_change_to_draft(mock_trigger, mock_delete, mock_check, mock_setup):
    current_rule = ProgramRuleModelDB(state=RuleState.ACTIVE.value)
    updated_rule = ProgramRuleModelDB(state=RuleState.DRAFT.value)

    await RuleActions.handle_rule_state_change(current_rule, updated_rule)

    mock_trigger.assert_not_called()
    mock_delete.assert_called_once_with(updated_rule.company_id, updated_rule.uuid)
    mock_check.assert_not_called()
    mock_setup.assert_not_called()


@pytest.mark.asyncio
async def test_handle_rule_state_change_to_active_with_keys_changed(mock_trigger, mock_delete, mock_check, mock_setup):
    current_rule = ProgramRuleModelDB(state=RuleState.ACTIVE.value)
    updated_rule = ProgramRuleModelDB(state=RuleState.ACTIVE.value)

    mock_check.return_value = True

    await RuleActions.handle_rule_state_change(current_rule, updated_rule)

    mock_trigger.assert_called_once_with(updated_rule)
    mock_delete.assert_called_once_with(updated_rule.company_id, updated_rule.uuid)
    mock_check.assert_called_once_with(current_rule, updated_rule)
    mock_setup.assert_not_called()


@pytest.mark.asyncio
async def test_handle_rule_state_change_to_active_with_keys_not_changed(mock_trigger, mock_delete, mock_check, mock_setup):
    current_rule = ProgramRuleModelDB(state=RuleState.ACTIVE.value)
    updated_rule = ProgramRuleModelDB(state=RuleState.ACTIVE.value)

    mock_check.return_value = False

    await RuleActions.handle_rule_state_change(current_rule, updated_rule)

    mock_trigger.assert_not_called()
    mock_delete.assert_not_called()
    mock_check.assert_called_once_with(current_rule, updated_rule)
    mock_setup.assert_called_once_with(updated_rule)


@pytest.mark.asyncio
async def test_trigger_worker_reward_creation(mock_worker):
    mock_worker.get_users_for_reward_creation.return_value = True
    rule = ProgramRuleModelDB()
    await RuleActions.trigger_worker_reward_creation(rule)
    mock_worker.get_users_for_reward_creation.assert_called_once_with(rule)


@pytest.mark.asyncio
async def test_to_program_rule_db_model():
    rule_create = ProgramRuleCreate(**utils.new_program_rule)
    response = await RuleActions.to_program_rule_db_model(rule_create)
    assert response == ProgramRuleModelDB(**utils.new_program_rule)


@pytest.mark.asyncio
async def test_setup_staged_rewards_for_update(mock_get_staged_reward, mock_update_staged_reward):
    rule = ProgramRuleModelDB()
    staged_rewards = [ProgramRuleModelDB() for _ in range(3)]
    mock_get_staged_reward.return_value = staged_rewards
    await RuleActions.setup_staged_rewards_for_update(rule)
    assert mock_get_staged_reward.called
    assert mock_update_staged_reward.call_count == 3


@pytest.mark.asyncio
async def test_handle_check_keys_false():
    current_rule = ProgramRuleModelDB(rule_type="test")
    updated_rule = ProgramRuleModelDB(rule_type="test")
    response = await RuleActions.handle_check_keys(current_rule, updated_rule)
    assert response == False


@pytest.mark.asyncio
async def test_handle_check_keys_true():
    current_rule = ProgramRuleModelDB(rule_type="test")
    updated_rule = ProgramRuleModelDB(rule_type="test1")
    response = await RuleActions.handle_check_keys(current_rule, updated_rule)
    assert response == True


@pytest.mark.asyncio
async def test_handle_check_keys_none():
    current_rule = ProgramRuleModelDB()
    updated_rule = ProgramRuleModelDB()
    response = await RuleActions.handle_check_keys(current_rule, updated_rule)
    assert response == False


@pytest.mark.asyncio
async def test_update_rule(mock_crud, mock_get_program_rule_by_uuid):
    rule_uuid = SHA224Hash()
    mock_get_program_rule_by_uuid.return_value = ProgramRuleModelDB()
    mock_update_response = ProgramRuleModelDB(uuid=rule_uuid, **utils.new_program_rule)
    mock_crud.update.return_value = mock_update_response

    company_id = 1
    rule_uuid = SHA224Hash()
    rule_update = ProgramRuleCreate(**utils.new_program_rule)

    response = await RuleActions.update_program_rule(company_id, rule_uuid, rule_update)
    assert response == mock_update_response
    assert mock_crud.update.called


@pytest.mark.asyncio
async def test_deactivate_program_rule(mock_crud):
    rule_uuid = SHA224Hash()
    mock_delete_response = ProgramRuleModelDB(uuid=rule_uuid, **utils.new_program_rule)
    mock_crud.delete.return_value = mock_delete_response

    company_id = 1
    rule_uuid = SHA224Hash()

    await RuleActions.deactivate_program_rule(company_id, rule_uuid, state=RuleState.INACTIVE.value)
    assert mock_crud.update.called


@pytest.mark.asyncio
async def test_get_distinct_company_ids(mock_crud):
    mock_crud.get_all_where.return_value = [1, 2, 3]
    response = await RuleActions.get_distinct_company_ids()
    assert response == [1, 2, 3]
    assert mock_crud.get_all_where.called


@pytest.mark.asyncio
async def test_get_program_rule(mock_crud):
    mock_crud.get_one_where.return_value = ProgramRuleModelDB()
    company_id = 1
    rule_uuid = SHA224Hash()
    response = await RuleActions.get_program_rule(company_id, rule_uuid)
    assert response == ProgramRuleModelDB()
    assert mock_crud.get_one_where.called


@pytest.mark.asyncio
async def test_get_program_rules_by_company(mock_crud):
    mock_crud.get_all_where.return_value = [ProgramRuleModelDB() for _ in range(3)]
    company_id = 1
    response = await RuleActions.get_program_rules_by_company(company_id)
    assert response == [ProgramRuleModelDB() for _ in range(3)]
    assert mock_crud.get_all_where.called
