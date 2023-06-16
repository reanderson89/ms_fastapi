from enum import Enum
from typing import Optional
from fastapi import Query


class SortOrder(str, Enum):
	ASC = "ASC"
	DESC = "DESC"

	def __str__(self):
		return self.value


def get_query_params(
		offset: int = Query(default=0, ge=0),
		limit: int = Query(default=25, lte=100),
		order_by: Optional[str] = None,
		sort: SortOrder = Query(default = SortOrder.DESC)
	):
	return {
		"offset": offset,
		"limit": limit,
		"order_by": order_by,
		"sort": str(sort)
	}
