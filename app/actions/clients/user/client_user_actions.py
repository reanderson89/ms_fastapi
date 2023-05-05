from app.actions.users import UsersActions
from app.actions.users.services import UserServiceActions
from app.models.clients.user import ClientUserModel
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.utilities import SHA224Hash
from time import time
from sqlmodel import select

class ClientUserActions():

    @classmethod
    async def createClientUser(cls, data, client_uuid):
        user = None
        if 'user_uuid' in data.keys():
            user = await UsersActions.get_user_by_uuid(data['user_uuid'])

        """
        double if's here in the event that the above does not return a user. an else would skip this
        if no user was returned from above, the following function call will do:
        1. try and retrieve a UserServiceModel that contains the email address contained in `data`
        2. if no user was matched from the email, create a new UserServiceModel
        3. create a new user model
        4. create a new client user model
        """
        if user is None:
            user = await UserServiceActions.create_service_user(data)

        newClientUser = ClientUserModel(
            uuid=SHA224Hash(),
            user_uuid= user.uuid,
            client_uuid= client_uuid,
            manager_uuid= data['Manager ID'] if 'Manager ID' in data else None,
            employee_id= data['Employee ID'] if 'Employee ID' in data else None,
            title= data['Business Title'] if 'Business Title' in data else None,
            department= data['Department'] if 'Department' in data else None,
            active=data['Active'] if 'Active' in data else True,
            time_hire=int(time()),
            time_start=int(time()),
            admin= data['Admin'] if 'Admin' in data else 0,
        )
        newClientUser = CommonRoutes.create_one_or_many(newClientUser)
        return newClientUser

    @classmethod
    async def getExpandedClientUsers(cls, data, client_uuid, expansion):
        pass

    @staticmethod
    async def getAllUsers(client_uuid, session):
        users = session.exec(
            select(ClientUserModel)
            .where(ClientUserModel.client_uuid == client_uuid)
        ).all()
        ExceptionHandling.check404(users)
        return users

    @staticmethod
    async def getUser(client_uuid, user_uuid, session):
        user = session.exec(
            select(ClientUserModel)
            .where(ClientUserModel.client_uuid == client_uuid,
                    ClientUserModel.uuid == user_uuid)
        ).one_or_none()
        ExceptionHandling.check404(user)
        return user

    @staticmethod
    async def updateUser(client_uuid, user_uuid, user_updates, session):
        user = session.exec(
            select(ClientUserModel)
            .where(ClientUserModel.client_uuid == client_uuid,
                    ClientUserModel.uuid == user_uuid)
            ).one_or_none()
        ExceptionHandling.check404(user)
        update_user = user_updates.dict(exclude_unset=True)
        for key, value in update_user.items():
            setattr(user, key, value)
        user.time_updated = int(time())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    async def deleteUser(client_uuid, user_uuid, session):
        user = session.exec(
            select(ClientUserModel)
            .where(ClientUserModel.client_uuid == client_uuid,
                    ClientUserModel.uuid == user_uuid)
        ).one_or_none()
        ExceptionHandling.check404(user)
        session.delete(user)
        session.commit()
        return {"ok": True, "Deleted": user}
