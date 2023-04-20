from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from src.database.config import engine
from src.api import CommonRoutes, ExceptionHandling
from .segment_models import ProgramSegmentModel, SegmentUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["program segments"])

async def get_session():
	async with Session(engine) as session:
		yield session

@router.get("/segments", response_model=List[ProgramSegmentModel])
async def get_segments(
	client_uuid: str,
	program_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	segments = session.exec(
		select(ProgramSegmentModel).where(
			ProgramSegmentModel.client_uuid == client_uuid,
			ProgramSegmentModel.program_9char == program_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(segments)
	return segments

@router.get("/segments/{segment_9char}", response_model=ProgramSegmentModel)
async def get_segment(segment_9char: str):
	return CommonRoutes.get_one(ProgramSegmentModel, segment_9char)

@router.post("/segments", response_model=ProgramSegmentModel)
async def create_segment(segment: (ProgramSegmentModel | List[ProgramSegmentModel])):
	return CommonRoutes.create_one_or_many(segment)

@router.put("/segments/{segment_9char}", response_model=ProgramSegmentModel)
async def update_segment(segment_9char: str, segment_updates: SegmentUpdate):
	return CommonRoutes.update_one(segment_9char, ProgramSegmentModel, segment_updates)

@router.delete("/segments/{segment_9char}")
async def delete_segment(segment_9char: str):
	return CommonRoutes.delete_one(segment_9char, ProgramSegmentModel)
