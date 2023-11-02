#!/usr/bin/env bash

echo "Starting db container..."
docker-compose -f docker-compose.debug.yml up --build -d milestones_db

export ENV="dev"
read -r local_HOST local_USER local_PASSWD local_PORT local_DB<<< $(python3 app/configs/database_configs.py)
while ! mysqladmin ping -h"$local_HOST" -P"$local_PORT" -u"$local_USER" -p"$local_PASSWD" --silent; do
    echo "MariaDB not yet ready, sleeping..."
    sleep 0.5
done
echo "DB ready, continuing..."

# Check if Alembic versions folder exists and has relevant files
VERSIONS_DIR="migrations/versions"
# if [ -d "$VERSIONS_DIR" ] && [ "$(find $VERSIONS_DIR -maxdepth 1 -type f)" ]; then
if [ -d "$VERSIONS_DIR" ] && [ "$(find "$VERSIONS_DIR" -maxdepth 1 -type f ! -name '.*' | wc -l)" -gt 0 ]; then
    echo "Existing Alembic migrations found. Running migrations..."
    # find "$VERSIONS_DIR" -maxdepth 1 -type f
else
    echo "No existing Alembic migrations. Creating new migration next..."
    alembic revision --autogenerate -m "Initial migration"
fi

docker-compose -f docker-compose.debug.yml up --build -d
