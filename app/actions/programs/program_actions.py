from time import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.config import engine
from app.models.programs import ProgramModel, ProgramBase
from app.models.clients import ClientUserModel
from app.actions.helper_actions import HelperActions
from app.models.programs.program_event_models import ProgramEventModel
from app.models.segments.segment_models import SegmentModel
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.actions.base_actions import BaseActions


class ProgramActions():

	@classmethod
	async def create_program_handler(cls, programs, path_params):
		to_return = []
		if isinstance(programs, list):
			for i in programs:
				program = await cls.create_program(i, path_params["client_uuid"])
				to_return.append(program)
		else:
			program = await cls.create_program(programs, path_params["client_uuid"])
			to_return.append(program)
		return to_return

	@classmethod
	async def create_program(cls, program_data, client_uuid):
		admin_check = await cls.is_admin(program_data.user_uuid)
		if admin_check:
			check = await cls.check_for_existing(program_data.name)
			if check:
				return ProgramBase.from_orm(check)
			else:
				new_program = ProgramModel(
					name=program_data.name,
					cadence=program_data.cadence,
					cadence_value=program_data.cadence_value,
					program_type=program_data.program_type,
					status=program_data.status,
					description=program_data.description,
					user_uuid=program_data.user_uuid,
					budget_9char=program_data.budget_9char,
					client_uuid=client_uuid,
					program_9char = await HelperActions.generate_9char()
				)
				# new_program.program_9char = await HelperActions.generate_9char()
			program = await BaseActions.create(new_program)
			return ProgramBase.from_orm(program)
		else:
			return admin_check

	@classmethod
	async def check_for_existing(cls, name):
		program = await cls.get_program_by_name(name)
		if not program:
			return None
		else:
			return program

	@classmethod
	async def get_program_by_name(cls, name):
		with Session(engine) as session:
			return session.scalars(select(ProgramModel)
								.where(ProgramModel.name == name)).one_or_none()

	@classmethod
	async def is_admin(cls, user_uuid):
		admin = await cls.check_is_admin(user_uuid)
		await ExceptionHandling.check404(admin)
		if admin.admin == 1:
			return True
		else:
			return False

	@classmethod
	async def check_is_admin(cls, user_uuid):
		with Session(engine) as session:
			return session.scalars(select(ClientUserModel)
								.where(ClientUserModel.user_uuid == user_uuid)
								).one_or_none()

	@classmethod
	async def get_by_program_9char(cls, path_params):
		return await BaseActions.get_one_where(
			ProgramModel,
			[
				ProgramModel.program_9char == path_params["program_9char"],
				ProgramModel.client_uuid == path_params["client_uuid"]
			]
		)

	@classmethod
	async def get_by_client_uuid(cls, path_params, query_params):
		return await BaseActions.get_all_where(
			ProgramModel,
			[
				ProgramModel.client_uuid == path_params["client_uuid"]
			],
			query_params)

	@classmethod
	async def update_program(cls, program_updates, path_params):
		return await BaseActions.update(
			ProgramModel,
			[
				ProgramModel.program_9char == path_params["program_9char"],
				ProgramModel.client_uuid == path_params["client_uuid"]
			],
			program_updates
		)
	
	@classmethod
	async def check_for_program_event(cls, path_params):
		return await BaseActions.check_if_one_exists(
			ProgramEventModel,
			[
				ProgramEventModel.client_uuid == path_params["client_uuid"],
				ProgramEventModel.program_9char == path_params["program_9char"]
			]
		)
	
	@classmethod
	async def check_for_program_segment(cls, path_params):
		return await BaseActions.check_if_one_exists(
			SegmentModel,
			[
				SegmentModel.client_uuid == path_params["client_uuid"],
				SegmentModel.program_9char == path_params["program_9char"]
			]
		)

	@classmethod
	async def delete_program(cls, path_params):
		segment_check = await cls.check_for_program_segment(path_params)
		if segment_check:
			return {"message":"A segment exists for this program. It cannot be deleted at this time."}

		event_check = await cls.check_for_program_event(path_params)
		if event_check:
			return {"message":"An event exists for this program. It cannot be deleted at this time."}
		
		return await BaseActions.delete_one(
			ProgramModel,
			[
				ProgramModel.program_9char == path_params["program_9char"],
				ProgramModel.client_uuid == path_params["client_uuid"]
			]
		)
