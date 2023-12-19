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
  "company_gid": "6cdcf917-a0da-4445-93ec-d51d662c60c6",
  "sub": "dd3085e2-a6bd-4339-a7bb-9d06c0132c34",
  "scp": "account",
  "aud": None,
  "jti": "6f3d0081-0f73-473c-b1ad-c6165661d969"
}

token = access_token_creation(data, True)
process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE)
process.communicate(token['access_token'].encode('utf-8'))