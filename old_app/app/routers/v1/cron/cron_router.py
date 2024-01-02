from fastapi import APIRouter, Depends
from app.actions.cron.cron_actions import CronActions

router = APIRouter(tags=["Cron Jobs"])


# This route is currently being pinged every minute by a cron job. You can stop this by opening the "crontab" file in the "Docker" folder and commenting out the active job. You will then have to re-build the container.
@router.get("/cron/rewards/send")
async def send_rewards(
    authenticate: bool = Depends(CronActions.authenticate)
):
    if authenticate:
        await CronActions.send_rewards()
        return {"message": "Great Success!"}


# @router.get("/cron", response_model_by_alias=True)
# async def cron_kickoff():
#     results = await CronActions.kick_off()
#     return results
