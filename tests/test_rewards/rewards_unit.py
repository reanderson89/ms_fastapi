import pytest
import os
import tests.testutil as utils
from burp.utils.helper_actions import SHA224Hash
from burp.models.reward import ProgramRuleModelDB
from unittest.mock import patch, MagicMock, AsyncMock
from app.actions.rules.rule_actions import RuleActions
from app.models.reward.reward_models import ProgramRuleCreate

@pytest.mark.asyncio
async def test_create_program_rule_mock_users():
    requests_path = "app.actions.rewards.staged_reward_actions.requests.get"
    base_crud_path = "app.actions.rewards.staged_reward_actions.BaseCRUD"
    with patch(requests_path, new_callable=MagicMock) as MockRequest, \
         patch(base_crud_path, new_callable=AsyncMock) as MockCRUD:

        mock_rails_response = MagicMock()
        mock_rails_response.json.return_value = utils.users_from_rails
        MockRequest.return_value = mock_rails_response

        rule_uuid = SHA224Hash()
        mock_create_response = ProgramRuleModelDB(uuid=rule_uuid, **utils.new_program_rule)
        MockCRUD.create = AsyncMock(return_value=mock_create_response)
        mock_update_response = ProgramRuleModelDB(uuid=rule_uuid, users=utils.users_from_rails['users'], **utils.new_program_rule)
        MockCRUD.update = AsyncMock(return_value=mock_update_response)

        response = await RuleActions.create_rule(ProgramRuleCreate(**utils.new_program_rule))
        rails_api = os.environ.get("RAILS_API")
        MockRequest.assert_called_once_with(f"{rails_api}/accounts?company={utils.new_program_rule['company_id']}")
        assert len(response.users) == 2
        assert isinstance(response.users, list)
