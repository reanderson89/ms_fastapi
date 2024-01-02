import pytest
from burp.models.award import AwardModelDB
from burp.utils.base_crud import BaseCRUD

@pytest.mark.asyncio


async def get_all():
    response = await BaseCRUD.get_all(
        AwardModelDB
    )
    print(response)
    print('')

    response = await BaseCRUD.get_all(
        AwardModelDB,
        'time_created',
        'DESC'
    )
    print(response)
    print('')

    response = await BaseCRUD.get_all(
        AwardModelDB,
        'time_created',
    )
    print(response)
    print('')

    response = await BaseCRUD.get_all(
        AwardModelDB,
        'time_created',
        'ASC'
    )
    print(response)
