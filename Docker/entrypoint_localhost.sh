#!/usr/bin/env bash
#
# This is the Docker entrypoint script for running the Milestones app on localhost
#
set -e

echo "Cleaning up Python..."
find /app -name "*.pyc" -exec rm -f {} \;

# this is to allow Maria DB to fully start
while ! mariadb-admin ping -h'milestones_db' -P3306 -u${MYSQL_USER} -p${MYSQL_PASSWORD} 2>/dev/null; do
    echo "MariaDB not yet ready, sleeping..."
    sleep 0.5
done

cat << EOF >> /etc/bash.bashrc
alias ls='ls -la'
alias bb-mysql="mysql -u$MYSQL_USER -p${MYSQL_PASSWORD} -h${MYSQL_HOSTNAME} ${MYSQL_DATABASE}"
alias bb-clean-db="bb-mysql < migrations/milestones_nodata_v1.9.3.sql"
EOF

if [ -f "${ALEMBIC_INI_FILE}" ]; then
    echo "Alembic config file '${ALEMBIC_INI_FILE}' exists, getting alembic ready..."

    export CONN="sqlalchemy.url = mysql+pymysql\:\/\/${MYSQL_USER}\:${MYSQL_PASSWORD}\@${MYSQL_HOSTNAME}\:${MYSQL_PORT}\/${MYSQL_DATABASE}"

    # back up original ini file for good measure
    cp ${ALEMBIC_INI_FILE} "${ALEMBIC_INI_FILE}.bak"
    echo "Setting alembic connection string to use env vars for sqlalchemy.url..."

    # replace the connection string with the new connection string
    sed -i "s/sqlalchemy.url.*/$CONN/" ${ALEMBIC_INI_FILE}

    echo "Running alembic migrations..."
    alembic upgrade head
else
    echo "Alembic config file '${ALEMBIC_INI_FILE}' does not exist, skipping Alembic migrations..."
fi

# Append our cron to the system crontab and start crond
if [ ! -z ${CRON} ]; then
    echo "Configuring cron..."
    # printenv added for demo purposes with the cron job
    # printenv > /etc/environment
    # envsubst is used here to put a bearer token into the crontab
    envsubst < /crontab >> /etc/crontab
    # crontab /etc/crontab
    service cron start
    service cron status
else
    echo "Skipping cron..."
fi

echo "Debug is: ${DEBUG}"
if [ "${DEBUG}" == "True" ]; then
    echo "Starting Milestones app in debug mode, now lauch Debug Docker."
    exec sh -c "python -Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:5677 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 80"
else
    echo "Starting Milestones app"
    uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80 --reload --use-colors
fi
