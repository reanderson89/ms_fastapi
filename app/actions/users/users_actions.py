from app.models.users import UsersServiceModel, UsersModel
from app.database.config import engine
from sqlmodel import Session, select
from datetime import datetime
from app.routers.v1.v1CommonRouting import CommonRoutes

class UsersActions():

    @staticmethod
    def getTimeFromBday(bday):
        date_obj = datetime.strptime(bday, '%m/%d/%y')
        epoch_time = int(date_obj.timestamp())
        return epoch_time

    @classmethod
    async def check_for_existing(cls, email):
        user = await cls.get_user_by_service_user_id(email)
        if not user:
            return None
        else:
            return user

    @classmethod
    async def get_user_by_service_user_id(cls, search_by):
        with Session(engine) as session:
            return session.exec(select(UsersModel)
                                .where(UsersServiceModel.service_user_id == search_by)
                                .where(UsersServiceModel.user_uuid == UsersModel.uuid)).one_or_none()
