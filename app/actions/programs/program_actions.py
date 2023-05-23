from time import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.actions.commonActions import CommonActions
from app.database.config import engine
from app.models.programs import ProgramModel
from app.models.clients import ClientUserModel
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
				return check
			else:
				new_program = ProgramModel(
					name=program_data.name,
					cadence=program_data.cadence,
					description=program_data.description,
					user_uuid=program_data.user_uuid,
					client_uuid=client_uuid
				)
				new_program.program_9char = await CommonActions.generate_9char()
			return await CommonRoutes.create_one_or_many(new_program)
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
	def get_program_by_name(cls, name):
		with Session(engine) as session:
			return session.exec(select(ProgramModel)
								.where(ProgramModel.name == name)).one_or_none()

	@classmethod
	async def is_admin(cls, user_uuid):
		admin = await cls.check_is_admin(user_uuid)
		if admin.admin == 1:
			return True
		else:
			return False

	@classmethod
	async def check_is_admin(cls, user_uuid):
		with Session(engine) as session:
			return session.scalars(select(ClientUserModel)
								.where(ClientUserModel.uuid == user_uuid))
		#TODO: current bug - if no user is found, this returns the execution call and no empty list

	@classmethod
	async def get_by_program_9char(cls, client_uuid, program_9char):
		with Session(engine) as session:
			return session.scalars(
				select(ProgramModel)
				.where(
					ProgramModel.program_9char == program_9char,
					ProgramModel.client_uuid == client_uuid
				)
			).one_or_none()

	@classmethod
	async def get_by_client_uuid(cls, client_uuid, offset, limit):
		with Session(engine) as session:
			return session.scalars(
				select(ProgramModel).where(
					ProgramModel.client_uuid == client_uuid
				)
				.offset(offset)
				.limit(limit)
			).all()

	@classmethod
	def update_program(cls, client_uuid, program_9char, program_updates):
		with Session(engine) as session:
			program = session.scalars(
				select(ProgramModel)
				.where(
					ProgramModel.program_9char == program_9char,
					ProgramModel.client_uuid == client_uuid
				)
			).one_or_none()
			update_program = program_updates.dict(exclude_unset=True)
			for k, v in update_program.items():
				setattr(program, k, v)
			program.time_updated = int(time())
			session.add(program)
			session.commit()
			session.refresh(program)
			return program
