from app.database.config import engine
from app.utilities import SHA224Hash
from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List
from time import time

class CommonRoutes():
	
	async def get_all(model):
		with Session(engine) as session:
			items = session.exec(select(model)).all()
			await ExceptionHandling.check404(items)
			return items
		
	async def get_one(model, search_by):
		with Session(engine) as session:
			item = session.get(model, search_by)
			await ExceptionHandling.check404(item)
			return item
		
	async def create_one_or_many(items):
		with Session(engine) as session:
			if isinstance(items, List):
				for item in items:
					item.uuid = SHA224Hash() if item.uuid is None else None
					item.time_created = item.time_updated = int(time())
					session.add(item)
			else:
				items.uuid = SHA224Hash() if items.uuid is None else items.uuid
				items.time_created = items.time_updated = int(time())
				session.add(items)

			session.commit()

			if isinstance(items, List):
				for item in items:
					session.refresh(item)
			else:
				session.refresh(items)
			return items
	
	async def update_one(search_by, original_model, update_model):
		with Session(engine) as session:
			db_item = session.get(original_model, search_by)
			await ExceptionHandling.check404(db_item)
			updated_fields = update_model.dict(exclude_unset=True)
			for key, value in updated_fields.items():
				setattr(db_item, key, value)
			if(db_item.time_updated):
				db_item.time_updated = int(time())
			session.add(db_item)
			session.commit()
			session.refresh(db_item)
			return db_item

	async def delete_one(search_by, model):
		with Session(engine) as session:
			item = session.get(model, search_by)
			await ExceptionHandling.check404(item)
			session.delete(item)
			session.commit()
			return {'ok': True, 'Deleted:': item}


class ExceptionHandling():

	async def check404(item):
		if not item:
			raise HTTPException(status_code=404, detail="Not Found")
	
	async def custom500(message):
		raise HTTPException(status_code=500, detail=message)
