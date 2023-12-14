import os
import jwt
import subprocess
from datetime import datetime
from pydantic.datetime_parse import timedelta
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file


SECRET_KEY = os.environ['SECRET_KEY']
RAILS_JWT_SECRET_KEY = os.environ['RAILS_JWT_SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def create_access_token(data: dict, expires_delta: timedelta | None = None, cron_job: bool = False):
    secret_key = RAILS_JWT_SECRET_KEY if cron_job else SECRET_KEY
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def access_token_creation(redeem, cron_job: bool = False):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=redeem, expires_delta=access_token_expires, cron_job=cron_job
    )
    return {"access_token": access_token, "token_type": "Bearer"}

data = {
  "exp": 1702755196,
  "company_gid": "04daa65d-3a89-4242-b38a-e4d6273019c1",
  "sub": "a837d688-fb9a-4622-af07-d37c9b64bb02",
  "scp": "account",
  "aud": None,
  "iat": 1702495996,
  "jti": "b7778065-625e-4b75-a5d7-33a0aa53147b"
}

token = access_token_creation(data, True)
process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE)
process.communicate(token['access_token'].encode('utf-8'))