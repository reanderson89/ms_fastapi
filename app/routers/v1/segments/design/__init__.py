from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.segments.design import SegmentDesignModel, SegmentDesignUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["segment designs"])

async def get_session():
	async with Session(engine) as session:
		yield session

@router.get("/designs", response_model=List[SegmentDesignModel])
async def get_designs(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	designs = session.exec(
		select(SegmentDesignModel).where(
			SegmentDesignModel.client_uuid == client_uuid,
			SegmentDesignModel.program_9char == program_9char,
			SegmentDesignModel.segment_9char == segment_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(designs)
	return designs

@router.get("/designs/{design_9char}", response_model=SegmentDesignModel)
async def get_design(design_9char: str):
	return CommonRoutes.get_one(SegmentDesignModel, design_9char)

@router.post("/designs", response_model=SegmentDesignModel)
async def create_design(designs: (SegmentDesignModel | List[SegmentDesignModel])):
	return CommonRoutes.create_one_or_many(designs)

@router.put("/designs/{design_9char}", response_model=SegmentDesignModel)
async def update_design(design_9char: str, design_updates: SegmentDesignUpdate):
	return CommonRoutes.update_one(design_9char, SegmentDesignModel, design_updates)

@router.delete("/designs/{design_9char}")
async def delete_design(design_9char: str):
	return CommonRoutes.delete_one(design_9char, SegmentDesignModel)