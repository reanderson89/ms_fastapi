from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.segments import SegmentDesignModel, SegmentDesignUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["Client Program Segment Designs"])

def get_session():
	with Session(engine) as session:
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
	await ExceptionHandling.check404(designs)
	return designs

@router.get("/designs/{design_9char}", response_model=SegmentDesignModel)
async def get_design(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	design_9char: str,
	session: Session = Depends(get_session)
):
	design = session.exec(
		select(SegmentDesignModel)
		.where(
			SegmentDesignModel.design_9char == design_9char,
			SegmentDesignModel.client_uuid == client_uuid,
			SegmentDesignModel.program_9char == program_9char,
			SegmentDesignModel.segment_9char == segment_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(design)
	return design

@router.post("/designs", response_model=(List[SegmentDesignModel] | SegmentDesignModel))
async def create_design(designs: (List[SegmentDesignModel] | SegmentDesignModel)):
	return await CommonRoutes.create_one_or_many(designs)

@router.put("/designs/{design_9char}", response_model=SegmentDesignModel)
async def update_design(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	design_9char: str,
	design_updates: SegmentDesignUpdate,
	session: Session = Depends(get_session)
):
	design = session.exec(
		select(SegmentDesignModel)
		.where(
			SegmentDesignModel.design_9char == design_9char,
			SegmentDesignModel.client_uuid == client_uuid,
			SegmentDesignModel.program_9char == program_9char,
			SegmentDesignModel.segment_9char == segment_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(design)
	update_design = design_updates.dict(exclude_unset=True)
	for k, v in update_design.items():
		setattr(design, k, v)
	design.time_updated = int(time())
	session.add(design)
	session.commit()
	session.refresh(design)
	return design

@router.delete("/designs/{design_9char}")
async def delete_design(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	design_9char: str,
	session: Session = Depends(get_session)
):
	design = session.exec(
		select(SegmentDesignModel)
		.where(
			SegmentDesignModel.design_9char == design_9char,
			SegmentDesignModel.client_uuid == client_uuid,
			SegmentDesignModel.program_9char == program_9char,
			SegmentDesignModel.segment_9char == segment_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(design)
	session.delete(design)
	session.commit()
	return {"ok": True, "Deleted": design}
