from faker import Faker
from faker.providers import job
from app.actions.clients.user import ClientUserActions

Faker.seed(0)
faker = Faker()
faker.add_provider(job)

client_user_uuid_list = [
    "6fc9d027ad6f35f658061a8e26f039c66ce36dbe125507862e70faca",
    "93d1735b39e0f4993c247c2bc8bd38be10c96e77164f0a14b4ba2926",
    "f2123ec36883c78af910d1b327626450ec3b8e9ccba08060d27bca83",
    "9b5fcd41e014bfd1b5fca60eb83675e5db03a40645defd90523c69ae",
    "3c89f06811025dcf7cc4fb0df6b6d1bdc3c818c0ee905a7925cf8ca3",
    "6455036f85c37f9bcf00c035046eecfb4cfe23f3e1523983c5a5e6cc",
    "4a805c077482484f691fd39001b26c3e3a7a8cb21f78a91ac9773713",
    "a72fe5907159394307a5761c81ce811c32ecd87361ce59d029b5be88",
    "5024d5d357a3cae1409378db354f23f9d848fcb5c540d963eaa9f925",
    "78776866b6e91c6f2682bfd7cbaedbb77e1b71ad0d4f6da197034b56",
    "f102bce8a755128a4e115e02b3fe403489de5f82b00199df9799cb60",
    "e9ae6f6140de804bd55ab663c3ddfcfa35a1cb39d8879e6e2d4a409a",
    "e2ee5a3c13e9471c91a30041d4310892c3a708311954eb3c9efe97bd",
    "d71a40ac7b6a6b5fc4a9bfcfed5313980be23cd64447310a2e585521",
    "280d9bd08e72e86464cb292366431a5ac72d1e4a31d745d419c63639",
    "96008330312c6c599956e2d5e09d85639dd27946d5e31507c43646be",
    "4cc981e6878bc77d80f749aad655c45338411e9af8791b1465de1f9a",
    "ccb755a6cd5216438198d552f5328c049d91a83247fed26c20833367",
    "694712a1bd35f3fee697633ef8b60c86609460562e3fca5d0877eaf4",
    "e61cbd1104125f9ee32ab94024f9d78e481f17a7bdd3224aa0997367",
    "d1135b265c841b92162c4d86cbbd95f810c5a307ba4b0cc068453519",
    "22433b620957ee2b4652d92d2cc511587fafd4a821b8f76f26f8df8a",
    "6f6bc47a19f429053c6ee09b1c8c6f335d2d4dac32b9ff57f24beb65",
    "87b31cadc4b2af88469623e44a5492764ba5bd2284ecb31a37255555",
    "a80d021e2799e74445b8cbbdf823a868864e84ba093739045df009bf",
    "c8b9eb48e50596bd42d44d033c2aaab8a2166303559cef24c0972b77",
    "3017b8f4f916671f58a21a9e2fc7ce044bf0330b0c53e041c7992e15",
    "a5e87492da5368ac84bcd6c109a9505b11d6373e199d314378a38530",
    "168bd56b6a3393776cff9f08d7f9eb7e343363e88a202dcc3c9919e3",
    "f1df59c44b05847edba036c35d2ea0bd03f8117a0526ffa0bf6d6a61",
    "9ce30a17a859e6eedb22e0a2079590651aba289540e83508379ba3c8",
    "6f5072d4acc3bce3091b6949d868bfc48ed7fcd31fba31161f135eaa",
    "8b0f95083cf1b337e5df56d17dc15e262006b09eb07ea33c0ba166de",
    "ceaf6122a6ee7edb5efca3ee8d967a8382b39741f6c6e5a7f330c5c5",
    "00cb730bc7c27509b1049558e3161a8db8c1da26bbd65f6337c3fb62",
    "af0ba0daa20ed55306d1efce9b89c9d5a08f03073956fed053aa01e9",
    "89e5fe792bbffe1d3371425e363d71c7ee6bcfd6bb4e1c9f7eb337a8",
    "99c6154806296ec02ca498cd1687551dd2680045c1e80125b73aacd6",
    "ea52727da25ba5a81d65e04131ff45d485aaee014c78f59c12002135",
    "8e6021e1a9cdae4f545f00a9eec9ba5337a32962533407a8a7c7391a",
    "c81f8c1ac3156631213334761bc08bb591bf42286959a6c8f46f5b89",
    "439646f273d68c79aedb2f2229dee402a074b86dd5c806fdd89eb50c",
    "ef338ac0a6b87e4e92ca93eee8bd6248386a726ae2cc6a7d62538a30",
    "cd4d766bf81f84d100e8b20de360c8d8906bd3b0481c9dec22e1660c",
    "0c18435d295203d41a3cf058185cf42f250f03708bce2864ab2568a6",
    "c6d5b94710218d9f35f5e1188580fbaf71f6e45e4176b59be96b6a60",
    "682251a185445dd47bdc1538a2e19aaefdea8053d5469decf47ce375",
    "58b12d950c4a6cd9c51ecc0c3d6b28279b8044406f5d075f6cdcbc15",
    "66fa2354b6210a85a439f7d0196193198816e9bc80ca707b9bbbad44",
    "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
]


