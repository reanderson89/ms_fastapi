from src.database.config import engine
from sqlmodel import Session, select
from typing import List
from time import time

class CommonRoutes():
	
	def get_all(model):
		with Session(engine) as session:
			items = session.exec(select(model)).all()
			return items
	
	def get_one(model, search_by):
		with Session(engine) as session:
			statement = select(model).where(model.uuid == search_by)
			item = session.exec(statement).one_or_none()
			return item
		
	def create_one_or_many(items):
		with Session(engine) as session:
			if isinstance(items, List):
				for item in items:
					session.add(item)
			else:
				session.add(items)
			session.commit()
			session.refresh(items)
			return items
	
	def update_one(search_by, original_model, compare_model):
		with Session(engine) as session:
			statement = select(original_model).where(original_model.uuid == search_by)
			item = session.exec(statement).one()
			updated_fields = compare_model.dict(exclude_unset=True)
			for key, value in updated_fields.items():
				setattr(item, key, value)
			if(original_model.time_updated):
				item.time_updated = int(time( ))
			session.add(item)
			session.commit()
			session.refresh(item)
			return item

	def delete_one(search_by, model):
		with Session(engine) as session:
			statement = select(model).where(model.uuid == search_by)
			item = session.exec(statement).one()
			session.delete(item)
			session.commit()
			return {'Deleted:': item}
