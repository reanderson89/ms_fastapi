from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.segments import SegmentRuleModel, SegmentRuleUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["Client Program Segment Rules"])

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
	session: Session = Depends(get_session)
):
	rules = session.exec(
		select(SegmentRuleModel)
		.where(
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
async def get_rule(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	rule_9char: str,
	session: Session = Depends(get_session)
):
	rule = session.exec(
		select(SegmentRuleModel)
		.where(
			SegmentRuleModel.rule_9char == rule_9char,
			SegmentRuleModel.client_uuid == client_uuid,
			SegmentRuleModel.program_9char == program_9char,
			SegmentRuleModel.segment_9char == segment_9char
		)
	).one_or_none()
	ExceptionHandling.check404(rule)
	return rule

@router.post("/rules", response_model=(List[SegmentRuleModel] | SegmentRuleModel))
async def create_rule(rules: (List[SegmentRuleModel] | SegmentRuleModel)):
	return CommonRoutes.create_one_or_many(rules)

@router.put("/rules/{rule_9char}", response_model=SegmentRuleModel)
async def update_rule(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	rule_9char: str,
	rule_updates: SegmentRuleUpdate,
	session: Session = Depends(get_session)
):
	rule = session.exec(
		select(SegmentRuleModel)
		.where(
			SegmentRuleModel.rule_9char == rule_9char,
			SegmentRuleModel.client_uuid == client_uuid,
			SegmentRuleModel.program_9char == program_9char,
			SegmentRuleModel.segment_9char == segment_9char
		)
	).one_or_none()
	ExceptionHandling.check404(rule)
	update_rule = rule_updates.dict(exclude_unset=True)
	for k, v in update_rule.items():
		setattr(rule, k, v)
	rule.time_updated = int(time())
	session.add(rule)
	session.commit()
	session.refresh(rule)
	return rule

@router.delete("/rules/{rule_9char}")
async def delete_rule(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	rule_9char: str,
	session: Session = Depends(get_session)
):
	rule = session.exec(
		select(SegmentRuleModel)
		.where(
			SegmentRuleModel.rule_9char == rule_9char,
			SegmentRuleModel.client_uuid == client_uuid,
			SegmentRuleModel.program_9char == program_9char,
			SegmentRuleModel.segment_9char == segment_9char
		)
	).one_or_none()
	session.delete(rule)
	session.commit()
	return {"ok": True, "Deleted": rule}
