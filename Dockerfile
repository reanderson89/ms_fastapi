FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS builder

WORKDIR /app

RUN apt-get update
RUN apt -y install iputils-ping lsof vim
RUN apt -y install default-mysql-client python3-pymysql alembic

# install dependencies first so that changes in application code do not invalidate
# the cache of the layer with installed dependencies
COPY requirements.txt ./
# when pip install is here, docker caches all the pip dependencies
RUN pip install -r requirements.txt

# next, copy everything else
# TODO tighten this up
COPY . .

# for initialization sequences and Gunicorn/uvicorn configs, see the docs: https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
# in particular, note:
# - pre-start.sh
# - start.sh
# - start-reload.sh
# Docker's default entrypoint (if not specified in the Dockerfile) is start.sh
RUN chmod +x prestart.sh