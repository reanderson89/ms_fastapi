import os
from faker import Faker
from faker.providers import job
from app.models.clients import CreateClientUser
from app.actions.clients.user import ClientUserActions
import httpx
from httpx import ConnectError
from dotenv import load_dotenv
load_dotenv()

YASS_URL = os.environ.get("YASS_URL")

Faker.seed(0)
faker = Faker()
faker.add_provider(job)


def fake_date():
    return int(faker.date_time_between(start_date="-1y", end_date="now").timestamp())


def fake_bday():
    return int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp())

admins = {
    "owen": {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "owen.plambeck@blueboard.com",
        "first_name": "Owen",
        "last_name": "Plambeck",
        "title": "Sr Bug Creator",
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "department": "Sr Bug Creator",
        "admin": 2,
        "time_start": fake_date(),
        "time_hire": fake_date(),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": fake_bday()
    },
    "clark": {
        "user_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "clark.ritchie@blueboard.com",
        "first_name": "Clark",
        "last_name": "Ritchie",
        "title": "Domestique",
        "department": "Domestique", #faker doesnt have a job department field
        "admin": 2,
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "time_start": fake_date(),
        "time_hire": fake_date(),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": fake_bday() #we dont ask for birthday during client user creation
    },
    "rob": {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "rob.anderson@blueboard.com",
        "first_name": "Rob",
        "last_name": "Anderson",
        "title": "Assistent to the Assistence Manager",
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "department": "Racecar Recreation Enthusiast",
        "admin": 2,
        "time_start": fake_date(),
        "time_hire": fake_date(),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": fake_bday() #we dont ask for birthday during client user creation
    },
    "jason": {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "jason@blueboard.com",
        "first_name": "Jason",
        "last_name": "Wiener",
        "title": "Quality Assurance Intern",
        "department": "Quality Assurance Intern", #faker doesnt have a job department field
        "admin": 2,
        "manager_uuid": None,
        "time_start": fake_date(),
        "time_hire": fake_date(),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": fake_bday() #we dont ask for birthday during client user creation
    },
    "josh": {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "joshua.crowley@blueboard.com",
        "first_name": "Josh",
        "last_name": "Crowley",
        "title": "Bug Fixer",
        "department": "Tooth Hurts",
        "admin": 2,
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "time_start": fake_date(),
        "time_hire": fake_date(),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": fake_bday() #we dont ask for birthday during client user creation
    },
    "test_user": {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "test.user@testclient.com",
        "first_name": "Test",
        "last_name": "User",
        "title": "Test User",
        "department": "Test Department",
        "admin": 2,
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "time_start": fake_date(),
        "time_hire": fake_date(),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": fake_bday() #we dont ask for birthday during client user creation
    },
}

new_admins = list(admins.values())


async def generate_client_users(clients: list):
    # create clarks user first
    async with httpx.AsyncClient() as client:
        try:
            await client.post(f"{YASS_URL}/users", json=admins["clark"])
        except ConnectError:
            print("Could not connect to YASS API. Adding 'Clark' admin skipped during debugging.")

    for admin in new_admins:
        admin_client_user = CreateClientUser(**admin)
        try:
            await ClientUserActions.create_client_user(
                admin_client_user,
                {"client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34"}
            )
        except Exception as e:
            print(e)
            print("Could not create admin user. Skipping during debugging.")

    # Uncomment if you want the full list of client_users, users, and user_services to be created
    # import pandas as pd
    # from datetime import timedelta
    # from app.seed_data.seed_clients.client_user_uuids import client_user_uuid_list


    # base = pd.Timestamp.today()
    # timestamp_list = [int((base - timedelta(days=x)).timestamp()) for x in range(370)]
    # for client in clients:
    #     if client.name != "Blueboard":
    #         for i in range(0, 37):
    #             if i == 0:
    #                 uuid = client_user_uuid_list.pop()
    #                 manager_uuid = uuid
    #             time_use = timestamp_list.pop()
    #             await ClientUserActions.create_client_user(
    #                 {
    #                     "uuid": uuid,
    #                     "client_uuid": client.uuid,
    #                     "work_email": f"faker_test_email+{faker.email()}",
    #                     "first_name": faker.first_name(),
    #                     "last_name": faker.last_name(),
    #                     "title": faker.job(),
    #                     "department": f"{faker.job()} Department", #faker doesnt have a job department field
    #                     "manager_uuid": manager_uuid,
    #                     "admin": 1,
    #                     "time_start": time_use,
    #                     "time_hire": time_use,
    #                     "active": 1,
    #                     "employee_id": faker.pystr(),
    #                     "time_birthday": fake_bday(), #we dont ask for birthday during client user creation
    #                 },
    #                 {"client_uuid": client.uuid, "user_uuid": None}
    #             )
