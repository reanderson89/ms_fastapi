#!/usr/bin/env bash
#
# This is the Docker entrypoint script for running the Milestones app on localhost
#
set -e

echo "Cleaning up Python..."
find /app -name "*.pyc" -exec rm -f {} \;

echo "Sleeping for 10 seconds to allow Maria DB to start..."
sleep 10;

cat << EOF >> /etc/bash.bashrc
alias ls='ls -la'
alias bb-mysql="mysql -u$MYSQL_USER -p${MYSQL_PASSWORD} -h${MYSQL_HOSTNAME} ${MYSQL_DATABASE}"
alias bb-clean-db="bb-mysql < migrations/milestones_nodata_v1.4.3.sql"
EOF

# temporary solution to bootstrapping db
echo "Checking if bootstrap file '${MILESTONES_BOOTSTRAP}' exists"
if [ -f "${MILESTONES_BOOTSTRAP}" ]; then
    echo "Bootstrapping ${MYSQL_DATABASE} with SQL file ${MILESTONES_BOOTSTRAP}..."
    mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_HOSTNAME} ${MYSQL_DATABASE} < ${MILESTONES_BOOTSTRAP}
else
    echo "Bootstrap file '${MILESTONES_BOOTSTRAP}' does not exist, skipping database bootstrapping..."
fi

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

uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80 --reload --use-colors
