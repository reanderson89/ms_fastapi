import codecs
import csv
import json
from fastapi import UploadFile, File
from app.models.users import UsersServiceModel, UsersModel
from app.database.config import engine
from sqlmodel import Session, select
from app.utilities import SHA224Hash
from time import time
from datetime import datetime
from app.routers.v1.v1CommonRouting import CommonRoutes

class UsersActions():

    @classmethod
    async def check_for_existing(cls, email):
        user = await cls.get_user_by(email)
        if not user:
            return None
        else:
            return CommonRoutes.get_one(UsersModel, user.user_uuid)

    @staticmethod
    def getTimeFromBday(bday):
        date_obj = datetime.strptime(bday, '%m/%d/%y')
        epoch_time = int(date_obj.timestamp())
        return epoch_time

    @staticmethod
    def make_username(first, last):
        first = first.lower()
        last = last.lower()
        return f"{first}{last}"

    @classmethod
    async def process_csv(cls, csv_file: UploadFile = File(...)):
            csv_reader = csv.DictReader(codecs.iterdecode(csv_file.file, 'utf-8'))
            users = []
            for row in csv_reader:
                user_data = json.loads(json.dumps(row))
                user = await cls.create_service_user(user_data)
                users.append(user)
            return users

    @classmethod
    async def create_service_user(cls, employee_data):
        if 'Primary Work Email' in employee_data or 'primary_work_email' in employee_data:
            employee_email = employee_data.get('Primary Work Email') or employee_data.get('primary_work_email')
        else:
            raise Exception
        print(employee_email)
        user = await cls.check_for_existing(employee_email)
        if user:
            return user
        elif not user:
            #get_coordinates(employee_data["location"]) # ask Jason, is this a call to Nominatim???
            new_user = UsersModel(
                first_name = employee_data['Legal First Name'],
                last_name= employee_data['Legal Last Name'],
                latitude = 407127281,
                longitude = -740060152,
                time_ping= int(time()),
                time_birthday=  cls.getTimeFromBday(employee_data['Hire Date']),
            )
            new_user = CommonRoutes.create_one_or_many(new_user)

            new_user_service = UsersServiceModel(
                user_uuid= new_user.uuid,
                service_uuid= SHA224Hash(),
                service_user_id= employee_email,
                service_user_screenname= f"{new_user.first_name} {new_user.last_name}",
                service_user_name= cls.make_username(new_user.first_name, new_user.last_name),
                service_access_token= "access token",
                service_access_secret= "secret token",
                service_refresh_token= "refresh token",
            )
            new_user_service = CommonRoutes.create_one_or_many(new_user_service)


            return new_user, new_user_service # or add to list of users

    @classmethod
    async def get_user_by(cls, search_by):
        with Session(engine) as session:
            return session.exec(select(UsersServiceModel)
                                .where(UsersServiceModel.service_user_id == search_by)).one_or_none()