owen = {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "owen.plambeck@blueboard.com",
        "first_name": "Owen",
        "last_name": "Plambeck",
        "title": "Sr Bug Creator",
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "department": f"{faker.job()} Department",
        "admin": 2,
        "time_start": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "time_hire": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp())}

clark = {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "clark.ritchie@blueboard.com",
        "first_name": "Clark",
        "last_name": "Ritchie",
        "title": "Domestique",
        "department": f"{faker.job()} Department", #faker doesnt have a job department field
        "admin": 2,
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "time_start": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "time_hire": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp()) #we dont ask for birthday during client user creation
    }

ryan = {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "ryan.green@blueboard.com",
        "first_name": "Ryan",
        "last_name": "Green",
        "title": "Sr Software Engineer",
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "department": f"{faker.job()} Department", #faker doesnt have a job department field
        "admin": 2,
        "time_start": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "time_hire": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp()) #we dont ask for birthday during client user creation
    }

jason = {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "jason@blueboard.com",
        "first_name": "Jason",
        "last_name": "Wiener",
        "title": "Quality Assurance Intern",
        "department": f"{faker.job()} Department", #faker doesnt have a job department field
        "admin": 2,
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "time_start": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "time_hire": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp()) #we dont ask for birthday during client user creation
        }

josh = {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "joshua.crowley@blueboard.com",
        "first_name": "Josh",
        "last_name": "Crowley",
        "title": "Software Engineer",
        "department": f"{faker.job()} Department", #faker doesnt have a job department field
        "admin": 2,
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "time_start": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "time_hire": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp()) #we dont ask for birthday during client user creation
    }

dan = {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "daniel@nscale.io",
        "first_name": "Daniel",
        "last_name": "O'Niell",
        "title": "Frontend",
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "department": f"{faker.job()} Department",
        "admin": 2,
        "time_start": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "time_hire": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp())}

mike = {
        "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        "work_email": "michael@nscale.io",
        "first_name": "Michael",
        "last_name": "Lindenau",
        "title": "Frontend",
        "manager_uuid": "06ad1e1f05a61ab1ac423d5a6fb969193305145100c888a069eaacbf",
        "department": f"{faker.job()} Department",
        "admin": 2,
        "time_start": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "time_hire": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
        "active": 1,
        "employee_id": faker.pystr(),
        "time_birthday": int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp())}

new = [owen, jason, josh, ryan, clark, mike, dan]

async def generate_client_users(clients: list):
    for client in clients:
        if client.name != "Blueboard":
            for i in range(0, 5):
                if i == 0:
                    uuid = client_user_uuid_list.pop()
                    manager_uuid = uuid
                await ClientUserActions.create_client_user(
                    {
                        "uuid": uuid,
                        "client_uuid": client.uuid,
                        "work_email": f"faker_test_email+{faker.email()}",
                        "first_name": faker.first_name(),
                        "last_name": faker.last_name(),
                        "title": faker.job(),
                        "department": f"{faker.job()} Department", #faker doesnt have a job department field
                        "manager_uuid": manager_uuid,
                        "admin": 1,
                        "time_start": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
                        "time_hire": int(faker.date_time_between(start_date="-1y", end_date="now").timestamp()),
                        "active": 1,
                        "employee_id": faker.pystr(),
                        "time_birthday": int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp()), #we dont ask for birthday during client user creation
                    },
                    {"client_uuid": client.uuid, "user_uuid": None}
                )
    for i in new:
        await ClientUserActions.create_client_user(i, {
           "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
        })
