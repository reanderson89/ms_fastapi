import csv
import codecs
import json
import time

from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from app.database.config import engine
from app.exceptions import ExceptionHandling
from app.utilities import SHA224Hash, PositiveNumbers

class HelperActions():

	@staticmethod
	async def get_session():
		with Session(engine) as session:
			yield session

	@staticmethod
	async def make_username(first, last):
		first = first.lower()
		last = last.lower()
		return f"{first}{last}"

	@staticmethod
	async def process_csv(csv_file: UploadFile = File(...)):
			csv_reader = csv.DictReader(codecs.iterdecode(csv_file.file, 'utf-8'))
			csv_items = []
			for row in csv_reader:
				csv_items.append(json.loads(json.dumps(row)))
			return csv_items

	@staticmethod
	async def get_email_from_header(data):
		email_types = ['Primary Work Email', 'primary_work_email', 'email_address', 'email']
		email_type = list(set(email_types).intersection(data))
		if bool(email_type):
			return data.get(email_type[0])
		else:
			raise Exception

	@staticmethod
	async def get_fname_from_header(data):
		name_types = ['Legal First Name', 'legal_first_name', 'firstname', 'first_name']
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			raise Exception

	@staticmethod
	async def get_lname_from_header(data):
		name_types = ['Legal Last Name', 'legal_last_name', 'lastname', 'last_name']
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			raise Exception

	@classmethod
	async def check_for_existing(cls, model, search_by):
		with Session(engine) as session:
			item = session.get(model, search_by)
			return (item if item else None)

	@staticmethod
	async def update(statement, updates):
		with Session(engine) as session:
			response = session.scalars(statement).one_or_none()
			await ExceptionHandling.check404(response)

			updated_mapped_columns = updates.dict(exclude_unset=True)
			for key, value in updated_mapped_columns.items():
				setattr(response, key, value)
			session.add(response)
			session.commit()
			session.refresh(response)
			return response

	@staticmethod
	async def generate_9char():
		generator = PositiveNumbers.PositiveNumbers(size=9)
		uuid_time = int(str(time.time()).replace('.', '')[:16])
		char_9 = generator.encode(uuid_time)
		return char_9

	@staticmethod
	def generate_UUID(input_string=None):
		return SHA224Hash(input_string)
