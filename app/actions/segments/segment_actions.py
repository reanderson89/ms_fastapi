from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.segments.segment_models import SegmentModelDB

class SegmentActions:

    @staticmethod
    async def get_all_segments(path_params, query_params):
        return await BaseActions.get_all_where(
            SegmentModelDB,
            [
            SegmentModelDB.client_uuid == path_params["client_uuid"],
            SegmentModelDB.program_9char == path_params["program_9char"]
            ],
            query_params
        )

    @staticmethod
    async def get_segment(path_params):
        return await BaseActions.get_one_where(
            SegmentModelDB,
            [
            SegmentModelDB.segment_9char == path_params["segment_9char"],
            SegmentModelDB.client_uuid == path_params["client_uuid"],
            SegmentModelDB.program_9char == path_params["program_9char"]
            ]
        )

    @staticmethod
    async def create_segment(segments, path_params):
        if isinstance(segments, list):
            segments = [SegmentModelDB(
                **segment.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = await HelperActions.generate_9char()
            ) for segment in segments]
            return await BaseActions.create(segments)
        segments = SegmentModelDB(
            **segments.dict(),
            client_uuid = path_params["client_uuid"],
            program_9char = path_params["program_9char"],
            segment_9char = await HelperActions.generate_9char()
        )
        return await BaseActions.create(segments)

    @staticmethod
    async def update_segment(path_params, segment_updates):
        return await BaseActions.update(
            SegmentModelDB,
            [
            SegmentModelDB.segment_9char == path_params["segment_9char"],
            SegmentModelDB.client_uuid == path_params["client_uuid"],
            SegmentModelDB.program_9char == path_params["program_9char"]
            ],
            segment_updates
        )

    @staticmethod
    async def delete_segment(path_params):
        return await BaseActions.delete_one(
            SegmentModelDB,
            [
            SegmentModelDB.segment_9char == path_params["segment_9char"],
            SegmentModelDB.client_uuid == path_params["client_uuid"],
            SegmentModelDB.program_9char == path_params["program_9char"]
            ]
        )

