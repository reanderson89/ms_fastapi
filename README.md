# Milestones API

<div align="center">
  <!-- <a href="https://github.com/blueboard/milestones_api/actions/workflows/tbd-v0.yml"><img src="https://github.com/blueboard/milestones_api/actions/workflows/tbd-v0.yml/badge.svg?branch=dev" /></a> -->

  [![Tag, Build & Deploy v0](https://github.com/blueboard/milestones_api/actions/workflows/tbd-v0.yml/badge.svg)](https://github.com/blueboard/milestones_api/actions/workflows/tbd-v0.yml)
  [![Lint Code](https://github.com/blueboard/milestones_api/actions/workflows/linting.yml/badge.svg)](https://github.com/blueboard/milestones_api/actions/workflows/linting.yml)

</div>

## Reference Documents
- [Alembic DB Migrations](https://blueboard.atlassian.net/wiki/spaces/PROD/pages/2774237209/Alembic+DB+Migrations)
- [Alembic Initial Setup](https://blueboard.atlassian.net/wiki/spaces/PROD/pages/2782101618/Alembic+Initial+Setup)
- [BURP: a Git Submodule](https://blueboard.atlassian.net/wiki/spaces/PROD/pages/2781315095/BURP+as+a+Git+Submodule) - Milestones uses `burp` as a submodule.
- [Login Sequence with Bearer Token](https://blueboard.atlassian.net/wiki/spaces/PROD/pages/2679570827/Login+Sequence+with+Bearer+Tokens)
- [Misc Docker Items](https://blueboard.atlassian.net/wiki/spaces/PROD/pages/2641559779/Misc+milestones-api+Docker+Items)
- [UUID and Nchar Reference](https://blueboard.atlassian.net/wiki/spaces/PROD/pages/2647457829/Canonical+UUID+Nchar+Reference)
- [Old Milestones Back Up Branch](https://github.com/blueboard/milestones_api/tree/324-DONT-DELETE-old-milestones-backup)

## Requirements

- Python 3.11 or higher
- Docker Desktop

## Running Locally
After the repo has been cloned, either of the following methods can be used to build the project locally. Both methods will start the app and database docker containers. On startup, db migrations are run and the db is seeded with mock data. The app will be started with the `--reload` flag, which will watch for changes to the code and restart the app when changes are detected.

### 1. Using `run.sh`
Script will build the docker containers and start the app. From the root of the project run:
```bash
./run.sh
```

### 2. Using `debug.sh`
Script will build the docker containers and start the app in debug mode. From the root of the project run:
```bash
./debug.sh
```
In VSCode, you can then attach to the running app by selecting the `Attach_Debugger` debug configuration.

### 3. Using `Debug Docker` launch configuration (VSCode Only)
In VSCode, select the `Debug Docker` launch configuration and start the debugger. This will build the docker containers and attaches debugger to the app container.

> [!NOTE]
> Detaching the debugger will stop and remove the containers.


# Running Tests
### pytest
To run the unit and integration tests in the containers:
```bash
./run-pytests.sh
```

### Postman
To run the Postman tests in the containers:
```bash
./run-postman.sh
```

### Job Queue
To test various job queue scenarios:
```bash
python app/producer.py
```
The jobs will be added to the queue and processed by the app worker, logging the results of the jobs to the console.
> [!NOTE]
> - Some jobs require the `milestones_api` and/or `yass_api` containers to be running for the jobs to be processed.
> - In `producer.py`, use ctrl+c to stop the script or any long running tasks.

## Migrations
On startup the app will check for any pending migrations and run them. If you need to create a new migration, run the following command:
```bash
./migration.sh --make "<migration_name>"
```
### Additional `migrate.sh` options:
- `--up` - Run all pending migrations
- `--down` - Rollback the last migration
- `--down <number>` - Rollback the last `<number>` of migrations

> [!NOTE]
> - The app must be running for migrations to be run.
> - After using --make, inspect generated migration files to confirm accurate changes.

## Deploying to dev environment
To deploy to the dev environment, add one of the following keywords to the commit message:
- `patch` - patch version bump
- `minor` - minor version bump
- `major` - major version bump

## Docker

### TL;DR...

[Docker](https://docs.docker.com/get-started/overview/) is a software tool for building and running applications based on containers.  Containers are small, lightweight execution environments that make shared use of the operating system's kernel but otherwise run in isolation from one another.

At a very high level, containers can be thought of as being similar to virtual machines.  A developer, who is maybe running OS/X on their laptop, is developing/running/testing against an application that is, itself, running in its own container with all of its own dependencies.

The application is likely running in a Linux continaer, using Docker, on a computer that is running OS/X.  In other words, the application is _not_ using tools that are installed in the developer's operating system, rather the application is running, in isolation, in a container and is fully isloated from the developer's own operating system.

[Docker Compose](https://docs.docker.com/get-started/08_using_compose/#:~:text=Docker%20Compose%20is%20a%20tool,or%20tear%20it%20all%20down.) is a tool for orchistrating one or many Docker containers.  A common use case for Docker Compose would be to start a database server in one container, then start an application server in another container, and finally to establish a virtual network between the two containers.  This would very closely mimic how an application would be configured in production.

There are literally thousands of tutorials, YouTube videos, blogs, and so on, on how to use Docker.
- https://www.docker.com/101-tutorial/

## Docker Links

- [uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)
- [Hot Reloading with Local Docker Development](https://olshansky.medium.com/hot-reloading-with-local-docker-development-1ec5dbaa4a65)

## Docker Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/), licensing is TBD

## Docker files used in milestones_api

- `docker-compose.yml` orchistrates two containers:
  - The first container is named `milestones_db` -- it is simply runs an instance of `mariadb:latest`.  Note the use of environment variables.
  - The second container is named `milestones_server` -- it has its own `Dockerfile` that specifies how it works.
- `Dockerfile` specifies how the application server itself is built.  It defines the dependencies that are needed by the application, and a sequential order of execution.  Note the use of `FROM` at the top -- this specifies that this container is based on a pre-built image named [tiangolo/uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker), which incudes numerous pre-bundled dependencies (unicorn, uvicorn, etc.) that are part of the "base container".  The sequential steps in the `Dockerfile` tell Docker how the application is to be assembled.
- `./run.sh` starts Docker Compose in a non-detached state (which is easier for debugging) -- this is a simple wrapper for `docker-compose up` command.  This brings up the containers that are defined in `docker-compose.yml`.
- `./stop.sh` stops the running containers -- it is a simple wrapper for the `docker-compose down` command.

## Useful Docker Commands

This README is not a Docker tutorial, and there are probably hundreds of useful command line commands.  [docker exec](https://docs.docker.com/engine/reference/commandline/exec/) is one that is very useful to get familar with.

## Docker Examples

### Example 1 -- What is running?

In this example, we use `docker ps` to list running containers.

```
❯ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS        PORTS                    NAMES
429850ef1ab4   milestones_api-server   "/start.sh"              16 hours ago   Up 16 hours   0.0.0.0:80->80/tcp       milestones_api
4b1654034516   mariadb:latest          "docker-entrypoint.s…"   16 hours ago   Up 16 hours   0.0.0.0:3306->3306/tcp   milestones_db
```

### Example 2 -- Get a shell in a running container

Using a container's ID (see `docker ps`) to get a `bash` shell in the running container.  You are now `root` in `/app`.

```
❯ docker exec -it 429850ef1ab4 bash
root@429850ef1ab4:/app#
```

### Example 3 -- Dump the logs from a currently running container

In this example, we use `docker logs` along with the a container ID, to dump STDOUT for the database server.

```
❯ docker logs 4b1654034516
2023-04-20 23:58:17+00:00 [Note] [Entrypoint]: Entrypoint script for MariaDB Server 1:10.11.2+maria~ubu2204 started.
2023-04-20 23:58:17+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
2023-04-20 23:58:17+00:00 [Note] [Entrypoint]: Entrypoint script for MariaDB Server 1:10.11.2+maria~ubu2204 started.
2023-04-20 23:58:17+00:00 [Note] [Entrypoint]: Initializing database files


PLEASE REMEMBER TO SET A PASSWORD FOR THE MariaDB root USER !
To do so, start the server, then issue the following command:

'/usr/bin/mariadb-secure-installation'

which will also give you the option of removing the test
databases and anonymous user created by default.  This is
strongly recommended for production servers.

See the MariaDB Knowledgebase at https://mariadb.com/kb

Please report any problems at https://mariadb.org/jira

The latest information about MariaDB is available at https://mariadb.org/.

Consider joining MariaDB's strong and vibrant community:
https://mariadb.org/get-involved/

2023-04-20 23:58:18+00:00 [Note] [Entrypoint]: Database files initialized
2023-04-20 23:58:18+00:00 [Note] [Entrypoint]: Starting temporary server
2023-04-20 23:58:18+00:00 [Note] [Entrypoint]: Waiting for server startup
...
```

## Docker Caching

A lot of work remains to optimize our use of Docker caching.  This is an area that is work in progress.

### Links

- [Fast Docker Builds With Caching (Not Only) For Python](https://towardsdatascience.com/fast-docker-builds-with-caching-for-python-533ddc3b0057)

### Example

Using the approach above, with no changes to `requirements.txt`, note the two build times here -- 27.40 and 1.010.

```
❯ time Docker build .
[+] Building 1.8s (10/14)
[+] Building 2.2s (10/14)
[+] Building 26.9s (15/15) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                      0.0s
 => => transferring dockerfile: 807B                                                                                                                      ...                                                                                        0.3s
 => exporting to image                                                                                                                                    0.2s
 => => exporting layers                                                                                                                                   0.1s
 => => writing image sha256:84af8f93a7311b2caff02d1fd75b35ee1edfd8cf159ab03d84d1e2449038f9fd                                                              0.0s
Docker build .  0.22s user 0.32s system 1% cpu 27.401 total
```

```
❯ time Docker build .                                                                 28s
[+] Building 0.7s (15/15) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                      0.0s
 => => transferring dockerfile: 37B                                                                                                                     ...
 => exporting to image                                                                                                                                    0.0s
 => => exporting layers                                                                                                                                   0.0s
 => => writing image sha256:84af8f93a7311b2caff02d1fd75b35ee1edfd8cf159ab03d84d1e2449038f9fd                                                              0.0s
Docker build .  0.09s user 0.13s system 22% cpu 1.010 total
```

## Docker Errata

### Dockerfile Expose vs. Ports

The expose section allows us to expose specific ports from our container only to other services on the same network. We can do this simply by specifying the container ports.

The ports section also exposes specified ports from containers. Unlike the previous section, ports are open not only for other services on the same network, but also to the host. The configuration is a bit more complex, where we can configure the exposed port, local binding address, and restricted protocol. Finally, depending on our preferences, we can choose between the two different syntaxes.


### Dockerfile Networks

- [Docker Compose Network](https://medium.com/@caysever/docker-compose-network-b86e424fad82)
- `network_mode: "host"` [Host networking](https://docs.docker.com/network/host/)

## Run Cron Jobs
#### Local Configuration
- Make sure CRON is set to "true" in the `docker-compose.yml`
- - If you would like to turn CRON off you can set it to "false"
- Create an environment variable in `.env` for `CRON_TOKEN`
- - Any token will work for local setup. e.g. `CRON_TOKEN=321`

#### Usage
After you have milestones running, you can verify the cron job is running two different ways:

1. You can check output the code for the cron job and verify that it is passing the right information to the correct url.
```bash
docker ps
```

Select the `CONTAINER ID` for the milestones_api and run:
```bash
docker exec -it <CONTAINER_ID> bash
```

Finally, run:
```bash
crontab -l
```
You should see a list of cron jobs. Any cron job starting with `#` is a job that is currently un-active.

2. You can check the logs from the container and you should see something like this:
- `milestones_api  | INFO:     127.0.0.1:47190 - "GET /blue/cron/rewards/send HTTP/1.1" 200 OK`

If you see a 401 Unauthorized it means you probably did not set the `CRON_TOKEN` in your `.env`, or you have not re-built the container since you did.
- `milestones_api  | INFO:     127.0.0.1:47914 - "GET /blue/cron/rewards/send HTTP/1.1" 401 Unauthorized`
