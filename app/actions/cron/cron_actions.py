
import pandas as pd
from sqlalchemy.orm import Session
from app.database.config import engine
from sqlalchemy import select
from app.actions.users import UserActions
from app.models.users import UserModelDB
from app.routers.v1.v1CommonRouting import ExceptionHandling
from pprint import pprint as pp
import json


rule = '{"admin":"2"}'


class CronActions:

    @classmethod
    async def kick_off(cls, query_params):
        users = await cls.get_all_cron(UserModelDB)
        users_df = pd.DataFrame(users)
        rule_dict = json.loads(rule)
        result = await cls.run_rule(users_df, rule_dict)
        return result

    @classmethod
    async def get_all_cron(cls, model):
        with Session(engine) as session:
            query = select(model)
            db_query = session.scalars(query).all()
            await ExceptionHandling.check404(db_query)
            return db_query

    @classmethod
    async def run_rule(cls, users_df, rule_dict):
        admin_level = int(rule_dict['admin'])
        results = users_df[users_df['admin'] == admin_level]
        results = results.reindex()
        ret = results.to_dict('records')
        return ret
