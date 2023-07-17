from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.segments.segment_award_models import SegmentAward

class SegmentAwardActions():

	@staticmethod
	async def get_all_segment_awards(path_params, query_params):
		return await BaseActions.get_all_where(
			SegmentAward,
			[
			SegmentAward.client_uuid == path_params["client_uuid"],
			SegmentAward.program_9char == path_params["program_9char"],
			SegmentAward.segment_9char == path_params["segment_9char"]
			],
			query_params
		)
	
	@staticmethod
	async def get_segment_award(path_params):
		return await BaseActions.get_one_where(
			SegmentAward,
			[
			SegmentAward.segment_9char == path_params["segment_9char"],
			SegmentAward.client_uuid == path_params["client_uuid"],
			SegmentAward.program_9char == path_params["program_9char"],
			SegmentAward.segment_award_9char == path_params["segment_award_9char"]
			]
		)
	
	@staticmethod
	async def create_segment_award(segment_awards, path_params,  program_award_9char):
		if isinstance(segment_awards, list):
			segment_awards = [SegmentAward(
				**segment_award.dict(),
				client_uuid = path_params["client_uuid"],
				program_9char = path_params["program_9char"],
				segment_9char = path_params["segment_9char"],
				program_award_9char = program_award_9char,
			) for segment_award in segment_awards]
			return await BaseActions.create(segment_awards)
		segment_awards = SegmentAward(
			**segment_awards.dict(),
				client_uuid = path_params["client_uuid"],
				program_9char = path_params["program_9char"],
				segment_9char = path_params["segment_9char"],
				program_award_9char = program_award_9char,
		)
		return await BaseActions.create(segment_awards)
	
	@staticmethod
	async def update_segment_award(path_params, segment_award_updates):
		return await BaseActions.update(
			SegmentAward,
			[
			SegmentAward.segment_9char == path_params["segment_9char"],
			SegmentAward.client_uuid == path_params["client_uuid"],
			SegmentAward.program_9char == path_params["program_9char"],
			SegmentAward.segment_award_9char == path_params["segment_award_9char"]
			],
			segment_award_updates
		)
	
	@staticmethod
	async def delete_segment_award(path_params):
		return await BaseActions.delete_one(
			SegmentAward,
			[
			SegmentAward.segment_9char == path_params["segment_9char"],
			SegmentAward.client_uuid == path_params["client_uuid"],
			SegmentAward.program_9char == path_params["program_9char"],
			SegmentAward.segment_award_9char == path_params["segment_award_9char"]
			]
		)
	
