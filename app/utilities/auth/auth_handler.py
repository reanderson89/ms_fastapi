from typing import Optional
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
import os
from pydantic import BaseModel

get_bearer_token = HTTPBearer(auto_error=False)

valid_tokens = set([os.getenv("BEARER_TOKEN")])

class UnAuthedMessage(BaseModel):
    detail: str = "Bearer token missing or unknown"

async def get_token(
        auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)
) -> str:
    pass
   # if auth is None or (token := auth.credentials) not in valid_tokens:
    #    raise HTTPException(
     #       status_code = status.HTTP_401_UNAUTHORIZED,
      #      detail = UnAuthedMessage().detail
      #  )
   # return token
