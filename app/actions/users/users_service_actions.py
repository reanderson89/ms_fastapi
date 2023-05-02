import codecs
import csv
import json
from fastapi import UploadFile, File
from app.models.users import UsersServiceModel, UsersModel
from app.utilities import SHA224Hash
from time import time
from app.routers.v1.v1CommonRouting import CommonRoutes
from .users_actions import UsersActions

class UsersServiceActions():

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
                user = await UsersServiceActions.create_service_user(user_data)
                users.append(user)
            return users

    @classmethod
    async def create_service_user(cls, employee_data):
        if 'Primary Work Email' in employee_data or 'primary_work_email' in employee_data:
            employee_email = employee_data.get('Primary Work Email') or employee_data.get('primary_work_email')
        else:
            raise Exception
        print(employee_email)
        user = await UsersActions.check_for_existing(employee_email)
        if user:
            return user
        elif not user:
            #get_coordinates(employee_data["location"]) # ask Jason, is this a call to Nominatim???
            new_user = UsersModel(
                first_name = (employee_data['legal_first_name'] or employee_data['Legal First Name']),
                last_name= (employee_data['legal_last_name'] or employee_data['Legal Last Name']),
                latitude = 407127281,
                longitude = -740060152,
                time_ping= int(time()),
                time_birthday=  UsersActions.getTimeFromBday(employee_data['hire_date'] or employee_data['Hire Date']),
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
            CommonRoutes.create_one_or_many(new_user_service)
            return new_user # or add to list of users
