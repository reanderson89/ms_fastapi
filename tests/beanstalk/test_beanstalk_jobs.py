import pytest
import tests.testutil as utils
from unittest.mock import patch, MagicMock, AsyncMock
# from app.actions.clients.user import ClientUserActions

# @pytest.mark.asyncio
# async def test_create_client_user_job(test_app):
#     try:
#         func_path = "app.actions.clients.user.client_user_actions.TempWorker"
#         with patch(func_path, new_callable=MagicMock) as MockTempWorker:
#             mocked_instance = MockTempWorker.return_value
#             mocked_instance.get_user_job = AsyncMock(return_value = None)
#             mocked_instance.alt_get_user_job = AsyncMock(return_value = None)
#             mocked_instance.create_user_job = AsyncMock(return_value = utils.response_create_user_job)
#             client_user = await ClientUserActions.handle_client_user_job(utils.create_client_user_job)
#             assert client_user.user_uuid == utils.create_client_user_job["body"]["user_uuid"]   
#             assert client_user.client_uuid == utils.create_client_user_job["body"]["client_uuid"]
#     finally:
#         test_app.delete(f"/v1/clients/{client_user.client_uuid}/users/{client_user.uuid}")
        
# @pytest.mark.asyncio
# async def test_migrate_user_job(test_app, client_user, program):
#     try:
#         func_path = "app.actions.clients.user.client_user_actions.TempWorker"
#         with patch(func_path, new_callable=MagicMock) as MockTempWorker:
#             mocked_instance = MockTempWorker.return_value
#             mocked_instance.get_user_job = AsyncMock(return_value = None)
#             mocked_instance.alt_get_user_job = AsyncMock(return_value = None)
#             mocked_instance.create_user_job = AsyncMock(return_value = utils.response_create_user_job)
#             new_client_user = await ClientUserActions.handle_client_user_job(utils.create_client_user_job)
#             migrated_user = await ClientUserActions.migrate_user(new_client_user.user_uuid, client_user['user_uuid'])
#             updated_program = test_app.get(f"/v1/clients/{client_user['client_uuid']}/programs/{program['program_9char']}")
#             query_params = {"order_by": "time_created", "sort": "DESC"}
#             updated_client_users = await ClientUserActions.get_all_client_users_by_user_uuid(new_client_user.user_uuid, query_params)
#             sorted_client_users = sorted(updated_client_users, key=lambda user: user.time_created, reverse=True)
#             assert migrated_user
#             assert updated_program.json()["user_uuid"] == new_client_user.user_uuid
#             # testing that the client_users are coming out in descending order by sorting one in reverse in matching them against each other.
#             assert updated_client_users[0].time_created == sorted_client_users[0].time_created
#             for client_user in updated_client_users:
#                 assert client_user.user_uuid == new_client_user.user_uuid
#     finally:
#         await ClientUserActions.delete_client_user({"client_uuid":new_client_user.client_uuid, "client_user_uuid":new_client_user.uuid})
        
