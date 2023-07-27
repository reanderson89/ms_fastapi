from time import time
from sqlalchemy import select
from fastapi import APIRouter, Query, Depends
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.segments import SegmentRuleModel, SegmentRuleUpdate
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}",
    tags=["Client Program Segment Rules"]
)

def get_session():
    with Session(engine) as session:
        yield session


@router.get("/rules", response_model=list[SegmentRuleModel])
async def get_rules(
    client_uuid: str,
    program_9char: str,
    segment_9char: str,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: Session = Depends(get_session)
):
    rules = session.scalars(
        select(SegmentRuleModel)
        .where(
            SegmentRuleModel.client_uuid == client_uuid,
            SegmentRuleModel.program_9char == program_9char,
            SegmentRuleModel.segment_9char == segment_9char
        )
        .offset(offset)
        .limit(limit)
        ).all()
    await ExceptionHandling.check404(rules)
    return rules


@router.get("/rules/{rule_9char}", response_model=SegmentRuleModel)
async def get_rule(
    client_uuid: str,
    program_9char: str,
    segment_9char: str,
    rule_9char: str,
    session: Session = Depends(get_session)
):
    rule = session.scalars(
        select(SegmentRuleModel)
        .where(
            SegmentRuleModel.rule_9char == rule_9char,
            SegmentRuleModel.client_uuid == client_uuid,
            SegmentRuleModel.program_9char == program_9char,
            SegmentRuleModel.segment_9char == segment_9char
        )
    ).one_or_none()
    await ExceptionHandling.check404(rule)
    return rule


@router.post("/rules", response_model=(list[SegmentRuleModel] | SegmentRuleModel))
async def create_rule(rules: (list[SegmentRuleModel] | SegmentRuleModel)):
    return await CommonRoutes.create_one_or_many(rules)


@router.put("/rules/{rule_9char}", response_model=SegmentRuleModel)
async def update_rule(
    client_uuid: str,
    program_9char: str,
    segment_9char: str,
    rule_9char: str,
    rule_updates: SegmentRuleUpdate,
    session: Session = Depends(get_session)
):
    rule = session.scalars(
        select(SegmentRuleModel)
        .where(
            SegmentRuleModel.rule_9char == rule_9char,
            SegmentRuleModel.client_uuid == client_uuid,
            SegmentRuleModel.program_9char == program_9char,
            SegmentRuleModel.segment_9char == segment_9char
        )
    ).one_or_none()
    await ExceptionHandling.check404(rule)
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
    rule = session.scalars(
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
