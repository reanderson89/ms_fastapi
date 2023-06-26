from time import time
from app.actions.base_actions import BaseActions
from app.utilities import SHA224Hash
from app.models.programs import AdminModelDB, AdminUpdate, AdminCreate, AdminStatus

class ProgramAdminActions():

	@staticmethod
	async def get_program_admins(path_params, query_params):
		return await BaseActions.get_all_where(
			AdminModelDB,
			[
				AdminModelDB.client_uuid == path_params['client_uuid'],
				AdminModelDB.program_9char == path_params['program_9char']
			],
			query_params
		)

	@staticmethod
	async def get_program_admin(path_params):
		return await BaseActions.get_one_where(
			AdminModelDB,
			[
				AdminModelDB.user_uuid == path_params['user_uuid'],
				AdminModelDB.client_uuid == path_params['client_uuid'],
				AdminModelDB.program_9char == path_params['program_9char']
			]
		)

	@staticmethod
	async def create_program_admin(ids: dict, admins):
		current_time = int(time())
		admin = AdminModelDB(
			uuid = SHA224Hash(f"{admins.program_uuid}+{ids['user_uuid']}"),
			program_uuid=admins.program_uuid,
			client_uuid=ids["client_uuid"],
			program_9char=ids["program_9char"] if ids["program_9char"] else None,
			user_uuid=admins.user_uuid,
			permissions=admins.permissions if admins.permissions else 0,
			time_created=current_time,
			time_updated=current_time
		)
		admin = await BaseActions.create(admin)
		new_admin = AdminStatus.from_orm(admin)
		new_admin.status = "admin created"
		return new_admin

	@classmethod
	async def create_program_admins(cls, ids: dict, admins: list):
		for admin in admins:
			if isinstance(admin, AdminCreate):
				new_admin = await cls.create_program_admin(ids, admin)
				admin = AdminStatus.from_orm(new_admin)
				admin.status = "admin created"

	@staticmethod
	async def update_program_admin(path_params: dict, updates: AdminUpdate):
		return await BaseActions.update(
			AdminModelDB,
			[
				AdminModelDB.user_uuid == path_params['user_uuid'],
				AdminModelDB.client_uuid == path_params['client_uuid'],
				AdminModelDB.program_9char == path_params['program_9char']
			],
			updates
		)

	@staticmethod
	async def delete_program_admin(path_params: dict):
		return await BaseActions.delete_one(
			AdminModelDB,
			[
				AdminModelDB.user_uuid == path_params['user_uuid'],
				AdminModelDB.client_uuid == path_params['client_uuid'],
				AdminModelDB.program_9char == path_params['program_9char']
			]
		)

	@classmethod
	async def get_admin_by_user_id(cls, user_uuid):
		return await BaseActions.check_if_exists(AdminModelDB, [AdminModelDB.user_uuid == user_uuid])

	@staticmethod
	async def check_existing(users: AdminCreate):
		if isinstance(users, list):
			for user in users:
				admin = await ProgramAdminActions.get_admin_by_user_id(user.user_uuid)
				if admin:
					user = AdminStatus.from_orm(admin)
					user.status = "exists"
			return users
		admin = await ProgramAdminActions.get_admin_by_user_id(users.user_uuid)
		if admin:
			admin = AdminStatus.from_orm(admin)
			admin.status = "exists"
			return admin
		return users
