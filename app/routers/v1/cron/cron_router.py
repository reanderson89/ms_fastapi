from fastapi import APIRouter, Depends

from app.actions.cron.cron_actions import CronActions

from app.routers.v1.dependencies import default_query_params


router = APIRouter()


@router.get("/cron/", response_model_by_alias=True)
async def cron_kickoff(
    query_params: dict = Depends(default_query_params)
):
    results = await CronActions.kick_off(query_params)
    return results
