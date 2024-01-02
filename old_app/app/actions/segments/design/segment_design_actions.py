from burp.utils.base_crud import BaseCRUD
from burp.utils.helper_actions import HelperActions
from burp.models.segment_design import SegmentDesignModelDB
from burp.models.program import ProgramModelDB
from app.exceptions import ExceptionHandling

class SegmentDesignActions:

    @staticmethod
    async def get_program_uuid(program_9char: str):
        program = await BaseCRUD.get_one_where(
            ProgramModelDB.uuid,
            [ProgramModelDB.program_9char == program_9char]
        )
        await ExceptionHandling.check404(program)

        return program

    @staticmethod
    async def get_all_segment_designs(path_params, query_params):
        return await BaseCRUD.get_all_where(
            SegmentDesignModelDB,
            [
                SegmentDesignModelDB.client_uuid == path_params["client_uuid"],
                SegmentDesignModelDB.program_9char == path_params["program_9char"],
                SegmentDesignModelDB.segment_9char == path_params["segment_9char"]
            ],
            query_params
        )

    @staticmethod
    async def get_segment_design(path_params):
        return await BaseCRUD.get_one_where(
            SegmentDesignModelDB,
            [
                SegmentDesignModelDB.design_9char == path_params["design_9char"],
                SegmentDesignModelDB.client_uuid == path_params["client_uuid"],
                SegmentDesignModelDB.program_9char == path_params["program_9char"],
                SegmentDesignModelDB.segment_9char == path_params["segment_9char"]
            ]
        )

    @staticmethod
    async def create_designs(designs, path_params, program_uuid):
        if isinstance(designs, list):
            designs = [SegmentDesignModelDB(
                **design.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                program_uuid = program_uuid,
                design_9char = await HelperActions.generate_9char()
            ) for design in designs]
            return await BaseCRUD.create(designs)
        designs = SegmentDesignModelDB(
            **designs.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                program_uuid = program_uuid,
                design_9char = await HelperActions.generate_9char()
        )
        return await BaseCRUD.create(designs)

    @staticmethod
    async def update_design(design_updates, path_params):
        return await BaseCRUD.update(
            SegmentDesignModelDB,
            [
                SegmentDesignModelDB.design_9char == path_params["design_9char"],
                SegmentDesignModelDB.client_uuid == path_params["client_uuid"],
                SegmentDesignModelDB.program_9char == path_params["program_9char"],
                SegmentDesignModelDB.segment_9char == path_params["segment_9char"]
            ],
            design_updates
        )

    @staticmethod
    async def delete_design(path_params):
        return await BaseCRUD.delete_one(
            SegmentDesignModelDB,
            [
                SegmentDesignModelDB.design_9char == path_params["design_9char"],
                SegmentDesignModelDB.client_uuid == path_params["client_uuid"],
                SegmentDesignModelDB.program_9char == path_params["program_9char"],
                SegmentDesignModelDB.segment_9char == path_params["segment_9char"]
            ]
        )
