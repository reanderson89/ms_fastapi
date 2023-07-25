from fastapi import APIRouter

from app.actions.cron.cron_actions import CronActions



router = APIRouter()


@router.get("/cron", response_model_by_alias=True)
async def cron_kickoff():
    results = await CronActions.kick_off()
    return results
