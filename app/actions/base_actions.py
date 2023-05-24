from time import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.config import engine
from app.utilities import SHA224Hash
from app.routers.v1.v1CommonRouting import ExceptionHandling

class BaseActions():

	@staticmethod
	async def get_all(model):
		with Session(engine) as session:
			items = session.scalars(select(model)).all()
			# TODO: refactor to use general exception handling
			await ExceptionHandling.check404(items)
			return items

	@staticmethod
	async def get_all_where(model, conditions: tuple):
		with Session(engine) as session:
			return session.scalars(
				select(model)
				.where(*conditions)
				).all()

	@staticmethod
	async def get_one_where(model, conditions: tuple):
		with Session(engine) as session:
			return session.scalars(
				select(model)
				.where(*conditions)
				).one_or_none()

	# Deprecated
	# move to get_one_where or seperate queries if different tables
	# are being queried, to avoid joins
	@staticmethod
	async def get_one_where2(model, conditions1: tuple, conditions2: tuple):
		with Session(engine) as session:
			return session.scalars(
				select(model)
				.where(*conditions1)
				.where(*conditions2)
				).one_or_none()

	@staticmethod
	async def create(model_obj):
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
			if(db_item.time_updated):
				db_item.time_updated = int(time())
			session.add(db_item)
			session.commit()
			session.refresh(db_item)
			return db_item

	@staticmethod
	async def delete(model, conditions: tuple):
		with Session(engine) as session:
			item = session.scalars(
				select(model)
				.where(*conditions)
				).one_or_none()
			# TODO: refactor to use general exception handling
			await ExceptionHandling.check404(item)
			session.delete(item)
			session.commit()
			return {'ok': True, 'Deleted:': item}

	@staticmethod
	async def delete_all(model, conditions: tuple):
		with Session(engine) as session:
			items = session.scalars(
				select(model)
				.where(conditions)
				).all()
			# TODO: refactor to use general exception handling
			ExceptionHandling.check404(items)
			for item in items:
				session.delete(item)
			session.commit()
			return {'ok': True, 'Deleted:': items}
