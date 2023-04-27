from typing import Optional
from fastapi import Depends, HTTPException
from sqlmodel import SQLModel
from starlette import status
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

get_bearer_token = HTTPBearer(auto_error=False)

valid_tokens = set(["4c402a7d-83ea-472f-8670-a31750fa2ab2"])

class UnAuthedMessage(SQLModel, table=False):
    detail: str = "Bearer token missing or unknown"

async def get_token(
        auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)
) -> str:
    if auth is None or (token := auth.credentials) not in valid_tokens:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = UnAuthedMessage().detail
        )
    return token
