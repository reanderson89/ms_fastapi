import pytest
from app.models.award import AwardModel

@pytest.mark.asyncio

async def get_all():


async def get_all():
    response = await BaseActions.get_all(
        AwardModel
    )
    print(response)
    print('')

    response = await BaseActions.get_all(
        AwardModel,
        'time_created',
        'DESC'
    )
    print(response)
    print('')

    response = await BaseActions.get_all(
        AwardModel,
        'time_created',
    )
    print(response)
    print('')

    response = await BaseActions.get_all(
        AwardModel,
        'time_created',
        'ASC'
    )
    print(response)
