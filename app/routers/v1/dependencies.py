from enum import Enum
from typing import Optional
from fastapi import Query
from app.actions.base_actions import BaseActions
from app.exceptions import ExceptionHandling
from app.models.clients import ClientUserModelDB

class SortOrder(str, Enum):
	ASC = "ASC"
	DESC = "DESC"

	def __str__(self):
		return self.value

def default_query_params(
		order_by: Optional[str] = "time_created",
		sort: SortOrder = Query(default = SortOrder.DESC)
	):
	return {
		"order_by": order_by,
		"sort": str(sort)
	}


async def verify_client_user(user_uuid: str, client_uuid: str):
	user = await BaseActions.check_if_exists(
		ClientUserModelDB,
		[
			ClientUserModelDB.user_uuid == user_uuid,
			ClientUserModelDB.client_uuid == client_uuid
		]
	)
	await ExceptionHandling.check404(
		user,
		message="The provided user_uuid is not related to the current client"
	)
