from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.segments.rules import SegmentRuleModel, SegmentRuleUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["segment rules"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/rules", response_model=List[SegmentRuleModel])
async def get_rules(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(CommonRoutes)
):
	rules = session.exec(
		select(SegmentRuleModel).where(
			SegmentRuleModel.client_uuid == client_uuid,
			SegmentRuleModel.program_9char == program_9char,
			SegmentRuleModel.segment_9char == segment_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(rules)
	return rules

@router.get("/rules/{rule_9char}", response_model=SegmentRuleModel)
async def get_rule(rule_9char: str):
	return CommonRoutes.get_one(SegmentRuleModel, rule_9char)

@router.post("/rules", response_model=SegmentRuleModel)
async def create_rule(rules: (SegmentRuleModel | List[SegmentRuleModel])):
	return CommonRoutes.create_one_or_many(rules)

@router.put("/rules/{rule_9char}", response_model=SegmentRuleModel)
async def update_rule(rule_9char: str, rule_updates: SegmentRuleUpdate):
	return CommonRoutes.update_one(rule_9char, SegmentRuleModel, rule_updates)

@router.delete("/rules/{rule_9char}")
async def delete_rule(rule_9char: str):
	return CommonRoutes.delete_one(rule_9char, SegmentRuleModel)
