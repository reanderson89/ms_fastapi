from app.actions.base_actions import BaseActions
from app.models.award import AwardModel, AwardUpdate


class AwardActions(BaseActions):

	@classmethod
	async def get_all_awards(cls, query_params: dict):
		"""
		Get all awards from the database
		:params query_params(dict): A dictionary of query parameters
			- order_by(str): The field to sort by
			- sort(str): The sort order ('ASC' or 'DESC')
			- offset(int): The number of results to skip
			- limit(int): The maximum number of results to return
		:return: A list of model objects, for example [model(DataModel),...]
		"""
		return await cls.get_all(
			AwardModel,
			query_params
		)

	@classmethod
	async def get_awards_where(cls, conditions: list, query_params: dict):
		"""
		Get all awards from the database that match the specified conditions
		:param conditions(list): A list of conditions to match
		:param params(dict): A dictionary of query parameters
			- order_by(str): The field to sort by
			- sort(str): The sort order ('ASC' or 'DESC')
			- offset(int): The number of results to skip
			- limit(int): The maximum number of results to return
		:return: A list of model objects, for example [model(DataModel),...]
		"""
		return await cls.get_all_where(
			AwardModel,
			conditions,
			query_params
		)

	@classmethod
	async def get_award(cls, award_uuid: str):
		"""
		Get one award from the database
		:param award_uuid(str): The uuid of the award to query
		:return: The award model(DataModel instance)
		"""
		return await cls.get_one_where(
			AwardModel,
			[AwardModel.uuid == award_uuid]
		)

	@classmethod
	async def create_award(cls, award_objs):
		"""
		Create one or more awards in the database
		:param award_objs(AwardModel | list[AwardModel]): A list of Award models to create
		:return: The list of created award models
		"""
		return await cls.create(award_objs)

	@classmethod
	async def update_award(cls, award_uuid: str, update_obj: AwardUpdate):
		"""
		Update one award in the database
		:param award_uuid(str): The uuid of the award to update
		:param update_obj(AwardUpdate):The model object containing the updated fields
		:return: The updated award model
		"""
		return await cls.update(
			AwardModel,
			[AwardModel.uuid == award_uuid],
			update_obj
		)

	@classmethod
	async def delete_award(cls, award_uuid: str):
		"""
		Delete one award from the database
		:param award_uuid(str): The uuid of the award to delete
		:return: Status of deletion and the deleted model object
		"""
		return await cls.delete_one(
			AwardModel,
			[AwardModel.uuid == award_uuid]
		)

	@classmethod
	async def delete_all_where(cls, conditions: list):
		"""
		Delete all awards from the database that match the specified conditions
		:param conditions(list): A list of conditions to filter by
		:return: Status of deletion and the deleted model object(s)
		"""
		return await cls.delete_all(
			AwardModel,
			conditions
		)
















    # @classmethod
    # async def create_award_handler(cls, awards):

    #     if not isinstance(awards, list):
    #         awards = list(awards)

    #     return [
    #         cls.create_award(awards)
    #         for award in awards
    #     ]


    # @classmethod
    # async def create_award(cls, award_data):
    #     check = await cls.check_for_existing(award_data.name)
    #     if check:
    #         return check

    #     new_award = AwardModel(
    #         name=award_data.name,
    #         award_type=award_data.award_type,
    #         value=award_data.value
    #     )
    #     return await CommonRoutes.create_one_or_many(new_award)


    # @classmethod
    # async def check_for_existing(cls, name):
    #     client = await cls.get_award_by_name(name)
    #     if client:
    #         return client


    # @classmethod
    # async def get_award_by_name(cls, search_by):
    #     with Session(engine) as session:
    #         return session.exec(
    #             select(AwardModel).where(AwardModel.name == search_by)
    #         ).one_or_none()


    # @staticmethod
    # async def get_name_by_uuid(search_by):
    #     with Session(engine) as session:
    #         return session.exec(
    #             select(AwardModel.name).where(AwardModel.uuid == search_by)
    #         ).one_or_none()
