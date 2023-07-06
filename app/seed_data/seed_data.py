from faker import Faker
from time import time
from app.models.users import UserModel,  UserServiceModelDB
from app.models.clients import ClientModelDB, ClientUserModelDB, ClientBudgetModelDB
from app.models.award import AwardModelDB

fake = Faker()

def generate_seed_data():
    
    # the first 2 uuid's are being used for the 2 client_users
    client_uuid_list = [
    "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
    "f45c9e73e70c47b2ae8c95a28309e6d1f2f8b24a9a0d4df0979c5e",
    "0ef80fcb3d92494daaaeff6c2dc5e48983c97377d78045e58db43c",
    "b56a74a45b2f4016ab6d00f3e36c3b2a93d6849a46494e3d9a0f70",
    "db8f1c6a764e4b5893d3eaa726a15530a8f6f6e6d5b84c73b9c52a",
    "63af66248f5e4d0799b442c73d06f22b71fc2c64b7a74579a2a08a",
    "a54f79e84c2c49929663d1dc413af075c0edcc2402b148cd9ad21e",
    "1e9e6f803b354eb98aa03c79b47e83594be38dd45e7c41c79a5c27",
    "7daeb6ccf24a47fba96cc0b31a4f3a7c5ccedca91e1146edbf0f46",
    "1493abab133e4dcdb699e37c69c2d5d13584c6365a774f13a4ee71"
    ]

    client_user_uuid_list = [
    "2f5bcb5e7e08415bbdd25b111d045b13817b437e4a4345e7be573a",
    "9e31b2c87f0e4e9d826a99e3b6d9ff497430e377b90f4aeeb493a6"
    ]

    client_budget_uuid_list = [
    "d2a6c149d8124fcaad1da05f7b743bf5c7f3b11f145048ef88d996",
    "af3bca4a1a9748558d67236d58d15e8d9e3e6df16a0246e399fcb9",
    "d8dc8e0c4fd84e8d9448b66920e1b5b213f081cfdfc647d08f7e7e",
    "5c0f879e0c0d4b5fa89d6a963708f719ef369d89e2f340c4832e49",
    "7f4e63c5ea894d329e1267d9e1d0627a27f66e54d24e416993c526",
    "eaeac352c36c4e0b99e9c25a9ee6a15c6f3e344f3fc14d548c5431"
    ]

    award_uuid_list = [
    "f8e53c5f0b9f46f08e5975d31d91f76a55a82be2f9c54da89b0b9f",
    "367c041785fa4fc9b8d2bfa49e4428d1a8dbb77318a64257b6f646",
    "54a8e604b19b4f77a24d1b3d8499571b97dc3ef9849c40a3b9e4a3",
    "06e8e7ff157147d1a8b736f64e24fc9e070d45a2a4914dc995c734",
    "e891d1e649cc4ed1aa5e4299b3941b61832f44d9b3b347b5a30d7b",
    "2016c75fe1574f189a6e6785b2db3efeb22869e4e7e549f5b8d84b",
    "f88d99d803b74f8eae87e7cb9b6d6fbf1b74c3e738d74f8ebe8e34",
    "87c749b7e4374e00bfb0d1c9d628f3a5b3b790eb43af4eb1b6f7bb"
    ]

    user1 = UserModel(
            uuid="55063ccb52750171d9138f6293d93330e5be577fba84e92d72856426",
            first_name="TestUser",
            last_name="CellService",
            latitude=407127281,
            longitude=-740060152,
            time_created=1686591427,
            time_updated=1686591427,
            time_ping=1686591427
        )

    user2 = UserModel(
            uuid="0e58cd793a1d465c638276e450a92d82082f640b494fbc7735478aa9",
            first_name="TestUser",
            last_name="EmailService",
            latitude=407127281,
            longitude=-740060152,
            time_created=1686591427,
            time_updated=1686591427,
            time_ping=1686591427
        )
    
    user1_service = UserServiceModelDB(
        uuid= "a59a0209ab829e672d748026608bdcc19695d01b3e56ffc0d6adb29e",
        user_uuid= "55063ccb52750171d9138f6293d93330e5be577fba84e92d72856426",
        service_uuid= "cell",
        service_user_id= "15005550006",
        service_user_screenname= "TestUser CellService",
        service_user_name= "testusercellservice",
        service_access_token= "access token",
        service_access_secret= "secret token",
        service_refresh_token= "refresh token",
        time_created= 1686591427,
        time_updated= 1686591427,
        login_secret="place_holder",
        login_token="place_holder"
    )

    user2_service = UserServiceModelDB(
        uuid="774339d7415fe0f393cb401ed6efdb3537af7b0b9a1235bf542767b1",
        user_uuid="0e58cd793a1d465c638276e450a92d82082f640b494fbc7735478aa9",
        service_uuid="email",
        service_user_id="test.user@testclient.com",
        service_user_screenname="TestUser EmailService",
        service_user_name="testuseremailservice",
        service_access_token="access token",
        service_access_secret="secret token",
        service_refresh_token="refresh token",
        time_created=1686591427,
        time_updated=1686591427,
        login_secret="place_holder",
        login_token="place_holder"
    )

    user_seed_data = [user1, user2]
    
    user_service_seed_data = [user1_service, user2_service]
    
    all_seed_data = [user_seed_data, user_service_seed_data]

    client_seed_data = [
        ClientModelDB(
            uuid=uuid,
            url=fake.url(),
            name=fake.first_name(),
            description=fake.sentence(),
            time_created=int(time()),
            time_updated=int(time()),
            time_ping=int(time()),
            status=1
        ) for uuid in client_uuid_list]
    
    

    client_user_seed_data = []
    for i, uuid in enumerate(client_user_uuid_list):
        client_user = ClientUserModelDB(
            uuid=uuid,
            user_uuid=client_user_uuid_list[i],
            client_uuid=client_uuid_list[i],
            manager_uuid=None,
            employee_id=None,
            title=fake.job(),
            department=fake.state(),
            active=True,
            time_hire=int(time()),
            time_start=int(time()),
            admin=1
        )
        client_user_seed_data.append(client_user)


    # index 0 and 3 are the static budgets in budget_names, budget_values, and budget_9chars
    budget_names = ["static_budget_1", "parent_budget_1", "sub_budget_1", "static_budget_2", "parent_budget_2", "sub_budget_2"]
    budget_values = [1000, 500, 250, 1000, 500, 250]
    budget_9chars = ["8aB3yH9Zx", "7cD4pQ8Mw", "2eF9rT6Lu", "5gI2sK1Jv", "1iL5uO3Px", "4kN7wR0Ty"]
    parent_9chars = [None, "8aB3yH9Zx", "7cD4pQ8Mw", None, "5gI2sK1Jv", "1iL5uO3Px"]
    client_budget_seed_data = [
        ClientBudgetModelDB(
            uuid=uuid,
            budget_9char=budget_9chars[i],
            parent_9char=parent_9chars[i],
            name=budget_names[i],
            value=budget_values[i],
            active=True,
            budget_type=1
        ) for i, uuid in enumerate(client_budget_uuid_list)
    ]


    award_names = ["Ivory", "White Gold", "Indigo", "Tiburon", "Emerald", "Ruby", "Aviator", "Iconic"]
    award_values = [150, 250, 500, 1000, 2500, 5000, 10000, 25000]
    award_descriptions = ["Experience Menu Only", "Experience Menu Only", "Experience Menu Only", "Build Your Own Experience (BYOE), Typically Domestic Travel", "Build Your Own Experience (BYOE), Typically Domestic Travel", "Build Your Own Experience (BYOE), International Travel", "Build Your Own Experience (BYOE), International Travel", "Build Your Own Experience (BYOE), International Travel"]
    award_seed_data = [
        AwardModelDB(
            uuid=uuid,
            name=award_names[i],
            description=award_descriptions[i],
            hero_image=1,
            channel=1,
            award_type=1,
            value=award_values[i]
        ) for i, uuid in enumerate(award_uuid_list)
    ]

    return user_seed_data + user_service_seed_data + client_seed_data + client_user_seed_data + client_budget_seed_data + award_seed_data
    # all_seed_data = [user_seed_data, user_service_seed_data, client_seed_data, client_user_seed_data, client_budget_seed_data, award_seed_data]
    # final_seed_data = {
    #     user_seed_data[0].__tablename__: user_seed_data,
    #     user_service_seed_data[0].__tablename__: user_service_seed_data,
    #     client_seed_data[0].__tablename__: client_seed_data,
    #     client_user_seed_data[0].__tablename__: client_user_seed_data,
    #     client_budget_seed_data[0].__tablename__: client_budget_seed_data,
    #     award_seed_data[0].__tablename__: award_seed_data
    # }

    final_seed_data = {
        list[0].__tablename__:list for list in all_seed_data
    }





