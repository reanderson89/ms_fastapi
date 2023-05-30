from time import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.config import engine
from app.models.programs import ProgramModel, ProgramBase
from app.models.clients import ClientUserModel
from app.actions.helper_actions import HelperActions
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling


class ProgramActions():

	@classmethod
	async def create_program_handler(cls, programs, client_uuid):
		to_return = []
		if isinstance(programs, list):
			for i in programs:
				program = await cls.create_program(i, client_uuid)
				to_return.append(program)
		else:
			program = await cls.create_program(programs, client_uuid)
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
					client_uuid=client_uuid
				)
				new_program.program_9char = await HelperActions.generate_9char()
			program =  await CommonRoutes.create_one_or_many(new_program)
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
	async def get_by_program_9char(cls, client_uuid, program_9char):
		with Session(engine) as session:
			program = session.scalars(
				select(ProgramModel)
				.where(
					ProgramModel.program_9char == program_9char,
					ProgramModel.client_uuid == client_uuid
				)
			).one_or_none()
			await ExceptionHandling.check404(program)
			return program

	@classmethod
	async def get_by_client_uuid(cls, client_uuid, offset, limit):
		with Session(engine) as session:
			programs = session.scalars(
				select(ProgramModel).where(
					ProgramModel.client_uuid == client_uuid
				)
				.offset(offset)
				.limit(limit)
			).all()
			await ExceptionHandling.check404(programs)
			return programs

	@classmethod
	async def update_program(cls, client_uuid, program_9char, program_updates):
		with Session(engine) as session:
			program = session.scalars(
				select(ProgramModel)
				.where(
					ProgramModel.program_9char == program_9char,
					ProgramModel.client_uuid == client_uuid
				)
			).one_or_none()
			await ExceptionHandling.check404(program)
			update_program = program_updates.dict(exclude_unset=True)
			for k, v in update_program.items():
				setattr(program, k, v)
			program.time_updated = int(time())
			session.add(program)
			session.commit()
			session.refresh(program)
			return program
