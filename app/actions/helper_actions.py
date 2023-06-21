import csv
import codecs
import json
import time

from collections import namedtuple
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
			csv_reader = csv.DictReader(codecs.iterdecode(csv_file.file, "utf-8"))
			csv_items = []
			for row in csv_reader:
				csv_items.append(json.loads(json.dumps(row)))
			return csv_items

	ServiceType = namedtuple("ServiceType", ["type", "value"])

	@classmethod
	def flatten(cls, seq):
		output = []
		for elt in seq:
			if type(elt) is tuple or type(elt) is list:
				for elt2 in cls.flatten(elt):
					output.append(elt2)
			else:
				output.append(elt)
		return output

	@classmethod
	async def get_email_from_header(cls, data):
		email_types = {"Primary Work Email", "primary_work_email", "email_address", "email"}
		email_type = list(email_types.intersection(data))
		if bool(email_type):
			return cls.ServiceType(type="email", value=data.get(email_type[0]))
		else:
			return None

	@classmethod
	async def get_cell_from_header(cls, data):
		cell_types = {"Primary Cell Number", "primary_cell_number", "cell_number", "cell"}
		cell_type = list(cell_types.intersection(data))
		if bool(cell_type):
			cell_value = data.get(cell_type[0])
			cell_value = cell_value.replace("-", "").replace("(", "").replace(")", "").strip()
			return cls.ServiceType(type="cell", value=cell_value)
		else:
			return None

	@staticmethod
	async def get_fname_from_header(data):
		name_types = ["Legal First Name", "legal_first_name", "firstname", "first_name"]
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			raise Exception

	@staticmethod
	async def get_lname_from_header(data):
		name_types = ["Legal Last Name", "legal_last_name", "lastname", "last_name"]
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			raise Exception
		
	@staticmethod
	async def get_manager_uuid(data):
		name_types = ["manager_uuid", "Manager ID", "Manager UUID", "manager_id"]
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			return
			# raise Exception
		
	@staticmethod
	async def get_employee_id(data):
		name_types = ["employee id", "employee_id", "Employee ID"]
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			return
			# raise Exception

	@staticmethod
	async def get_title(data):
		name_types = ["title", "business title", "Business Title", "Title"]
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			return
			# raise Exception

	@staticmethod
	async def get_department(data):
		name_types = ["department", "Department"]
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			return
			# raise Exception

	@staticmethod
	async def get_active(data):
		name_types = ["active", "Active"]
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			return
			# raise Exception

	@staticmethod
	async def get_admin(data):
		name_types = ["admin", "Admin"]
		name_type = list(set(name_types).intersection(data))
		if bool(name_type):
			return data.get(name_type[0])
		else:
			return 1
			# raise Exception

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
		uuid_time = int(str(time.time()).replace(".", "")[:16])
		char_9 = generator.encode(uuid_time)
		return char_9

	@staticmethod
	async def generate_UUID(input_string=None):
		return SHA224Hash(input_string)
