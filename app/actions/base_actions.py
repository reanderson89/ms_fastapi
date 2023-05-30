from time import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.config import engine
from app.actions.helper_actions import HelperActions
from app.exceptions import ExceptionHandling

class BaseActions():

	@staticmethod
	async def get_all(model):
		with Session(engine) as session:
			db_items = session.scalars(select(model)).all()
			# TODO: refactor to use general exception handling
			await ExceptionHandling.check404(db_items)
			return db_items

	@staticmethod
	async def get_all_where(model, conditions: tuple):
		with Session(engine) as session:
			db_item = session.scalars(
				select(model)
				.where(*conditions)
				).all()
		await ExceptionHandling.check404(db_item)
		return db_item

	@staticmethod
	async def get_one_where(model, conditions: tuple):
		with Session(engine) as session:
			db_item = session.scalars(
				select(model)
				.where(*conditions)
				).one_or_none()
		await ExceptionHandling.check404(db_item)
		return db_item

	@staticmethod
	async def check_if_exists(model, conditions: tuple):
		with Session(engine) as session:
			return session.scalars(
				select(model)
				.where(*conditions)
				).one_or_none()

	@staticmethod
	async def create(model_obj):
		model_obj.uuid = await HelperActions.generate_SHA224() if model_obj.uuid is None else model_obj.uuid
		current_time = int(time())
		model_obj.time_created = current_time
		model_obj.time_updated = current_time

		with Session(engine) as session:
			session.add(model_obj)
			session.commit()
			session.refresh(model_obj)
		return model_obj

	@staticmethod
	async def update(model, conditions: tuple, updates):
		with Session(engine) as session:
			db_item = session.scalars(
				select(model)
				.where(*conditions)
				).one_or_none()
			# TODO: refactor to use general exception handling
			await ExceptionHandling.check404(db_item)
			updated_fields = updates.dict(exclude_unset=True)
			for key, value in updated_fields.items():
				setattr(db_item, key, value)
			db_item.time_updated = int(time())
			session.add(db_item)
			session.commit()
			session.refresh(db_item)
			return db_item

	@staticmethod
	async def delete(model, conditions: tuple):
		with Session(engine) as session:
			db_item = session.scalars(
				select(model)
				.where(*conditions)
				).one_or_none()
			# TODO: refactor to use general exception handling
			await ExceptionHandling.check404(db_item)
			session.delete(db_item)
			session.commit()
			return {'ok': True, 'Deleted:': db_item}

	@staticmethod
	async def delete_all(model, conditions: tuple):
		with Session(engine) as session:
			db_items = session.scalars(
				select(model)
				.where(*conditions)
				).all()
			# TODO: refactor to use general exception handling
			await ExceptionHandling.check404(*db_items)
			for item in db_items:
				session.delete(item)
			session.commit()
			return {'ok': True, 'Deleted:': db_items}
