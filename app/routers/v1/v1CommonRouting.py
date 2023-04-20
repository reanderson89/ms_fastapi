from app.database.config import engine
from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List
from time import time

class CommonRoutes():
	
	def get_all(model):
		with Session(engine) as session:
			items = session.exec(select(model)).all()
			ExceptionHandling.check404(items)
			return items
		
	def get_one(model, search_by):
		with Session(engine) as session:
			item = session.get(model, search_by)
			ExceptionHandling.check404(item)
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
	
	def update_one(search_by, original_model, update_model):
		with Session(engine) as session:
			db_item = session.get(original_model, search_by)
			ExceptionHandling.check404(db_item)
			updated_fields = update_model.dict(exclude_unset=True)
			for key, value in updated_fields.items():
				setattr(db_item, key, value)
			if(update_model.time_updated):
				db_item.time_updated = int(time())
			session.add(db_item)
			session.commit()
			session.refresh(db_item)
			print(db_item)
			return db_item

	def delete_one(search_by, model):
		with Session(engine) as session:
			item = session.get(model, search_by)
			ExceptionHandling.check404(item)
			session.delete(item)
			session.commit()
			return {'ok': True, 'Deleted:': item}


class ExceptionHandling():

	def check404(item):
		if not item:
			raise HTTPException(status_code=404, detail="Not Found")
