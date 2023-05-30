from time import time
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.config import engine
from app.utilities import SHA224Hash
from app.routers.v1.v1CommonRouting import CommonRoutes
from app.models.programs import AdminModel, AdminUpdate, AdminCreate, AdminStatus

class ProgramAdminActions():

	@staticmethod
	async def get_program_admins(ids, args):
		statement = select(AdminModel).where(
			AdminModel.client_uuid == ids['client_uuid'],
			AdminModel.program_9char == ids['program_9char']
			).offset(args['offset']).limit(args['limit'])
		return await CommonRoutes.exec_get_all(statement)

	@staticmethod
	async def get_program_admin(ids):
		conditions = (
			AdminModel.user_uuid == ids['user_uuid'],
			AdminModel.client_uuid == ids['client_uuid'],
			AdminModel.program_9char == ids['program_9char']
		)

		statement = select(AdminModel).where(*conditions)
		return await CommonRoutes.exec_get_one(statement)

	@staticmethod
	async def create_program_admin(ids: dict, admins):
		current_time = int(time())
		admin = AdminModel(
			uuid = SHA224Hash(f"{admins.program_uuid}+{ids['user_uuid']}"),
			program_uuid=admins.program_uuid,
			client_uuid=ids['client_uuid'],
			program_9char=ids['program_9char'] if ids['program_9char'] else None,
			user_uuid=admins.user_uuid,
			permissions=admins.permissions if admins.permissions else 0,
			time_created=current_time,
			time_updated=current_time
		)
		admin = await CommonRoutes.exec_add_one(admin)
		new_admin = AdminStatus.from_orm(new_admin)
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
	async def update_program_admin(ids: dict, updates: AdminUpdate):
		statement = select(AdminModel).where(
			AdminModel.user_uuid == ids['user_uuid'],
			AdminModel.client_uuid == ids['client_uuid'],
			AdminModel.program_9char == ids['program_9char']
		)
		return await CommonRoutes.exec_update(statement, updates)

	@staticmethod
	async def delete_program_admin(ids: dict):
		statement = select(AdminModel).where(
			AdminModel.user_uuid == ids['user_uuid'],
			AdminModel.client_uuid == ids['client_uuid'],
			AdminModel.program_9char == ids['program_9char']
		)
		return await CommonRoutes.exec_delete(statement)

	@classmethod
	async def get_admin_by_user_id(cls, user_uuid):
		statement = select(AdminModel).where(AdminModel.user_uuid == user_uuid)
		return await CommonRoutes.exec_get_one(statement)

	@staticmethod
	async def check_existing(users: AdminCreate):
		if isinstance(users, list):
			for user in users:
				admin = await ProgramAdminActions.get_admin_by_user_id(user.user_uuid)
				if admin:
					user = AdminStatus.from_orm(admin, {"status":"exists"})
			return users
		admin = await ProgramAdminActions.get_admin_by_user_id(users.user_uuid)
		if admin:
			admin = AdminStatus.from_orm(admin)#, {"status":"exists"})
			admin.status = "exists"
			return admin
		return users
