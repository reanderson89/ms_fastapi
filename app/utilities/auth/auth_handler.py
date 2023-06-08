from datetime import datetime
from typing import Optional
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException
from pydantic.datetime_parse import timedelta
from starlette import status
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
import os
from pydantic import BaseModel


get_bearer_token = HTTPBearer(auto_error=False)
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = 300


class UnAuthedMessage(BaseModel):
    detail: str = "Bearer token missing or unknown"


def check_token(credentials):
    try:
        verify = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if verify:
            return True
        else:
            return False
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnAuthedMessage().detail
        )


async def get_token(
        auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)
) -> str:
    if auth is None or not check_token(auth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnAuthedMessage().detail
        )
    return auth.credentials


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def access_token_creation(redeem):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=redeem, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

