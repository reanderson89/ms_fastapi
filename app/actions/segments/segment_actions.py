from burp.utils.base_crud import BaseCRUD
from burp.utils.helper_actions import HelperActions
from burp.models.segment import SegmentModelDB

class SegmentActions:

    @staticmethod
    async def get_all_segments(path_params, query_params):
        return await BaseCRUD.get_all_where(
            SegmentModelDB,
            [
            SegmentModelDB.client_uuid == path_params["client_uuid"],
            SegmentModelDB.program_9char == path_params["program_9char"]
            ],
            query_params
        )

    @staticmethod
    async def get_segment(path_params):
        return await BaseCRUD.get_one_where(
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
            to_create = []
            return_list = []
            segments_models = [SegmentModelDB(
                **segment.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = await HelperActions.generate_9char()
            ) for segment in segments]
            for segment in segments_models:
                existing_segment = await SegmentActions.check_if_segment_exists(path_params, segment)
                if existing_segment:
                    return_list.append(existing_segment)
                else:
                    to_create.append(segment)
            if to_create:
                return_list.extend(await BaseCRUD.create(to_create))
            return return_list
        else:
            segment_model = SegmentModelDB(
                **segments.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = await HelperActions.generate_9char()
            )
            existing_segment = await SegmentActions.check_if_segment_exists(path_params, segment_model)
            if existing_segment:
                return existing_segment
            return await BaseCRUD.create(segment_model)

    @staticmethod
    async def update_segment(path_params, segment_updates):
        return await BaseCRUD.update(
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
        return await BaseCRUD.delete_one(
            SegmentModelDB,
            [
            SegmentModelDB.segment_9char == path_params["segment_9char"],
            SegmentModelDB.client_uuid == path_params["client_uuid"],
            SegmentModelDB.program_9char == path_params["program_9char"]
            ]
        )

    @staticmethod
    async def check_if_segment_exists(path_params, segment):
        return await BaseCRUD.check_if_exists(
            SegmentModelDB,
            [
                SegmentModelDB.segment_9char == segment.name,
                SegmentModelDB.client_uuid == path_params['client_uuid'],
                SegmentModelDB.program_9char == path_params['program_9char']
            ]
        )
