from dotenv import load_dotenv

from app.exceptions import ExceptionHandling
from app.models.clients import ClientUserExpand, CreateClientUser
from app.worker.temp_worker import TempWorker
from burp.models.client_user import ClientUserModel, ClientUserModelDB
from burp.models.user import UserModel
from burp.utils.base_crud import BaseCRUD
from burp.utils.helper_actions import HelperActions
from burp.utils.utils import SHA224Hash, convert_date_to_int

load_dotenv()


class ClientUserActions:

    @staticmethod
    async def get_client_user_by_user_uuid(client_uuid: str, user_uuid: str):
        return await BaseCRUD.check_if_exists(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == client_uuid,
                ClientUserModelDB.user_uuid == user_uuid
            ]
        )

    @staticmethod
    async def expand_client_user(client_user, user):
        client_user_expanded = ClientUserExpand.from_orm(client_user)
        client_user_expanded.user = user
        return client_user_expanded

    @classmethod
    async def handle_client_user_job(cls, job_data: dict):
        data: dict = job_data.get("body", {})
        user_data = CreateClientUser(**data.get("user", {}))
        path_params: dict = {"client_uuid": data.get("client_uuid")}
        client_user = await cls.create_client_user(user_data, path_params)
        return client_user

    @classmethod
    async def create_client_user(cls, data: CreateClientUser, path_params: dict, expand: bool = True):
        service_id = ["work_email", "personal_email", "cell_phone", "email_address"]
        user_objs = []
        client_user_objs = []
        for service in service_id:
            service_value = getattr(data, service, None)
            if service_value:
                response_obj = await cls.handle_user_and_service(data, path_params, expand, service)
                if type(response_obj) is UserModel:
                    user_objs.append(response_obj)
                elif type(response_obj) in (ClientUserModel, ClientUserExpand):
                    client_user_objs.append(response_obj)
        if not (user_objs or client_user_objs):
            raise ValueError("No user or client user objects returned")

        user_uuids = [user.uuid for user in user_objs if user is not None]
        if len(set(user_uuids)) > 1:
            raise ValueError("Multiple user objects returned for different service IDs")

        client_user_uuids = [client_user.uuid for client_user in client_user_objs if client_user is not None]
        if len(set(client_user_uuids)) > 1:
            raise ValueError("Multiple client user objects returned for different service IDs")

        user_obj = user_objs[0] if user_objs else None
        client_user_obj = client_user_objs[0] if client_user_objs else None

        client_user = await cls.add_new_client_user(
            data, path_params, user_obj
        ) if not client_user_obj else client_user_obj
        return client_user

    @classmethod
    async def handle_user_and_service(cls, data: CreateClientUser, path_params, expand, service_id=None):
        worker = TempWorker()
        user = None
        user_uuid = getattr(data, "user_uuid", None)
        service = getattr(data, service_id, None)

        # raise error if both user_uuid and service are None
        if not (user_uuid or service):
            return await ExceptionHandling.custom500(
                "Not enough information to create a new Client User. Please include either an email address or user_uuid."
            )

        try:
            if user_uuid:
                # check if user exists
                user_response = await worker.get_user_job(user_uuid)
                user = UserModel(**user_response) if user_response else None
            elif service:
                request_obj = {"service_user_id": service}
                user_response = await worker.alt_get_user_job(**request_obj)
                user = UserModel(**user_response) if user_response else None
        except Exception as e:
            return await ExceptionHandling.custom404(f"User not found with error: {e}")

        if user:
            uuid = user.uuid
            client_user = await cls.get_client_user_by_user_uuid(path_params["client_uuid"], uuid)
            if client_user:
                if expand:
                    return await cls.expand_client_user(client_user, user)
                return client_user
            else:
                return user
        elif service:
            admin = getattr(data, "admin", 0)
            admin = 0 if admin is None else admin
            if admin not in [0, 1, 2]:
                await ExceptionHandling.custom409("Invalid value for admin field, must be 0 or 1.")

            user_response = await worker.create_user_job(data.dict())
            user = UserModel(**user_response) if user_response else None
            # UserActions.create_user_and_service(data, service_id)
            return user
        else:
            return await ExceptionHandling.custom409(
                "Not enough information to create a new Client User, User, and Service User."
            )

    @classmethod
    async def add_new_client_user(
        cls,
        data: CreateClientUser,
        path_params: dict,
        user,
        expand: bool = False
    ):
        # Check if client user already exists
        client_user = await cls.get_client_user_by_user_uuid(user.uuid, user.uuid)

        if not client_user:
            client_user_obj = ClientUserModelDB(
                uuid=SHA224Hash(),
                user_uuid=user.uuid,
                client_uuid=path_params.get("client_uuid", None),
                manager_uuid=await HelperActions.get_manager_uuid(data),
                employee_id=await HelperActions.get_employee_id(data),
                title=await HelperActions.get_title(data),
                department=await HelperActions.get_department(data),
                active=await HelperActions.get_active(data) if "active" in data.dict().keys() else 1,
                time_hire=convert_date_to_int(getattr(data, "time_hire", None)),
                time_start=convert_date_to_int(getattr(data, "time_start", None)),
                admin=await HelperActions.get_admin(data),
            )

            client_user = await BaseCRUD.create(client_user_obj)
        return await cls.expand_client_user(client_user, user)

    @classmethod
    async def getExpandedClientUsers(cls, data, client_uuid, expansion):
        pass

    @staticmethod
    async def get_all_users(client_uuid: str, query_params: dict):
        return await BaseCRUD.get_all_where(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == client_uuid
            ],
            query_params
        )

    @staticmethod
    async def get_user(path_params):
        return await BaseCRUD.get_one_where(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == path_params["client_uuid"],
                ClientUserModelDB.user_uuid == path_params["user_uuid"]
            ]
        )

    @staticmethod
    async def auth_get_user(user_uuid):
        return await BaseCRUD.get_one_where(
            ClientUserModelDB,
            [
                ClientUserModelDB.user_uuid == user_uuid
            ]
        )

    @staticmethod
    async def update_user(path_params: dict, user_updates):
        return await BaseCRUD.update(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == path_params["client_uuid"],
                ClientUserModelDB.uuid == path_params["user_uuid"]
            ],
            user_updates
        )

    @staticmethod
    async def update_users(path_params, user_updates):
        uuid_list = []
        for user in user_updates:
            if user.uuid:
                uuid_list.append(user.uuid)
            else:
                return await ExceptionHandling.custom400(f"Missing uuid in user update list for: {user}")
        return await BaseCRUD.bulk_update(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == path_params.get("client_uuid"),
            ],
            user_updates,
            uuid_list
        )

    @staticmethod
    async def update_admin_client_user(path_params: dict, user_updates):
        if path_params.get("client_uuid") is None:
            conditions = [ClientUserModelDB.user_uuid == path_params["user_uuid"]]
        else:
            conditions = [
                ClientUserModelDB.client_uuid == path_params["client_uuid"],
                ClientUserModelDB.user_uuid == path_params["user_uuid"]
            ]

        return await BaseCRUD.update(
            ClientUserModelDB,
            conditions,
            user_updates
        )

    @staticmethod
    async def delete_user(path_params):
        return await BaseCRUD.delete_one(
            ClientUserModelDB,
            [
                ClientUserModelDB.client_uuid == path_params["client_uuid"],
                ClientUserModelDB.uuid == path_params["user_uuid"]
            ]
        )
