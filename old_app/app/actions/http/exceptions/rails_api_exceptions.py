from fastapi import HTTPException


class Exceptions:
    @staticmethod
    async def rails_api500(message):
        raise HTTPException(status_code=500, detail=f"RAILS API ERROR: {message}")

    @staticmethod
    async def rails_api401(message):
        raise HTTPException(status_code=401, detail=f"RAILS API UNAUTHORIZED: {message}")
