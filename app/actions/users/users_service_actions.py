from app.models.users import UsersServiceModel, UsersModel
from app.utilities import SHA224Hash
from time import time
from app.routers.v1.v1CommonRouting import CommonRoutes
from .users_actions import UsersActions
from app.actions.commonActions import CommonActions

class UsersServiceActions():

    @classmethod
    async def csv_upload(cls, csv_file):
        user_list = CommonActions.process_csv(csv_file)
        users = []
        for user in user_list:
            users.append(cls.create_service_user(user))
        return users

    @classmethod
    async def create_service_user(cls, employee_data):
        email_types = ['Primary Work Email', 'primary_work_email', 'email_address']
        email_type = list(set(email_types).intersection(employee_data))
        if bool(email_type):
            employee_email = employee_data.get(email_type[0])
        else:
            raise Exception
        user = await UsersActions.get_user_by_service_user_id(employee_email)
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
                time_birthday=  UsersActions.getTimeFromBday(employee_data['Hire Date']),
            )
            new_user = CommonRoutes.create_one_or_many(new_user)

            new_user_service = UsersServiceModel(
                user_uuid= new_user.uuid,
                service_uuid= SHA224Hash(),
                service_user_id= employee_email,
                service_user_screenname= f"{new_user.first_name} {new_user.last_name}",
                service_user_name= CommonActions.make_username(new_user.first_name, new_user.last_name),
                service_access_token= "access token",
                service_access_secret= "secret token",
                service_refresh_token= "refresh token",
            )
            CommonRoutes.create_one_or_many(new_user_service)
            return new_user # or add to list of users
