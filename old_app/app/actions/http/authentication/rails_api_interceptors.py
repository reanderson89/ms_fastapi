from burp.utils.auth_utils import access_token_creation

TOKEN_DATA = {
    "company_gid": "6cdcf917-a0da-4445-93ec-d51d662c60c6",
    "sub": "dd3085e2-a6bd-4339-a7bb-9d06c0132c34",
    "scp": "account",
    "aud": None,
    "jti": "6f3d0081-0f73-473c-b1ad-c6165661d969"
}


def rails_auth(execute):
    async def interceptor(*args, **kwargs):
        jwt = await access_token_creation(TOKEN_DATA, True)
        headers = {
            "Cookie": f"stagingJwtToken={jwt['access_token']}"
        }

        execute(headers=headers, *args, **kwargs)

    return interceptor
