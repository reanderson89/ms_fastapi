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
        user = await cls.get_user_by(email)
        if not user:
            return None
        else:
            return CommonRoutes.get_one(UsersModel, user.user_uuid)

    @classmethod
    async def get_user_by(cls, search_by):
        with Session(engine) as session:
            return session.exec(select(UsersServiceModel)
                                .where(UsersServiceModel.service_user_id == search_by)).one_or_none()
