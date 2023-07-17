from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.segments.segment_design_models import SegmentDesignModel

class SegmentDesignActions():

    @staticmethod
    async def get_all_segment_designs(path_params, query_params):
        return await BaseActions.get_all_where(
            SegmentDesignModel,
            [
                SegmentDesignModel.client_uuid == path_params['client_uuid'],
                SegmentDesignModel.program_9char == path_params['program_9char'],
                SegmentDesignModel.segment_9char == path_params['segment_9char']
            ],
            query_params
        )
    
    @staticmethod
    async def get_segment_design(path_params):
        return await BaseActions.get_one_where(
            SegmentDesignModel,
            [
                SegmentDesignModel.design_9char == path_params['design_9char'],
                SegmentDesignModel.client_uuid == path_params['client_uuid'],
                SegmentDesignModel.program_9char == path_params['program_9char'],
                SegmentDesignModel.segment_9char == path_params['segment_9char']
            ]
        )
    
    @staticmethod
    async def create_designs(designs, path_params):
        if isinstance(designs, list):
            designs = [SegmentDesignModel(
                **design.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                design_9char = await HelperActions.generate_9char()
            ) for design in designs]
            return await BaseActions.create(designs)
        designs = SegmentDesignModel(
            **designs.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                design_9char = await HelperActions.generate_9char()
        )
        return await BaseActions.create(designs)
    
    @staticmethod
    async def update_design(design_updates, path_params):
        return await BaseActions.update(
            SegmentDesignModel,
            [
                SegmentDesignModel.design_9char == path_params['design_9char'],
                SegmentDesignModel.client_uuid == path_params['client_uuid'],
                SegmentDesignModel.program_9char == path_params['program_9char'],
                SegmentDesignModel.segment_9char == path_params['segment_9char']
            ],
            design_updates
        )

    @staticmethod
    async def delete_design(path_params):
        return await BaseActions.delete_one(
            SegmentDesignModel,
            [
                SegmentDesignModel.design_9char == path_params['design_9char'],
                SegmentDesignModel.client_uuid == path_params['client_uuid'],
                SegmentDesignModel.program_9char == path_params['program_9char'],
                SegmentDesignModel.segment_9char == path_params['segment_9char']
            ]
        )